from __future__ import annotations

import base64
import sys
import unittest
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from github_source import GitHubSourceClient, GitHubSourceError
from provider_crd_tools import ProviderCRDTools, ProviderToolError, SourceFileNotFound


class FakeGitHubSourceClient(GitHubSourceClient):
    def __init__(
        self, responses: dict[tuple[str, tuple[tuple[str, str | int], ...]], object]
    ) -> None:
        super().__init__()
        self.responses = responses
        self.requests: list[tuple[str, tuple[tuple[str, str | int], ...]]] = []

    def _request_json(self, path: str, query=None):  # type: ignore[override]
        key = (path, tuple(sorted((query or {}).items())))
        self.requests.append(key)
        return self.responses[key]


class FakeProviderCRDTools(ProviderCRDTools):
    def __init__(
        self, source_catalog: GitHubSourceClient, github_files: dict[str, str]
    ) -> None:
        super().__init__(source_catalog)
        self.github_files = github_files

    def _read_github_file(  # type: ignore[override]
        self, repository: str, ref: str, path: str
    ) -> bytes:
        key = f"{repository}@{ref}:{path}"
        try:
            return self.github_files[key].encode()
        except KeyError as error:
            raise SourceFileNotFound(key) from error


class GitHubSourceClientTest(unittest.TestCase):
    def test_api_requests_include_configured_token(self) -> None:
        request_log = []
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b"{}"

        def opener(request, timeout):
            request_log.append((request, timeout))
            return response

        client = GitHubSourceClient(opener=opener, token="test-token")

        self.assertEqual(client._request_bytes("/rate_limit"), b"{}")
        self.assertEqual(
            request_log[0][0].get_header("Authorization"), "Bearer test-token"
        )

    def test_api_requests_omit_authorization_without_token(self) -> None:
        request_log = []
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b"{}"

        def opener(request, timeout):
            request_log.append((request, timeout))
            return response

        client = GitHubSourceClient(opener=opener)

        client._request_bytes("/rate_limit")

        self.assertIsNone(request_log[0][0].get_header("Authorization"))

    def test_raw_source_requests_include_configured_token(self) -> None:
        request_log = []
        response = MagicMock()
        response.__enter__.return_value = response
        response.read.return_value = b"content"

        def opener(request, timeout):
            request_log.append((request, timeout))
            return response

        tools = ProviderCRDTools(MagicMock(), opener=opener, token="test-token")

        self.assertEqual(
            tools._fetch_github_file("crossplane/crossplane", "v2.0.0", "README.md"),
            b"content",
        )
        self.assertEqual(
            request_log[0][0].get_header("Authorization"), "Bearer test-token"
        )

    def _terraform_docs_tools(
        self,
        repository: str,
        version: str,
        group: str,
        kind: str,
        scope: str,
        terraform_source: str,
        terraform_repository: str,
        terraform_resource: str,
    ) -> FakeProviderCRDTools:
        service = group.split(".", 1)[0]
        directory = kind.lower()
        crd = f"""
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
spec:
  group: {group}
  scope: {scope}
  names:
    kind: {kind}
  versions:
    - name: v1beta1
      served: true
      storage: true
"""
        encoded = base64.b64encode(crd.encode()).decode()
        source = FakeGitHubSourceClient(
            {
                (f"/repos/{repository}/tags", (("page", 1), ("per_page", 100))): [
                    {"name": version, "commit": {"sha": "stable"}}
                ],
                (
                    f"/repos/{repository}/git/trees/{version}",
                    (("recursive", 1),),
                ): {"tree": [{"type": "blob", "path": "package/crds/resource.yaml"}]},
                (
                    f"/repos/{repository}/contents/package/crds/resource.yaml",
                    (("ref", version),),
                ): {"encoding": "base64", "content": encoded},
            }
        )
        source_scope = "namespaced" if scope == "Namespaced" else "cluster"
        return FakeProviderCRDTools(
            source,
            {
                f"{repository}@{version}:Makefile": f"""
export TERRAFORM_PROVIDER_VERSION := 1.2.3
export TERRAFORM_PROVIDER_SOURCE := {terraform_source}
export TERRAFORM_PROVIDER_REPO := https://github.com/{terraform_repository}
export TERRAFORM_DOCS_PATH := website/docs/r
""",
                f"{repository}@{version}:internal/controller/{source_scope}/{service}/{directory}/zz_controller.go": (
                    f'o.Provider.Resources["{terraform_resource}"]'
                ),
            },
        )

    def test_versions_use_oss_tags_and_exclude_prereleases(self) -> None:
        client = FakeGitHubSourceClient(
            {
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/tags",
                    (("page", 1), ("per_page", 100)),
                ): [
                    {"name": "v2.6.0", "commit": {"sha": "stable"}},
                    {"name": "v2.7.0-rc.1", "commit": {"sha": "candidate"}},
                ]
            }
        )

        for package_name in ("provider-aws-s3", "provider-upjet-aws"):
            with self.subTest(package_name=package_name):
                result = client.get_versions(package_name)

                self.assertEqual(
                    result["provider"], "crossplane-contrib/provider-upjet-aws"
                )
                self.assertEqual(result["versions"]["latest"], "v2.6.0")
                self.assertEqual(result["versions"]["recent"], ["v2.6.0"])
                self.assertEqual(result["versions"]["stable_count"], 1)
                self.assertEqual(result["versions"]["tag_count"], 2)

    def test_versions_and_tags_are_cached(self) -> None:
        client = FakeGitHubSourceClient(
            {
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/tags",
                    (("page", 1), ("per_page", 100)),
                ): [{"name": "v2.6.0", "commit": {"sha": "stable"}}]
            }
        )

        client.get_versions("provider-aws-s3")
        client.get_versions("provider-aws-s3")

        self.assertEqual(len(client.requests), 1)

    def test_search_reads_crds_from_the_selected_source_tag(self) -> None:
        crd = """
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
spec:
  group: s3.aws.m.upbound.io
  scope: Namespaced
  names:
    kind: Bucket
  versions:
    - name: v1beta1
      served: true
      storage: true
"""
        encoded = base64.b64encode(crd.encode()).decode()
        client = FakeGitHubSourceClient(
            {
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/tags",
                    (("page", 1), ("per_page", 100)),
                ): [{"name": "v2.6.0", "commit": {"sha": "stable"}}],
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/git/trees/v2.6.0",
                    (("recursive", 1),),
                ): {"tree": [{"type": "blob", "path": "package/crds/bucket.yaml"}]},
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/contents/package/crds/bucket.yaml",
                    (("ref", "v2.6.0"),),
                ): {"encoding": "base64", "content": encoded},
            }
        )

        result = client.search_resources(
            "upbound/provider-aws-s3", "s3.aws.m.upbound.io/Bucket", "v2.6.0"
        )

        self.assertEqual(result["provider"], "crossplane-contrib/provider-upjet-aws")
        self.assertEqual(result["resources"][0]["kind"], "Bucket")
        self.assertNotIn("definition_yaml", result["resources"][0])

        definition = client.get_definitions(
            "upbound/provider-aws-s3", "s3.aws.m.upbound.io/Bucket", "v2.6.0"
        )

        self.assertEqual(definition["definition_format"], "yaml")
        self.assertIn("kind: CustomResourceDefinition", definition["definition"])

        spec = client.get_definitions(
            "upbound/provider-aws-s3",
            "s3.aws.m.upbound.io/Bucket",
            "v2.6.0",
            ".spec",
        )

        self.assertEqual(spec["definition_path"], ".spec")
        self.assertIn("group: s3.aws.m.upbound.io", spec["definition"])
        self.assertNotIn("kind: CustomResourceDefinition", spec["definition"])

    def test_rejects_an_upbound_only_version_before_example_lookup(self) -> None:
        client = FakeGitHubSourceClient(
            {
                (
                    "/repos/crossplane-contrib/provider-upjet-aws/tags",
                    (("page", 1), ("per_page", 100)),
                ): [{"name": "v2.6.0", "commit": {"sha": "stable"}}]
            }
        )

        with self.assertRaisesRegex(
            GitHubSourceError,
            "v2.6.1.*not an OSS GitHub tag",
        ):
            client.search_resources(
                "upbound/provider-aws-s3",
                "s3.aws.m.upbound.io/Bucket",
                "v2.6.1",
            )

    def test_s3_bucket_terraform_docs_resolve_end_to_end(self) -> None:
        crd = """
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
spec:
  group: s3.aws.m.upbound.io
  scope: Namespaced
  names:
    kind: Bucket
  versions:
    - name: v1beta1
      served: true
      storage: true
"""
        encoded = base64.b64encode(crd.encode()).decode()
        repository = "crossplane-contrib/provider-upjet-aws"
        version = "v2.6.0"
        source = FakeGitHubSourceClient(
            {
                (f"/repos/{repository}/tags", (("page", 1), ("per_page", 100))): [
                    {"name": version, "commit": {"sha": "stable"}}
                ],
                (
                    f"/repos/{repository}/git/trees/{version}",
                    (("recursive", 1),),
                ): {"tree": [{"type": "blob", "path": "package/crds/bucket.yaml"}]},
                (
                    f"/repos/{repository}/contents/package/crds/bucket.yaml",
                    (("ref", version),),
                ): {"encoding": "base64", "content": encoded},
            }
        )
        tools = FakeProviderCRDTools(
            source,
            {
                f"{repository}@{version}:Makefile": """
export TERRAFORM_PROVIDER_VERSION := 6.53.0
export TERRAFORM_PROVIDER_SOURCE := hashicorp/aws
export TERRAFORM_PROVIDER_REPO := https://github.com/hashicorp/terraform-provider-aws
export TERRAFORM_DOCS_PATH := website/docs/r
""",
                f"{repository}@{version}:internal/controller/namespaced/s3/bucket/zz_controller.go": (
                    'o.Provider.Resources["aws_s3_bucket"]'
                ),
            },
        )

        result = tools.get_terraform_docs(
            "provider-aws-s3",
            version,
            "s3.aws.m.upbound.io/v1beta1/Bucket",
        )

        self.assertEqual(result["provider_name"], repository)
        self.assertEqual(result["provider_version"], version)
        self.assertEqual(result["terraform_resource_name"], "aws_s3_bucket")
        self.assertEqual(result["repository"], "hashicorp/terraform-provider-aws")
        self.assertEqual(result["ref"], "v6.53.0")
        self.assertEqual(result["path"], "website/docs/r/s3_bucket.html.markdown")

    def test_keycloak_and_openstack_terraform_docs_resolve_end_to_end(self) -> None:
        cases = [
            (
                "crossplane-contrib/provider-keycloak",
                "keycloak.crossplane.io",
                "Realm",
                "Cluster",
                "mrparkers/keycloak",
                "keycloak/terraform-provider-keycloak",
                "keycloak_realm",
                "realm.html.markdown",
            ),
            (
                "crossplane-contrib/provider-openstack",
                "compute.openstack.crossplane.io",
                "Instance",
                "Cluster",
                "terraform-provider-openstack/openstack",
                "terraform-provider-openstack/terraform-provider-openstack",
                "openstack_compute_instance_v2",
                "compute_instance_v2.html.markdown",
            ),
        ]
        for (
            provider,
            group,
            kind,
            scope,
            terraform_source,
            terraform_repository,
            terraform_resource,
            documentation,
        ) in cases:
            with self.subTest(provider=provider):
                tools = self._terraform_docs_tools(
                    provider,
                    "v1.2.3",
                    group,
                    kind,
                    scope,
                    terraform_source,
                    terraform_repository,
                    terraform_resource,
                )

                result = tools.get_terraform_docs(
                    provider, "v1.2.3", f"{group}/v1beta1/{kind}"
                )

                self.assertEqual(result["provider_name"], provider)
                self.assertEqual(result["terraform_resource_name"], terraform_resource)
                self.assertEqual(result["repository"], terraform_repository)
                self.assertEqual(result["ref"], "v1.2.3")
                self.assertEqual(result["path"], f"website/docs/r/{documentation}")

    def test_non_upjet_examples_resolve_without_terraform_metadata(
        self,
    ) -> None:
        cases = [
            (
                "crossplane-contrib/provider-kubernetes",
                "kubernetes.crossplane.io",
                "Object",
                "kubernetes",
                "v1alpha2",
            ),
            (
                "crossplane-contrib/provider-helm",
                "helm.crossplane.io",
                "Release",
                "helm",
                "v1beta1",
            ),
            (
                "crossplane-contrib/provider-sql",
                "sql.crossplane.io",
                "Database",
                "sql",
                "v1alpha1",
            ),
        ]
        for provider, group, kind, service, api_version in cases:
            with self.subTest(provider=provider):
                version = "v1.2.3"
                crd = f"""
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
spec:
  group: {group}
  scope: Cluster
  names:
    kind: {kind}
  versions:
    - name: {api_version}
      served: true
      storage: true
"""
                encoded = base64.b64encode(crd.encode()).decode()
                source = FakeGitHubSourceClient(
                    {
                        (
                            f"/repos/{provider}/tags",
                            (("page", 1), ("per_page", 100)),
                        ): [{"name": version, "commit": {"sha": "stable"}}],
                        (
                            f"/repos/{provider}/git/trees/{version}",
                            (("recursive", 1),),
                        ): {
                            "tree": [
                                {"type": "blob", "path": "package/crds/resource.yaml"}
                            ]
                        },
                        (
                            f"/repos/{provider}/contents/package/crds/resource.yaml",
                            (("ref", version),),
                        ): {"encoding": "base64", "content": encoded},
                    }
                )
                example = (
                    f"examples/{service}/cluster/{api_version}/{kind.lower()}.yaml"
                )
                tools = FakeProviderCRDTools(
                    source,
                    {
                        f"{provider}@{version}:{example}": "apiVersion: v1",
                        f"{provider}@{version}:Makefile": "# Not an Upjet provider\n",
                    },
                )

                examples = tools.get_examples(
                    provider, version, f"{group}/{api_version}/{kind}"
                )

                self.assertEqual(examples["examples"][0]["path"], example)
                self.assertFalse(examples["examples"][0]["generated"])
                with self.assertRaisesRegex(
                    ProviderToolError,
                    "TERRAFORM_PROVIDER_REPO was not found",
                ):
                    tools.get_terraform_docs(
                        provider, version, f"{group}/{api_version}/{kind}"
                    )


if __name__ == "__main__":
    unittest.main()
