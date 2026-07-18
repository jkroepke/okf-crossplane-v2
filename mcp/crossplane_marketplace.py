from __future__ import annotations

import fnmatch
import json
import re
from dataclasses import dataclass
from typing import Any, Callable
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen


class MarketplaceError(RuntimeError):
    """Raised when the Upbound Marketplace API cannot satisfy a request."""


@dataclass(frozen=True)
class PackageReference:
    account: str
    repository: str
    package_type: str

    @property
    def name(self) -> str:
        return f"{self.account}/{self.repository}"


_SEMVER = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)
_ACCOUNT_PRIORITY = {
    "crossplane-contrib": 0,
    "crossplane": 1,
    "upbound": 2,
}


class MarketplaceClient:
    def __init__(
        self,
        base_url: str = "https://api.upbound.io",
        timeout: float = 15.0,
        opener: Callable[..., Any] = urlopen,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener

    def get_versions(self, name: str) -> dict[str, Any]:
        package = self.resolve_package(name)
        metadata = self._request_json(
            f"/v1/packageMetadata/{self._segment(package.account)}/{self._segment(package.repository)}"
        )
        versions = self._versions(metadata)
        stable_versions = [version for version in versions if self._semver_key(version) is not None]
        stable_versions.sort(key=self._semver_key, reverse=True)

        latest_published = self._string(metadata.get("latestVersion")) or self._string(
            metadata.get("version")
        )
        latest_stable = stable_versions[0] if stable_versions else latest_published

        return {
            "package": package.name,
            "type": package.package_type,
            "latest": latest_stable,
            "latest_published": latest_published,
            "stable_versions": stable_versions,
            "versions": versions,
        }

    def search_resources(
        self,
        provider: str,
        pattern: str = "*",
        version: str = "latest",
        limit: int = 100,
    ) -> dict[str, Any]:
        if limit < 1 or limit > 500:
            raise ValueError("limit must be between 1 and 500")

        package = self.resolve_package(provider, expected_type="provider")
        selected_version = self._select_version(package, version)
        payload = self._request_json(
            f"/v1/packages/{self._segment(package.account)}/"
            f"{self._segment(package.repository)}/{self._segment(selected_version)}/resources"
        )
        resources = payload.get("customResourceDefinitions", [])
        if not isinstance(resources, list):
            raise MarketplaceError("Marketplace response does not contain a CRD list")

        normalized_pattern = pattern.strip() or "*"
        matches = [
            self._normalize_resource(resource)
            for resource in resources
            if isinstance(resource, dict)
            and self._resource_matches(resource, normalized_pattern)
        ]
        matches.sort(key=lambda item: (item["group"].lower(), item["kind"].lower()))
        truncated = len(matches) > limit

        return {
            "provider": package.name,
            "version": selected_version,
            "pattern": normalized_pattern,
            "count": len(matches),
            "truncated": truncated,
            "resources": matches[:limit],
        }

    def get_definitions(
        self,
        provider: str,
        resource: str,
        version: str = "latest",
    ) -> dict[str, Any]:
        package = self.resolve_package(provider, expected_type="provider")
        selected_version = self._select_version(package, version)
        match = self._resolve_resource(package, selected_version, resource)
        definition = self._request_document(
            f"/v1/packages/{self._segment(package.account)}/"
            f"{self._segment(package.repository)}/{self._segment(selected_version)}/resources/"
            f"{self._segment(match['group'])}/{self._segment(match['kind'])}"
        )
        return {
            "provider": package.name,
            "version": selected_version,
            "resource": match,
            "definition": definition,
        }

    def resolve_package(
        self,
        name: str,
        expected_type: str | None = None,
    ) -> PackageReference:
        normalized = self._normalize_package_name(name)
        if "/" in normalized:
            account, repository = normalized.split("/", 1)
            return PackageReference(
                account=account,
                repository=repository,
                package_type=expected_type or self._package_type_from_name(repository),
            )

        package_type = expected_type or self._package_type_from_name(normalized)
        query: dict[str, str | int] = {
            "query": normalized,
            "size": 100,
            "page": 0,
            "public": "true",
        }
        if package_type != "unknown":
            query["packageType"] = package_type

        payload = self._request_json("/v1/search", query)
        packages = payload.get("packages", [])
        if not isinstance(packages, list):
            raise MarketplaceError("Marketplace search response does not contain packages")

        candidates: list[PackageReference] = []
        for candidate in packages:
            if not isinstance(candidate, dict):
                continue
            account = self._string(candidate.get("account"))
            repository = self._string(candidate.get("repository")) or self._string(
                candidate.get("name")
            )
            candidate_type = self._string(candidate.get("type")) or self._string(
                candidate.get("packageType")
            )
            if not account or not repository:
                continue
            if expected_type and candidate_type and candidate_type != expected_type:
                continue
            if normalized.lower() not in {
                repository.lower(),
                self._string(candidate.get("name")).lower(),
                f"{account}/{repository}".lower(),
            }:
                continue
            candidates.append(
                PackageReference(
                    account=account,
                    repository=repository,
                    package_type=candidate_type or package_type,
                )
            )

        if not candidates:
            raise MarketplaceError(f"No public Crossplane package found for {name!r}")

        candidates.sort(
            key=lambda item: (
                _ACCOUNT_PRIORITY.get(item.account, 100),
                item.account,
                item.repository,
            )
        )
        return candidates[0]

    def _resolve_resource(
        self,
        package: PackageReference,
        version: str,
        resource: str,
    ) -> dict[str, Any]:
        payload = self._request_json(
            f"/v1/packages/{self._segment(package.account)}/"
            f"{self._segment(package.repository)}/{self._segment(version)}/resources"
        )
        resources = payload.get("customResourceDefinitions", [])
        if not isinstance(resources, list):
            raise MarketplaceError("Marketplace response does not contain a CRD list")

        needle = resource.strip().lower()
        matches = []
        for item in resources:
            if not isinstance(item, dict):
                continue
            normalized = self._normalize_resource(item)
            identities = {
                normalized["kind"].lower(),
                f"{normalized['group']}/{normalized['kind']}".lower(),
                f"{normalized['kind']}.{normalized['group']}".lower(),
            }
            if needle in identities:
                matches.append(normalized)

        if not matches:
            raise MarketplaceError(
                f"Resource {resource!r} was not found in {package.name}@{version}"
            )
        if len(matches) > 1:
            choices = ", ".join(
                f"{item['group']}/{item['kind']}" for item in matches[:10]
            )
            raise MarketplaceError(
                f"Resource {resource!r} is ambiguous; use group/kind. Matches: {choices}"
            )
        return matches[0]

    def _select_version(self, package: PackageReference, version: str) -> str:
        requested = version.strip()
        if requested and requested.lower() != "latest":
            return requested
        versions = self.get_versions(package.name)
        selected = self._string(versions.get("latest"))
        if not selected:
            raise MarketplaceError(f"No stable version found for {package.name}")
        return selected

    def _request_json(
        self,
        path: str,
        query: dict[str, str | int] | None = None,
    ) -> dict[str, Any]:
        body = self._request(path, query)
        try:
            payload = json.loads(body)
        except (TypeError, json.JSONDecodeError) as error:
            raise MarketplaceError("Marketplace API returned invalid JSON") from error
        if not isinstance(payload, dict):
            raise MarketplaceError("Marketplace API returned an unexpected JSON value")
        return payload

    def _request_document(
        self,
        path: str,
        query: dict[str, str | int] | None = None,
    ) -> Any:
        body = self._request(path, query)
        try:
            return json.loads(body)
        except (TypeError, json.JSONDecodeError):
            return body.decode("utf-8", errors="replace")

    def _request(
        self,
        path: str,
        query: dict[str, str | int] | None = None,
    ) -> bytes:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        request = Request(
            url,
            headers={
                "Accept": "application/json, application/yaml, text/yaml",
                "User-Agent": "okf-crossplane-v2-mcp/1.0",
            },
        )
        try:
            response = self._opener(request, timeout=self.timeout)
            with response:
                return response.read()
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:500]
            raise MarketplaceError(
                f"Marketplace API returned HTTP {error.code}: {detail}"
            ) from error
        except URLError as error:
            raise MarketplaceError(f"Marketplace API request failed: {error.reason}") from error
        except TimeoutError as error:
            raise MarketplaceError("Marketplace API request timed out") from error

    @staticmethod
    def _normalize_package_name(name: str) -> str:
        normalized = name.strip()
        if not normalized:
            raise ValueError("name must not be empty")
        if normalized.startswith("xpkg.upbound.io/"):
            normalized = normalized.removeprefix("xpkg.upbound.io/")
        if "@" in normalized:
            normalized = normalized.split("@", 1)[0]
        if ":" in normalized:
            normalized = normalized.rsplit(":", 1)[0]
        parts = normalized.split("/")
        if len(parts) > 2 or any(not part for part in parts):
            raise ValueError("name must be a package name or account/package reference")
        return normalized

    @staticmethod
    def _package_type_from_name(name: str) -> str:
        if name.startswith("provider-"):
            return "provider"
        if name.startswith("function-"):
            return "function"
        return "unknown"

    @staticmethod
    def _versions(metadata: dict[str, Any]) -> list[str]:
        raw = metadata.get("versions", [])
        if not isinstance(raw, list):
            return []
        return [str(version) for version in raw if isinstance(version, str)]

    @staticmethod
    def _semver_key(version: str) -> tuple[int, int, int] | None:
        match = _SEMVER.fullmatch(version)
        if match is None or match.group("prerelease") is not None:
            return None
        return (
            int(match.group("major")),
            int(match.group("minor")),
            int(match.group("patch")),
        )

    @staticmethod
    def _normalize_resource(resource: dict[str, Any]) -> dict[str, Any]:
        versions = resource.get("versions", [])
        return {
            "group": str(resource.get("group", "")),
            "kind": str(resource.get("kind", "")),
            "versions": versions if isinstance(versions, list) else [],
            "storage_version": str(resource.get("storageVersion", "")),
            "scope": str(resource.get("scope", "")),
        }

    @staticmethod
    def _resource_matches(resource: dict[str, Any], pattern: str) -> bool:
        group = str(resource.get("group", ""))
        kind = str(resource.get("kind", ""))
        normalized_pattern = pattern.lower()
        candidates = (
            group,
            kind,
            f"{group}/{kind}",
            f"{kind}.{group}",
        )
        return any(
            fnmatch.fnmatchcase(candidate.lower(), normalized_pattern)
            for candidate in candidates
        )

    @staticmethod
    def _segment(value: str) -> str:
        return quote(value, safe="")

    @staticmethod
    def _string(value: Any) -> str:
        return value if isinstance(value, str) else ""
