from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from fetch_cache import IMMUTABLE_SOURCE_TTL_SECONDS, FetchCache
from git_source import GitSourceCache


class ProviderToolError(RuntimeError):
    """Raised when provider source data cannot satisfy a tool request."""


class SourceFileNotFound(ProviderToolError):
    """Raised when an expected source file does not exist."""


class SourceCatalog(Protocol):
    def search_resources(
        self,
        provider: str,
        pattern: str = "*",
        version: str = "latest",
        limit: int = 100,
    ) -> dict[str, Any]: ...

    def get_definitions(
        self,
        provider: str,
        resource: str,
        version: str = "latest",
        path: str | None = None,
    ) -> dict[str, Any]: ...


@dataclass(frozen=True)
class ProviderSource:
    repository: str
    ref: str


_KUBERNETES_API_VERSION = re.compile(
    r"^v(?P<major>[1-9]\d*)(?:(?P<stage>alpha|beta)(?P<number>[1-9]\d*))?$"
)
_MAKE_ASSIGNMENT = r"^(?:export\s+)?{name}\s*(?::=|\?=|=)\s*(?P<value>[^#\n]+)"
_MAX_CRD_RESULTS = 100


class ProviderCRDTools:
    def __init__(
        self,
        source_catalog: SourceCatalog,
        github_raw_url: str = "https://raw.githubusercontent.com",
        timeout: float = 15.0,
        opener: Callable[..., Any] = urlopen,
        cache: FetchCache | None = None,
        token: str | None = None,
        source_cache: GitSourceCache | None = None,
    ) -> None:
        self.source_catalog = source_catalog
        self.github_raw_url = github_raw_url.rstrip("/")
        self.timeout = timeout
        self._opener = opener
        self.cache = cache or FetchCache()
        self.token = token
        self.source_cache = source_cache

    def search(
        self,
        provider_name: str,
        provider_version: str,
        crd_search_term: str,
    ) -> dict[str, Any]:
        return self.cache.get_or_load(
            ("provider-search", provider_name, provider_version, crd_search_term),
            lambda: self._search(provider_name, provider_version, crd_search_term),
            ttl_seconds=self._source_ttl(provider_version),
        )

    def _search(
        self,
        provider_name: str,
        provider_version: str,
        crd_search_term: str,
    ) -> dict[str, Any]:
        result = self.source_catalog.search_resources(
            provider_name,
            crd_search_term.strip() or "*",
            provider_version,
            500,
        )
        crds = result.get("resources", [])
        if not isinstance(crds, list):
            raise ProviderToolError(
                "Provider resource search returned an invalid CRD list"
            )
        filtered_crds = [
            crd
            for crd in crds
            if isinstance(crd, dict) and not self._is_provider_config_usage(crd)
        ]
        return {
            "provider_name": result.get("provider"),
            "provider_version": result.get("version"),
            "crd_search_term": result.get("pattern"),
            "count": len(filtered_crds),
            "truncated": len(filtered_crds) > _MAX_CRD_RESULTS,
            "crds": filtered_crds[:_MAX_CRD_RESULTS],
        }

    def get_definition(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
        path: str | None = None,
    ) -> dict[str, Any]:
        return self.cache.get_or_load(
            ("provider-definition", provider_name, provider_version, crd_name, path),
            lambda: self._get_definition(
                provider_name, provider_version, crd_name, path
            ),
            ttl_seconds=self._source_ttl(provider_version),
        )

    def _get_definition(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
        path: str | None,
    ) -> dict[str, Any]:
        provider, version, resource = self._resolve_resource(
            provider_name, provider_version, crd_name
        )
        result = self.source_catalog.get_definitions(
            provider, f"{resource['group']}/{resource['kind']}", version, path
        )
        output = {
            "provider_name": provider,
            "provider_version": version,
            "crd": resource,
            "definition_format": result.get("definition_format", "yaml"),
            "definition": result.get("definition"),
        }
        if path:
            output["definition_path"] = path
        return output

    def get_examples(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
    ) -> dict[str, Any]:
        return self.cache.get_or_load(
            ("provider-examples", provider_name, provider_version, crd_name),
            lambda: self._get_examples(provider_name, provider_version, crd_name),
            ttl_seconds=self._source_ttl(provider_version),
        )

    def _get_examples(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
    ) -> dict[str, Any]:
        provider, version, resource = self._resolve_resource(
            provider_name, provider_version, crd_name
        )
        source = self._provider_source(provider, version)
        api_version = self._resource_api_version(resource)
        service = self._resource_service(resource)
        scope = self._resource_scope(resource)
        filename = f"{self._kind_directory(resource['kind'])}.yaml"
        candidates = [
            (
                True,
                f"examples-generated/{scope}/{service}/{api_version}/{filename}",
            ),
            (
                False,
                f"examples/{service}/{scope}/{api_version}/{filename}",
            ),
        ]
        examples = [
            {
                "repository": source.repository,
                "ref": source.ref,
                "path": path,
                "generated": generated,
            }
            for generated, path in candidates
            if self._github_file_exists(source.repository, source.ref, path)
        ]
        if not examples:
            attempted = ", ".join(path for _, path in candidates)
            raise ProviderToolError(
                f"No examples found in {source.repository}@{source.ref}. "
                f"Tried: {attempted}"
            )
        return {
            "provider_name": provider,
            "provider_version": version,
            "crd": resource,
            "examples": examples,
        }

    def get_terraform_docs(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
    ) -> dict[str, Any]:
        return self.cache.get_or_load(
            ("provider-terraform-docs", provider_name, provider_version, crd_name),
            lambda: self._get_terraform_docs(provider_name, provider_version, crd_name),
            ttl_seconds=self._source_ttl(provider_version),
        )

    def _get_terraform_docs(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
    ) -> dict[str, Any]:
        provider, version, resource = self._resolve_resource(
            provider_name, provider_version, crd_name
        )
        source = self._provider_source(provider, version)
        makefile = self._read_github_text(source.repository, source.ref, "Makefile")
        terraform_repository = self._github_repository_from_url(
            self._make_variable(makefile, "TERRAFORM_PROVIDER_REPO")
        )
        terraform_version = self._make_variable(makefile, "TERRAFORM_PROVIDER_VERSION")
        terraform_source = self._make_variable(makefile, "TERRAFORM_PROVIDER_SOURCE")
        docs_path = self._make_variable(makefile, "TERRAFORM_DOCS_PATH")
        terraform_resource = self._terraform_resource_name(source, resource)
        provider_prefix = terraform_source.rsplit("/", 1)[-1]
        docs_resource = terraform_resource.removeprefix(f"{provider_prefix}_")
        return {
            "provider_name": provider,
            "provider_version": version,
            "crd": resource,
            "terraform_resource_name": terraform_resource,
            "repository": terraform_repository,
            "ref": self._version_tag(terraform_version),
            "path": (f"{docs_path.rstrip('/')}/{docs_resource}.html.markdown"),
        }

    def _resolve_resource(
        self,
        provider_name: str,
        provider_version: str,
        crd_name: str,
    ) -> tuple[str, str, dict[str, Any]]:
        group, api_version, kind = self._parse_crd_name(crd_name)
        search_pattern = f"{group}/{kind}" if group else kind
        result = self.source_catalog.search_resources(
            provider_name,
            search_pattern,
            provider_version,
            500,
        )
        resources = result.get("resources", [])
        if not isinstance(resources, list):
            raise ProviderToolError(
                "Provider resource search returned an invalid CRD list"
            )
        matches = []
        for resource in resources:
            if not isinstance(resource, dict):
                continue
            if self._is_provider_config_usage(resource):
                continue
            if str(resource.get("kind", "")).lower() != kind.lower():
                continue
            if group and str(resource.get("group", "")).lower() != group.lower():
                continue
            versions = resource.get("versions", [])
            if api_version and api_version not in versions:
                continue
            normalized = dict(resource)
            if api_version:
                normalized["requested_api_version"] = api_version
            matches.append(normalized)
        provider = str(result.get("provider", ""))
        version = str(result.get("version", ""))
        if not matches:
            raise ProviderToolError(
                f"CRD {crd_name!r} was not found in {provider}@{version}"
            )
        if len(matches) > 1:
            choices = ", ".join(
                f"{item.get('group')}/{item.get('kind')}" for item in matches[:10]
            )
            raise ProviderToolError(
                f"CRD {crd_name!r} is ambiguous; use group/version/kind. "
                f"Matches: {choices}"
            )
        return provider, version, matches[0]

    def _terraform_resource_name(
        self, source: ProviderSource, resource: dict[str, Any]
    ) -> str:
        controller_path = (
            f"internal/controller/{self._resource_scope(resource)}/"
            f"{self._resource_service(resource)}/"
            f"{self._kind_directory(str(resource['kind']))}/zz_controller.go"
        )
        controller = self._read_github_text(
            source.repository, source.ref, controller_path
        )
        matches = re.findall(r'o\.Provider\.Resources\["([^"]+)"\]', controller)
        if not matches:
            raise ProviderToolError(
                f"Terraform mapping not found in {source.repository}@"
                f"{source.ref}:{controller_path}"
            )
        if len(set(matches)) > 1:
            raise ProviderToolError(
                f"Multiple Terraform mappings found in {source.repository}@"
                f"{source.ref}:{controller_path}"
            )
        return matches[0]

    @staticmethod
    def _provider_source(provider: str, version: str) -> ProviderSource:
        return ProviderSource(repository=provider, ref=version)

    @staticmethod
    def _parse_crd_name(crd_name: str) -> tuple[str, str, str]:
        value = crd_name.strip()
        if not value:
            raise ValueError("crd_name must not be empty")
        api_version_match = re.search(r"(?m)^apiVersion:\s*(\S+)\s*$", value)
        kind_match = re.search(r"(?m)^kind:\s*(\S+)\s*$", value)
        if api_version_match and kind_match:
            api_value = api_version_match.group(1)
            if "/" not in api_value:
                raise ValueError("apiVersion must contain a group and version")
            group, api_version = api_value.rsplit("/", 1)
            return group, api_version, kind_match.group(1)
        parts = value.split("/")
        if len(parts) == 1:
            return "", "", parts[0]
        if len(parts) == 2:
            return parts[0], "", parts[1]
        if len(parts) == 3:
            return parts[0], parts[1], parts[2]
        raise ValueError(
            "crd_name must be kind, group/kind, group/version/kind, or YAML "
            "with apiVersion and kind"
        )

    @classmethod
    def _resource_api_version(cls, resource: dict[str, Any]) -> str:
        requested = str(resource.get("requested_api_version", ""))
        if requested:
            return requested
        versions = resource.get("versions", [])
        if isinstance(versions, list) and versions:
            values = [str(version) for version in versions]
            return max(values, key=cls._kubernetes_api_version_key)
        storage = str(resource.get("storage_version", ""))
        if storage:
            return storage
        raise ProviderToolError("CRD does not expose an API version")

    @staticmethod
    def _kubernetes_api_version_key(version: str) -> tuple[int, int, int]:
        match = _KUBERNETES_API_VERSION.fullmatch(version)
        if match is None:
            return (0, 0, 0)
        stability = {None: 3, "beta": 2, "alpha": 1}[match.group("stage")]
        return (
            int(match.group("major")),
            stability,
            int(match.group("number") or 0),
        )

    @staticmethod
    def _resource_service(resource: dict[str, Any]) -> str:
        service = str(resource.get("group", "")).split(".", 1)[0]
        if not service:
            raise ProviderToolError("CRD group does not contain a provider service")
        return service

    @staticmethod
    def _resource_scope(resource: dict[str, Any]) -> str:
        return (
            "namespaced"
            if str(resource.get("scope", "")).lower() == "namespaced"
            else "cluster"
        )

    @staticmethod
    def _is_provider_config_usage(resource: dict[str, Any]) -> bool:
        return str(resource.get("kind", "")).casefold() == "providerconfigusage"

    @staticmethod
    def _source_ttl(version: str) -> float | None:
        return (
            None
            if version.strip().lower() == "latest"
            else IMMUTABLE_SOURCE_TTL_SECONDS
        )

    @staticmethod
    def _kind_directory(kind: str) -> str:
        value = re.sub(r"[^0-9A-Za-z]", "", kind).lower()
        if not value:
            raise ProviderToolError("CRD kind cannot be converted to a source path")
        return value

    @staticmethod
    def _make_variable(makefile: str, name: str) -> str:
        pattern = re.compile(
            _MAKE_ASSIGNMENT.format(name=re.escape(name)), re.MULTILINE
        )
        match = pattern.search(makefile)
        if match is None:
            raise ProviderToolError(f"{name} was not found in the provider Makefile")
        value = match.group("value").strip().strip("\"'")
        if not value or "$" in value:
            raise ProviderToolError(
                f"{name} is empty or requires Make variable expansion"
            )
        return value

    @staticmethod
    def _github_repository_from_url(url: str) -> str:
        value = url.strip().removesuffix(".git").rstrip("/")
        for prefix in (
            "https://github.com/",
            "http://github.com/",
            "git@github.com:",
        ):
            if value.startswith(prefix):
                repository = value.removeprefix(prefix)
                if repository.count("/") == 1:
                    return repository
        raise ProviderToolError(f"Unsupported GitHub repository URL: {url}")

    @staticmethod
    def _version_tag(version: str) -> str:
        return version if version.startswith("v") else f"v{version}"

    def _read_github_file(self, repository: str, ref: str, path: str) -> bytes:
        if self.source_cache is not None:
            try:
                return self.source_cache.read_file(repository, ref, path)
            except FileNotFoundError as error:
                raise SourceFileNotFound(path) from error
        return self.cache.get_or_load(
            ("github-raw", repository, ref, path),
            lambda: self._fetch_github_file(repository, ref, path),
            ttl_seconds=IMMUTABLE_SOURCE_TTL_SECONDS,
        )

    def _fetch_github_file(self, repository: str, ref: str, path: str) -> bytes:
        url = (
            f"{self.github_raw_url}/{repository}/{quote(ref, safe='')}/"
            f"{quote(path, safe='/')}"
        )
        headers = {"User-Agent": "okf-crossplane-v2-mcp/1.0"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = Request(url, headers=headers)
        try:
            response = self._opener(request, timeout=self.timeout)
            with response:
                return response.read()
        except HTTPError as error:
            if error.code == 404:
                raise SourceFileNotFound(url) from error
            detail = error.read().decode("utf-8", errors="replace")[:500]
            raise ProviderToolError(
                f"GitHub source returned HTTP {error.code}: {detail}"
            ) from error
        except URLError as error:
            raise ProviderToolError(
                f"GitHub source request failed: {error.reason}"
            ) from error
        except TimeoutError as error:
            raise ProviderToolError("GitHub source request timed out") from error

    def _read_github_text(self, repository: str, ref: str, path: str) -> str:
        return self._read_github_file(repository, ref, path).decode(
            "utf-8", errors="replace"
        )

    def _github_file_exists(self, repository: str, ref: str, path: str) -> bool:
        try:
            self._read_github_file(repository, ref, path)
        except SourceFileNotFound:
            return False
        return True
