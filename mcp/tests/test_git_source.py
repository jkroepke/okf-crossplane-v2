from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from git import Repo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from git_source import GitSnapshot, GitSourceCache, GitSourceError


class GitSourceCacheTest(unittest.TestCase):
    def test_list_files_closes_repository(self) -> None:
        cache = GitSourceCache(Path("cache"))
        snapshot = GitSnapshot(Path("snapshot"), "a" * 40)
        blob = MagicMock(type="blob", path="examples/bucket.yaml")
        tree = MagicMock()
        tree.traverse.return_value = [blob]

        with (
            patch.object(cache, "_snapshot", return_value=snapshot),
            patch("git_source.Repo") as repository_class,
        ):
            repository = repository_class.return_value
            repository.__enter__.return_value = repository
            repository.commit.return_value.tree = tree

            self.assertEqual(
                cache.list_files("example/provider", "v1.2.3", "examples/"),
                ["examples/bucket.yaml"],
            )

        repository.__exit__.assert_called_once_with(None, None, None)

    def test_read_file_closes_repository(self) -> None:
        cache = GitSourceCache(Path("cache"))
        snapshot = GitSnapshot(Path("snapshot"), "a" * 40)
        blob = MagicMock(type="blob")
        blob.data_stream.read.return_value = b"contents"

        with (
            patch.object(cache, "_snapshot", return_value=snapshot),
            patch("git_source.Repo") as repository_class,
        ):
            repository = repository_class.return_value
            repository.__enter__.return_value = repository
            repository.commit.return_value.tree.__truediv__.return_value = blob

            self.assertEqual(
                cache.read_file("example/provider", "v1.2.3", "README.md"),
                b"contents",
            )

        repository.__exit__.assert_called_once_with(None, None, None)

    def test_clone_snapshot_closes_repository(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            cache = GitSourceCache(Path(temporary_directory) / "cache")
            snapshot_path = Path(temporary_directory) / "snapshot"
            repository = MagicMock()
            repository.__enter__.return_value = repository
            repository.commit.return_value.hexsha = "a" * 40

            with (
                patch("git_source.Git") as git_class,
                patch.object(Repo, "clone_from", return_value=repository),
            ):
                git_class.return_value.ls_remote.return_value = (
                    "a" * 40 + "\trefs/tags/v1.2.3\n"
                )

                snapshot = cache._clone_snapshot(
                    "example/provider", "v1.2.3", snapshot_path
                )

            self.assertEqual(snapshot.commit, "a" * 40)
            repository.__exit__.assert_called_once_with(None, None, None)

    def test_caches_one_immutable_snapshot_per_repository_and_tag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            working = root / "working"
            source = Repo.init(working)
            source.config_writer().set_value("user", "name", "Test User").release()
            source.config_writer().set_value(
                "user", "email", "test@example.com"
            ).release()
            crd_path = working / "package" / "crds" / "bucket.yaml"
            crd_path.parent.mkdir(parents=True)
            crd_path.write_text("kind: CustomResourceDefinition\n", encoding="utf-8")
            source.index.add([str(crd_path.relative_to(working))])
            source.index.commit("Add CRD")
            source.create_tag("v1.2.3")

            remote = root / "remotes" / "example" / "provider.git"
            remote.parent.mkdir(parents=True)
            Repo.clone_from(working, remote, bare=True)
            cache = GitSourceCache(
                root / "cache", git_base_url=f"file://{root / 'remotes'}"
            )

            self.assertEqual(
                cache.list_files("example/provider", "v1.2.3", "package/crds/"),
                ["package/crds/bucket.yaml"],
            )
            self.assertEqual(
                cache.read_file(
                    "example/provider", "v1.2.3", "package/crds/bucket.yaml"
                ),
                b"kind: CustomResourceDefinition\n",
            )

            snapshots = list(
                (root / "cache" / "provider-sources" / "example" / "provider").iterdir()
            )
            self.assertEqual(len(snapshots), 2)  # Snapshot plus its lock file.
            snapshot = next(path for path in snapshots if path.is_dir())
            self.assertTrue((snapshot / "complete").is_file())
            self.assertTrue((snapshot / "metadata.json").is_file())

    def test_rejects_a_branch_when_a_provider_tag_is_required(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            working = root / "working"
            source = Repo.init(working)
            source.config_writer().set_value("user", "name", "Test User").release()
            source.config_writer().set_value(
                "user", "email", "test@example.com"
            ).release()
            (working / "README.md").write_text("source\n", encoding="utf-8")
            source.index.add(["README.md"])
            source.index.commit("Initial commit")

            remote = root / "remotes" / "example" / "provider.git"
            remote.parent.mkdir(parents=True)
            Repo.clone_from(working, remote, bare=True)
            cache = GitSourceCache(
                root / "cache", git_base_url=f"file://{root / 'remotes'}"
            )

            with self.assertRaisesRegex(GitSourceError, "not a Git tag"):
                cache.list_files(
                    "example/provider", source.active_branch.name, "package/crds/"
                )


if __name__ == "__main__":
    unittest.main()
