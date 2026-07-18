from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from crossplane_marketplace import MarketplaceClient, MarketplaceError


class FakeMarketplaceClient(MarketplaceClient):
    def __init__(self, responses: dict[str, dict[str, Any]]) -> None:
        super().__init__()
        self.responses = responses
        self.requests: list[str] = []

    def _response(self, path: str, query=None):
        key = path
        if query:
            key = f"{path}?query={query.get('query', '')}"
        self.requests.append(key)
        try:
            return self.responses[key]
        except KeyError as error:
            raise AssertionError(f"Unexpected request: {key}") from error

    def _request_json(self, path: str, query=None):  # type: ignore[override]
        return self._response(path, query)

    def _request_document(self, path: str, query=None):  # type: ignore[override]
        return self._response(path, query)


SEARCH = {
    "packages": [
        {
            "account": "upbound",
            "repository": "provider-aws",
            "name": "provider-aws",
            "type": "provider",
        },
        {
            "account": "crossplane-contrib",
            "repository": "provider-aws",
            "name": "provider-aws",
            "type": "provider",
        },
    ]
}
RESOURCES = {
    "customResourceDefinitions": [
        {
            "group": "s3.aws.upbound.io",
            "kind": "Bucket",
            "versions": ["v1beta1"],
            "storageVersion": "v1beta1",
            "scope": "Cluster",
        },
        {
            "group": "iam.aws.upbound.io",
            "kind": "Role",
            "versions": ["v1beta1"],
            "storageVersion": "v1beta1",
            "scope": "Cluster",
        },
    ]
}


class MarketplaceClientTest(unittest.TestCase):
    def test_resolve_package_prefers_crossplane_contrib(self) -> None:
        client = FakeMarketplaceClient({"/v1/search?query=provider-aws": SEARCH})

        package = client.resolve_package("provider-aws", expected_type="provider")

        self.assertEqual(package.name, "crossplane-contrib/provider-aws")

    def test_get_versions_returns_latest_stable(self) -> None:
        client = FakeMarketplaceClient(
            {
                "/v1/packageMetadata/crossplane-contrib/provider-aws": {
                    "latestVersion": "v2.0.0-rc.1",
                    "versions": ["v1.2.0", "v2.0.0-rc.1", "v1.10.0"],
                }
            }
        )

        result = client.get_versions("crossplane-contrib/provider-aws")

        self.assertEqual(result["latest"], "v1.10.0")
        self.assertEqual(result["latest_published"], "v2.0.0-rc.1")

    def test_search_resources_supports_wildcards(self) -> None:
        client = FakeMarketplaceClient(
            {
                "/v1/packageMetadata/crossplane-contrib/provider-aws": {
                    "latestVersion": "v1.10.0",
                    "versions": ["v1.10.0"],
                },
                "/v1/packages/crossplane-contrib/provider-aws/v1.10.0/resources": RESOURCES,
            }
        )

        result = client.search_resources(
            "crossplane-contrib/provider-aws", "s3.*/*Bucket"
        )

        self.assertEqual(result["count"], 1)
        self.assertEqual(result["resources"][0]["kind"], "Bucket")

    def test_get_definitions_resolves_group_and_kind(self) -> None:
        definition = {
            "apiVersion": "apiextensions.k8s.io/v1",
            "kind": "CustomResourceDefinition",
        }
        client = FakeMarketplaceClient(
            {
                "/v1/packageMetadata/crossplane-contrib/provider-aws": {
                    "latestVersion": "v1.10.0",
                    "versions": ["v1.10.0"],
                },
                "/v1/packages/crossplane-contrib/provider-aws/v1.10.0/resources": RESOURCES,
                "/v1/packages/crossplane-contrib/provider-aws/v1.10.0/resources/s3.aws.upbound.io/Bucket": definition,
            }
        )

        result = client.get_definitions(
            "crossplane-contrib/provider-aws", "s3.aws.upbound.io/Bucket"
        )

        self.assertEqual(result["definition"], definition)

    def test_missing_resource_returns_clear_error(self) -> None:
        client = FakeMarketplaceClient(
            {
                "/v1/packageMetadata/crossplane-contrib/provider-aws": {
                    "latestVersion": "v1.10.0",
                    "versions": ["v1.10.0"],
                },
                "/v1/packages/crossplane-contrib/provider-aws/v1.10.0/resources": RESOURCES,
            }
        )

        with self.assertRaisesRegex(MarketplaceError, "was not found"):
            client.get_definitions("crossplane-contrib/provider-aws", "Database")

    def test_normalizes_oci_package_reference(self) -> None:
        client = FakeMarketplaceClient({})

        package = client.resolve_package(
            "xpkg.upbound.io/crossplane-contrib/provider-aws:v1.10.0",
            expected_type="provider",
        )

        self.assertEqual(package.name, "crossplane-contrib/provider-aws")


if __name__ == "__main__":
    unittest.main()
