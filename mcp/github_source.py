from __future__ import annotations

import base64
import fnmatch
import json
import re
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any, cast
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import yaml

from fetch_cache import IMMUTABLE_SOURCE_TTL_SECONDS, FetchCache


class GitHubSourceError(RuntimeError):
    """Raised when an OSS GitHub source cannot satisfy a request."""


@dataclass(frozen=True)
class SourceReference:
    repository: str


_SEMVER = re.compile(
    r"^v?(?P<major>0|[1-9]\d*)\."
    r"(?P<minor>0|[1-9]\d*)\."
    r"(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
    r"(?:\+[0-9A-Za-z.-]+)?$"
)
_SOURCE_ALIASES = {
    "upbound/provider-aws": "crossplane-contrib/provider-upjet-aws",
    "upbound/provider-aws-s3": "crossplane-contrib/provider-upjet-aws",
    "upbound/provider-azure": "crossplane-contrib/provider-upjet-azure",
    "upbound/provider-gcp": "crossplane-contrib/provider-upjet-gcp",
    "provider-upjet-aws": "crossplane-contrib/provider-upjet-aws",
    "provider-aws-s3": "crossplane-contrib/provider-upjet-aws",
    "provider-upjet-azure": "crossplane-contrib/provider-upjet-azure",
    "provider-upjet-gcp": "crossplane-contrib/provider-upjet-gcp",
}
_RECENT_VERSION_LIMIT = 10


