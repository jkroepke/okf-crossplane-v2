from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from provider_crd_tools import ProviderCRDTools, ProviderToolError, SourceFileNotFound

RESOURCES = [
    {
        "group": "aws.m.upbound.io",
        "kind": "ProviderConfig",
        "versions": ["v1beta1"],
        "storage_version": "v1beta1",
        "scope": "Namespaced",
    },
    {
        "group": "identity.example.io",
        "kind": "ProviderConfigUsage",
        "versions": ["v1beta1"],
        "storage_version": "v1beta1",
        "scope": "Cluster",
    },
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
    {
        "group": "mysql.sql.m.crossplane.io",
        "kind": "ProviderConfig",
        "versions": ["v1alpha1"],
        "storage_version": "v1alpha1",
        "scope": "Namespaced",
    },
    {
        "group": "mssql.sql.m.crossplane.io",
        "kind": "ProviderConfig",
        "versions": ["v1alpha1"],
        "storage_version": "v1alpha1",
        "scope": "Namespaced",
    },
    {
        "group": "postgresql.sql.m.crossplane.io",
        "kind": "Grant",
        "versions": ["v1alpha1"],
        "storage_version": "v1alpha1",
        "scope": "Namespaced",
    },
    {
        "group": "keycloak.crossplane.io",
        "kind": "ProviderConfig",
        "versions": ["v1beta1"],
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
        needle = pattern.lower().strip("*")
        matches = [
            resource
            for resource in RESOURCES
            if pattern == "*"
            or needle in str(resource["kind"]).lower()
            or needle == f"{resource['group']}/{resource['kind']}".lower()
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
        path: str | None = None,
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
            "crossplane-contrib/provider-upjet-aws", "v2.3.0", "*RouteResponse*"
        )

        self.assertEqual(
            marketplace.search_calls[0],
            ("crossplane-contrib/provider-upjet-aws", "*RouteResponse*", "v2.3.0", 500),
        )
        self.assertEqual(result["crds"][0]["kind"], "RouteResponse")

    def test_search_supports_provider_config_wildcards(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        result = tools.search(
            "crossplane-contrib/provider-upjet-aws", "v2.3.0", "*ProviderConfig*"
        )

        self.assertEqual(
            marketplace.search_calls[0],
            (
                "crossplane-contrib/provider-upjet-aws",
                "*ProviderConfig*",
                "v2.3.0",
                500,
            ),
        )
        self.assertTrue(result["crds"])
        self.assertTrue(
            all(resource["kind"] == "ProviderConfig" for resource in result["crds"])
        )

    def test_crd_search_results_are_cached(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        tools.search("crossplane-contrib/provider-upjet-aws", "v2.3.0", "*Route*")
        tools.search("crossplane-contrib/provider-upjet-aws", "v2.3.0", "*Route*")

        self.assertEqual(len(marketplace.search_calls), 1)

    def test_provider_config_usage_is_excluded_from_all_crd_tools(self) -> None:
        tools = FakeProviderCRDTools(FakeMarketplace())

        with self.assertRaisesRegex(ProviderToolError, "was not found"):
            tools.get_definition(
                "crossplane-contrib/provider-upjet-aws",
                "v2.3.0",
                "identity.example.io/ProviderConfigUsage",
            )

    def test_definition_accepts_api_version_and_kind_yaml(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        result = tools.get_definition(
            "crossplane-contrib/provider-upjet-aws",
            "v2.3.0",
            "apiVersion: apigatewayv2.aws.m.upbound.io/v1beta1\nkind: API",
        )

        self.assertEqual(
            marketplace.search_calls[0],
            (
                "crossplane-contrib/provider-upjet-aws",
                "apigatewayv2.aws.m.upbound.io/API",
                "v2.3.0",
                500,
            ),
        )
        self.assertEqual(
            marketplace.definition_calls[0],
            (
                "crossplane-contrib/provider-upjet-aws",
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
            "crossplane-contrib/provider-upjet-aws",
            "v2.3.0",
            "ec2.aws.m.upbound.io/Route",
        )

        self.assertEqual(result["examples"][0]["path"], generated)
        self.assertTrue(result["examples"][0]["generated"])
        self.assertEqual(result["examples"][1]["path"], handwritten)

    def test_examples_support_package_level_provider_config_layout(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-upjet-aws@v2.6.0"
        package_level = "examples/providerconfig/namespaced/v1beta1/providerconfig.yaml"
        tools = FakeProviderCRDTools(
            marketplace,
            {f"{source}:{package_level}": "provider config"},
        )

        result = tools.get_examples(
            "crossplane-contrib/provider-upjet-aws",
            "v2.6.0",
            "aws.m.upbound.io/v1beta1/ProviderConfig",
        )

        self.assertEqual(
            result["examples"],
            [
                {
                    "repository": "crossplane-contrib/provider-upjet-aws",
                    "ref": "v2.6.0",
                    "path": package_level,
                    "generated": False,
                }
            ],
        )

    def test_examples_support_sql_service_subpaths(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-sql@v0.15.0"
        cases = [
            (
                "mysql.sql.m.crossplane.io/v1alpha1/ProviderConfig",
                "examples/namespaced/mysql/config.yaml",
            ),
            (
                "mssql.sql.m.crossplane.io/v1alpha1/ProviderConfig",
                "examples/namespaced/mssql/config.yaml",
            ),
            (
                "postgresql.sql.m.crossplane.io/v1alpha1/Grant",
                "examples/namespaced/postgresql/grant.yaml",
            ),
        ]
        tools = FakeProviderCRDTools(
            marketplace,
            {f"{source}:{path}": "example" for _, path in cases},
        )

        for crd_name, path in cases:
            with self.subTest(crd_name=crd_name):
                result = tools.get_examples(
                    "crossplane-contrib/provider-sql",
                    "v0.15.0",
                    crd_name,
                )

                self.assertEqual(result["examples"][0]["path"], path)
                self.assertFalse(result["examples"][0]["generated"])

    def test_examples_support_kind_directory_layout_without_scope(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-keycloak@main"
        path = "examples/providerconfig/providerconfig.yaml"
        tools = FakeProviderCRDTools(
            marketplace,
            {f"{source}:{path}": "provider config"},
        )

        result = tools.get_examples(
            "crossplane-contrib/provider-keycloak",
            "main",
            "keycloak.crossplane.io/v1beta1/ProviderConfig",
        )

        self.assertEqual(result["examples"][0]["path"], path)
        self.assertFalse(result["examples"][0]["generated"])

    def test_terraform_docs_use_makefile_and_generated_controller(self) -> None:
        marketplace = FakeMarketplace()
        source = "crossplane-contrib/provider-upjet-aws@v2.3.0"
        makefile = """
export TERRAFORM_PROVIDER_VERSION := 6.53.0
export TERRAFORM_PROVIDER_SOURCE := hashicorp/aws
export TERRAFORM_PROVIDER_REPO ?= https://github.com/hashicorp/terraform-provider-aws
export TERRAFORM_DOCS_PATH ?= website/docs/r
"""
        github_files = {f"{source}:Makefile": makefile}
        cases = [
            (
                "API",
                "api",
                "aws_apigatewayv2_api",
                "website/docs/r/apigatewayv2_api.html.markdown",
            ),
            (
                "RouteResponse",
                "routeresponse",
                "aws_apigatewayv2_route_response",
                "website/docs/r/apigatewayv2_route_response.html.markdown",
            ),
        ]
        for kind, directory, terraform_name, docs_path in cases:
            controller_path = (
                f"internal/controller/namespaced/apigatewayv2/{directory}/"
                "zz_controller.go"
            )
            github_files[f"{source}:{controller_path}"] = (
                f'o.Provider.Resources["{terraform_name}"]'
            )
            github_files[f"hashicorp/terraform-provider-aws@v6.53.0:{docs_path}"] = (
                f"# {terraform_name}\n"
            )
        tools = FakeProviderCRDTools(marketplace, github_files)

        for kind, _, terraform_name, docs_path in cases:
            with self.subTest(kind=kind):
                result = tools.get_terraform_docs(
                    "crossplane-contrib/provider-upjet-aws",
                    "v2.3.0",
                    f"apigatewayv2.aws.m.upbound.io/v1beta1/{kind}",
                )
                self.assertEqual(
                    result["repository"], "hashicorp/terraform-provider-aws"
                )
                self.assertEqual(result["ref"], "v6.53.0")
                self.assertEqual(result["path"], docs_path)
                self.assertEqual(result["terraform_resource_name"], terraform_name)
                self.assertEqual(result["content"], f"# {terraform_name}\n")

    def test_missing_crd_returns_clear_error(self) -> None:
        tools = FakeProviderCRDTools(FakeMarketplace())

        with self.assertRaisesRegex(ProviderToolError, "was not found"):
            tools.get_definition(
                "crossplane-contrib/provider-upjet-aws", "v2.3.0", "Database"
            )

    def test_oss_provider_name_is_preserved(self) -> None:
        marketplace = FakeMarketplace()
        tools = FakeProviderCRDTools(marketplace)

        tools.search("crossplane-contrib/provider-upjet-aws", "v2.3.0", "API")

        self.assertEqual(
            marketplace.search_calls[0][0],
            "crossplane-contrib/provider-upjet-aws",
        )


if __name__ == "__main__":
    unittest.main()
