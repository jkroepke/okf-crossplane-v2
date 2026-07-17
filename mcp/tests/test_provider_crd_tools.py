from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from provider_crd_tools import ProviderCRDTools, ProviderToolError, SourceFileNotFound


RESOURCES = [
    {
        "group": "apigatewayv2.aws.m.upbound.io",
        "kind": "API",
        "versions": ["v1beta1"],
        "storage_version": "v1beta1",
        "scope": "Namespaced",
    },
    {
        "group": "apigatewayv2.aws.m.upbound.io",
        "kind": "RouteResponse",
        "versions": ["v1beta1"],
        "storage_version": "v1beta1",
        "scope": "Namespaced",
    },
    {
        "group": "ec2.aws.m.upbound.io",
        "kind": "Route",
        "versions": ["v1beta1", "v1beta2"],
        "storage_version": "v1beta1",
        "scope": "Namespaced",
    },
]


class FakeMarketplace:
    def __init__(self) -> None:
        self.search_calls: list[tuple[str, str, str, int]] = []
        self.definition_calls: list[tuple[str, str, str]] = []

    def search_resources(
        self,
        provider: str,
        pattern: str = "*",
        version: str = "latest",
        limit: int = 100,
    ) -> dict[str, Any]:
        self.search_calls.append((provider, pattern, version, limit))
        matches = [
            resource
            for resource in RESOURCES
            if pattern == "*"
            or pattern.lower().strip("*") in str(resource["kind"]).lower()
        ]
        return {
            "provider": provider,
            "version": version,
            "pattern": pattern,
            "count": len(matches),
            "resources": matches,
        }

    def get_definitions(
        self,
        provider: str,
        resource: str,
        version: str = "latest",
    ) -> dict[str, Any]:
        self.definition_calls.append((provider, resource, version))
        return {
            "definition": {
                "apiVersion": "apiextensions.k8s.io/v1",
                "kind": "CustomResourceDefinition",
            }
        }


class FakeProviderCRDTools(ProviderCRDTools):
    def __init__(
        self,
        marketplace: FakeMarketplace,
        github_files: dict[str, str] | None = None,
    ) -> None:
        super().__init__(marketplace)
        self.github_files = github_files or {}

    def _read_github_file(  # type: ignore[override]
        self, repository: str, ref: str, path: str
    ) -> bytes:
        key = f"{repository}@{ref}:{path}"
        try:
            return self.github_files[key].encode()
        except KeyError as error:
            raise SourceFileNotFound(key) from error


class ProviderCRDToolsTest(unittest.TestCase):
    def test_search_uses_requested_parameter_order(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        result = tools.search(
            "upbound/provider-aws", "v2.3.0", "*RouteResponse*"
        )

        self.assertEqual(
            marketplace.search_calls[0],
            ("upbound/provider-aws", "*RouteResponse*", "v2.3.0", 500),
        )
        self.assertEqual(result["crds"][0]["kind"], "RouteResponse")

    def test_definition_accepts_api_version_and_kind_yaml(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        result = tools.get_definition(
            "upbound/provider-aws",
            "v2.3.0",
            "apiVersion: apigatewayv2.aws.m.upbound.io/v1beta1\nkind: API",
        )

        self.assertEqual(
            marketplace.definition_calls[0],
            (
                "upbound/provider-aws",
                "apigatewayv2.aws.m.upbound.io/API",
                "v2.3.0",
            ),
        )
        self.assertEqual(result["definition"]["kind"], "CustomResourceDefinition")

    def test_examples_use_latest_served_api_version(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-upjet-aws@v2.3.0"
        generated = "examples-generated/namespaced/ec2/v1beta2/route.yaml"
        handwritten = "examples/ec2/namespaced/v1beta2/route.yaml"
        tools = FakeProviderCRDTools(
            marketplace,
            {
                f"{source}:{generated}": "generated",
                f"{source}:{handwritten}": "handwritten",
            },
        )

        result = tools.get_examples(
            "upbound/provider-aws", "v2.3.0", "ec2.aws.m.upbound.io/Route"
        )

        self.assertEqual(result["examples"][0]["path"], generated)
        self.assertTrue(result["examples"][0]["generated"])
        self.assertEqual(result["examples"][1]["path"], handwritten)

    def test_terraform_docs_use_makefile_and_generated_controller(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-upjet-aws@v2.3.0"
        makefile = """
export TERRAFORM_PROVIDER_VERSION := 6.53.0
export TERRAFORM_PROVIDER_SOURCE := hashicorp/aws
export TERRAFORM_PROVIDER_REPO ?= https://github.com/hashicorp/terraform-provider-aws
export TERRAFORM_DOCS_PATH ?= website/docs/r
"""
        controller_path = (
            "internal/controller/namespaced/apigatewayv2/routeresponse/"
            "zz_controller.go"
        )
        tools = FakeProviderCRDTools(
            marketplace,
            {
                f"{source}:Makefile": makefile,
                f"{source}:{controller_path}": (
                    'o.Provider.Resources["aws_apigatewayv2_route_response"]'
                ),
            },
        )

        result = tools.get_terraform_docs(
            "upbound/provider-aws",
            "v2.3.0",
            "apigatewayv2.aws.m.upbound.io/v1beta1/RouteResponse",
        )

        self.assertEqual(result["repository"], "hashicorp/terraform-provider-aws")
        self.assertEqual(result["ref"], "v6.53.0")
        self.assertEqual(
            result["path"],
            "website/docs/r/apigatewayv2_route_response.html.markdown",
        )
        self.assertEqual(
            result["terraform_resource_name"],
            "aws_apigatewayv2_route_response",
        )

    def test_missing_crd_returns_clear_error(self) -> None:
        tools = FakeProviderCRDTools(FakeMarketplace())

        with self.assertRaisesRegex(ProviderToolError, "was not found"):
            tools.get_definition("upbound/provider-aws", "v2.3.0", "Database")

    def test_upjet_source_alias_resolves_to_package_name(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        tools.search(
            "crossplane-contrib/provider-upjet-aws", "v2.3.0", "API"
        )

        self.assertEqual(marketplace.search_calls[0][0], "upbound/provider-aws")


if __name__ == "__main__":
    unittest.main()