class GitHubSourceClient:
    """Retrieve OSS Crossplane package versions and CRDs from GitHub."""

    def __init__(
        self,
        base_url: str = "https://api.github.com",
        timeout: float = 15.0,
        opener: Callable[..., Any] = urlopen,
        cache: FetchCache | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener
        self.cache = cache or FetchCache()

    def get_versions(self, name: str) -> dict[str, Any]:
        source = self.resolve_source(name)
        return self.cache.get_or_load(
            ("versions", source.repository),
            lambda: self._get_versions(source.repository),
        )

    def _get_versions(self, repository: str) -> dict[str, Any]:
        tags = self._list_tags(repository)
        stable_tags = [
            (tag, semantic_version)
            for tag in tags
            if (semantic_version := self._semver_key(tag["name"])) is not None
        ]
        stable_tags.sort(key=lambda item: item[1], reverse=True)
        stable_tag_values = [tag for tag, _ in stable_tags]
        latest = stable_tag_values[0]["name"] if stable_tag_values else None
        return {
            "provider": repository,
            "versions": {
                "latest": latest,
                "recent": [
                    tag["name"] for tag in stable_tag_values[:_RECENT_VERSION_LIMIT]
                ],
                "stable_count": len(stable_tag_values),
                "tag_count": len(tags),
            },
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
        source = self.resolve_source(provider)
        return self.cache.get_or_load(
            ("crd-search", source.repository, pattern, version, limit),
            lambda: self._search_resources(source.repository, pattern, version, limit),
            ttl_seconds=self._source_ttl(version),
        )

    def _search_resources(
        self, repository: str, pattern: str, version: str, limit: int
    ) -> dict[str, Any]:
        selected_version = self._select_version(repository, version)
        resources = self._resources(repository, selected_version)
        normalized_pattern = pattern.strip() or "*"
        matches = [
            resource
            for resource in resources
            if self._resource_matches(resource, normalized_pattern)
        ]
        matches.sort(key=lambda item: (item["group"].lower(), item["kind"].lower()))
        return {
            "provider": repository,
            "version": selected_version,
            "pattern": normalized_pattern,
            "count": len(matches),
            "truncated": len(matches) > limit,
            "resources": [
                self._resource_summary(resource) for resource in matches[:limit]
            ],
        }

    def get_definitions(
        self,
        provider: str,
        resource: str,
        version: str = "latest",
        path: str | None = None,
    ) -> dict[str, Any]:
        source = self.resolve_source(provider)
        return self.cache.get_or_load(
            ("crd-definition", source.repository, resource, version, path),
            lambda: self._get_definitions(source.repository, resource, version, path),
            ttl_seconds=self._source_ttl(version),
        )

    def _get_definitions(
        self, repository: str, resource: str, version: str, path: str | None
    ) -> dict[str, Any]:
        selected_version = self._select_version(repository, version)
        matches = [
            item
            for item in self._resources(repository, selected_version)
            if self._resource_matches(item, resource)
        ]
        if not matches:
            raise GitHubSourceError(
                f"Resource {resource!r} was not found in "
                f"{repository}@{selected_version}"
            )
        if len(matches) > 1:
            raise GitHubSourceError(f"Resource {resource!r} is ambiguous")
        definition = matches[0]["definition_yaml"]
        if path:
            definition = yaml.safe_dump(
                self._select_path(yaml.safe_load(definition), path), sort_keys=False
            )
        result = {
            "provider": repository,
            "version": selected_version,
            "definition_format": "yaml",
            "definition": definition,
        }
        if path:
            result["definition_path"] = path
        return result

    def resolve_source(self, name: str) -> SourceReference:
        normalized = self._normalize_name(name)
        repository = _SOURCE_ALIASES.get(normalized)
        if repository:
            return SourceReference(repository)
        if normalized.startswith("upbound/"):
            raise GitHubSourceError(
                f"No OSS GitHub source mapping is configured for {name!r}"
            )
        if "/" in normalized:
            return SourceReference(normalized)
        return SourceReference(f"crossplane-contrib/{normalized}")

    def _resources(self, repository: str, ref: str) -> list[dict[str, Any]]:
        return self.cache.get_or_load(
            ("crd-inventory", repository, ref),
            lambda: self._fetch_resources(repository, ref),
            ttl_seconds=IMMUTABLE_SOURCE_TTL_SECONDS,
        )

    def _fetch_resources(self, repository: str, ref: str) -> list[dict[str, Any]]:
        tree = self._request_json(
            f"/repos/{repository}/git/trees/{quote(ref, safe='')}", {"recursive": 1}
        )
        if not isinstance(tree, dict):
            raise GitHubSourceError("GitHub tree response is invalid")
        entries = tree.get("tree", [])
        if not isinstance(entries, list):
            raise GitHubSourceError("GitHub tree response does not contain files")
        paths = sorted(
            str(entry.get("path"))
            for entry in entries
            if isinstance(entry, dict)
            and entry.get("type") == "blob"
            and str(entry.get("path", "")).startswith("package/crds/")
            and str(entry.get("path", "")).endswith((".yaml", ".yml"))
        )
        resources = []
        for path in paths:
            resource = self._crd(repository, ref, path)
            if resource:
                resources.append(resource)
        return resources

    def _crd(self, repository: str, ref: str, path: str) -> dict[str, Any] | None:
        definition_yaml = self._read_contents(repository, path, ref)
        document = yaml.safe_load(definition_yaml)
        if (
            not isinstance(document, dict)
            or document.get("kind") != "CustomResourceDefinition"
        ):
            return None
        spec = document.get("spec")
        names = spec.get("names") if isinstance(spec, dict) else None
        versions = spec.get("versions") if isinstance(spec, dict) else None
        if not isinstance(names, dict) or not isinstance(versions, list):
            return None
        served_versions = [
            str(item.get("name"))
            for item in versions
            if isinstance(item, dict) and item.get("served")
        ]
        storage_version = next(
            (
                str(item.get("name"))
                for item in versions
                if isinstance(item, dict) and item.get("storage")
            ),
            "",
        )
        return {
            "group": str(spec.get("group", "")),
            "kind": str(names.get("kind", "")),
            "versions": served_versions,
            "storage_version": storage_version,
            "scope": str(spec.get("scope", "")),
            "definition_yaml": definition_yaml,
        }

    @staticmethod
    def _resource_summary(resource: Mapping[str, Any]) -> dict[str, Any]:
        return {
            "group": resource["group"],
            "kind": resource["kind"],
            "versions": resource["versions"],
            "storage_version": resource["storage_version"],
            "scope": resource["scope"],
        }

    @staticmethod
    def _select_path(document: object, path: str) -> object:
        if not path.startswith(".") or path == ".":
            raise ValueError("path must start with a field selector such as '.spec'")
        value = document
        for segment in path.removeprefix(".").split("."):
            match = re.fullmatch(r"(?P<field>[^\[\]]+)(?:\[(?P<index>\d+)\])?", segment)
            if match is None:
                raise ValueError(f"Invalid definition path segment: {segment!r}")
            field = match.group("field")
            if not isinstance(value, dict):
                raise ValueError(f"Definition path {path!r} does not exist")
            mapping = cast(dict[str, object], value)
            if field not in mapping:
                raise ValueError(f"Definition path {path!r} does not exist")
            value = mapping[field]
            index = match.group("index")
            if index is not None:
                if not isinstance(value, list) or int(index) >= len(value):
                    raise ValueError(f"Definition path {path!r} does not exist")
                value = value[int(index)]
        return value

    def _select_version(self, repository: str, version: str) -> str:
        requested = version.strip()
        if requested and requested.lower() != "latest":
            if requested not in {tag["name"] for tag in self._list_tags(repository)}:
                raise GitHubSourceError(
                    f"Version {requested!r} is not an OSS GitHub tag for {repository}"
                )
            return requested
        result = self.get_versions(repository)
        versions = result.get("versions")
        latest = versions.get("latest") if isinstance(versions, dict) else None
        if not isinstance(latest, str):
            raise GitHubSourceError(f"No stable version found for {repository}")
        return latest

    def _list_tags(self, repository: str) -> list[dict[str, str]]:
        return self.cache.get_or_load(
            ("github-tags", repository),
            lambda: self._fetch_tags(repository),
        )

    def _fetch_tags(self, repository: str) -> list[dict[str, str]]:
        tags = []
        page = 1
        while True:
            payload = self._request_json(
                f"/repos/{repository}/tags", {"per_page": 100, "page": page}
            )
            if not isinstance(payload, list):
                raise GitHubSourceError("GitHub tags response is invalid")
            for item in payload:
                if not isinstance(item, dict):
                    continue
                name = item.get("name")
                commit = item.get("commit")
                sha = commit.get("sha") if isinstance(commit, dict) else None
                if isinstance(name, str) and isinstance(sha, str):
                    tags.append({"name": name, "commit": sha})
            if len(payload) < 100:
                return tags
            page += 1

    def _read_contents(self, repository: str, path: str, ref: str) -> str:
        return self.cache.get_or_load(
            ("github-contents", repository, ref, path),
            lambda: self._fetch_contents(repository, path, ref),
            ttl_seconds=IMMUTABLE_SOURCE_TTL_SECONDS,
        )

    def _fetch_contents(self, repository: str, path: str, ref: str) -> str:
        payload = self._request_json(
            f"/repos/{repository}/contents/{quote(path, safe='/')}", {"ref": ref}
        )
        if not isinstance(payload, dict):
            raise GitHubSourceError("GitHub contents response is invalid")
        content = payload.get("content")
        encoding = payload.get("encoding")
        if not isinstance(content, str) or encoding != "base64":
            raise GitHubSourceError(
                "GitHub contents response does not contain base64 data"
            )
        try:
            return base64.b64decode(content).decode("utf-8")
        except (UnicodeDecodeError, ValueError) as error:
            raise GitHubSourceError(
                "GitHub contents response cannot be decoded"
            ) from error

    def _request_json(
        self, path: str, query: dict[str, str | int] | None = None
    ) -> object:
        return json.loads(self._request_bytes(path, query))

    def _request_bytes(
        self, path: str, query: dict[str, str | int] | None = None
    ) -> bytes:
        url = f"{self.base_url}{path}"
        if query:
            url = f"{url}?{urlencode(query)}"
        request = Request(
            url,
            headers={
                "Accept": "application/vnd.github+json",
                "User-Agent": "okf-crossplane-v2-mcp/1.0",
                "X-GitHub-Api-Version": "2026-03-10",
            },
        )
        try:
            response = self._opener(request, timeout=self.timeout)
            with response:
                return response.read()
        except HTTPError as error:
            detail = error.read().decode("utf-8", errors="replace")[:500]
            raise GitHubSourceError(
                f"GitHub API returned HTTP {error.code}: {detail}"
            ) from error
        except URLError as error:
            raise GitHubSourceError(
                f"GitHub API request failed: {error.reason}"
            ) from error
        except TimeoutError as error:
            raise GitHubSourceError("GitHub API request timed out") from error

    @staticmethod
    def _normalize_name(name: str) -> str:
        value = name.strip().removeprefix("xpkg.upbound.io/")
        value = value.split("@", 1)[0].rsplit(":", 1)[0]
        if not value or value.count("/") > 1:
            raise ValueError("name must be a repository or package reference")
        return value

    @staticmethod
    def _source_ttl(version: str) -> float | None:
        return (
            None
            if version.strip().lower() == "latest"
            else IMMUTABLE_SOURCE_TTL_SECONDS
        )

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
    def _resource_matches(resource: Mapping[str, Any], pattern: str) -> bool:
        identities = (
            str(resource["kind"]),
            str(resource["group"]),
            f"{resource['group']}/{resource['kind']}",
            f"{resource['kind']}.{resource['group']}",
        )
        return any(
            fnmatch.fnmatchcase(identity.lower(), pattern.lower())
            for identity in identities
        )
