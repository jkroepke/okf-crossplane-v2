from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import shutil
import tempfile
import time
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast

from git import Git, Repo
from git.exc import GitCommandError


class GitSourceError(RuntimeError):
    """Raised when a local Git source snapshot cannot satisfy a request."""


@dataclass(frozen=True)
class GitSnapshot:
    """An immutable, locally cached provider source snapshot."""

    path: Path
    commit: str


_REPOSITORY_COMPONENT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


class GitSourceCache:
    """Fetch immutable provider tags once and serve files from local Git snapshots."""

    def __init__(
        self,
        cache_dir: Path,
        timeout: float = 30.0,
        git_base_url: str = "https://github.com",
    ) -> None:
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")
        self.cache_dir = cache_dir.expanduser().resolve()
        self.timeout = timeout
        self.git_base_url = git_base_url.rstrip("/")

    def list_files(self, repository: str, ref: str, prefix: str) -> list[str]:
        """List blob paths below ``prefix`` in one cached provider snapshot."""
        snapshot = self._snapshot(repository, ref)
        repo = Repo(snapshot.path)
        tree: Any = repo.commit(snapshot.commit).tree
        return sorted(
            str(item.path)
            for item in tree.traverse()
            if item.type == "blob" and item.path.startswith(prefix)
        )

    def read_file(self, repository: str, ref: str, path: str) -> bytes:
        """Read one file from a cached provider snapshot without a checkout."""
        snapshot = self._snapshot(repository, ref)
        try:
            blob: Any = Repo(snapshot.path).commit(snapshot.commit).tree / path
        except KeyError as error:
            raise FileNotFoundError(path) from error
        if blob.type != "blob":
            raise FileNotFoundError(path)
        return cast(bytes, blob.data_stream.read())

    def _snapshot(self, repository: str, ref: str) -> GitSnapshot:
        owner, name = self._repository_parts(repository)
        requested_ref = ref.strip()
        if not requested_ref:
            raise ValueError("ref must not be empty")
        snapshot_path = self._snapshot_path(owner, name, requested_ref)
        cached = self._read_snapshot(snapshot_path)
        if cached is not None:
            return cached

        with self._snapshot_lock(snapshot_path):
            cached = self._read_snapshot(snapshot_path)
            if cached is not None:
                return cached
            return self._clone_snapshot(repository, requested_ref, snapshot_path)

    def _clone_snapshot(
        self, repository: str, ref: str, snapshot_path: Path
    ) -> GitSnapshot:
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        temporary_path = Path(
            tempfile.mkdtemp(prefix=f".{snapshot_path.name}.", dir=snapshot_path.parent)
        )
        try:
            source_url = f"{self.git_base_url}/{repository}.git"
            tag_ref = f"refs/tags/{ref}"
            tag_listing = cast(
                str,
                Git().ls_remote(source_url, tag_ref, kill_after_timeout=self.timeout),
            )
            if not tag_listing.strip():
                raise GitSourceError(f"Provider version is not a Git tag: {ref}")
            repo = Repo.clone_from(
                source_url,
                temporary_path,
                bare=True,
                branch=ref,
                depth=1,
                single_branch=True,
                kill_after_timeout=self.timeout,
            )
            commit = repo.commit(f"{tag_ref}^{{commit}}").hexsha
            metadata = {
                "commit": commit,
                "fetched_at": time.time(),
                "repository": repository,
                "requested_ref": ref,
            }
            (temporary_path / "metadata.json").write_text(
                json.dumps(metadata, sort_keys=True), encoding="utf-8"
            )
            (temporary_path / "complete").touch()
            os.replace(temporary_path, snapshot_path)
            return GitSnapshot(path=snapshot_path, commit=commit)
        except (GitCommandError, OSError, ValueError) as error:
            raise GitSourceError(
                f"Could not fetch {repository}@{ref} into the local Git cache: {error}"
            ) from error
        finally:
            if temporary_path.exists():
                shutil.rmtree(temporary_path)

    def _read_snapshot(self, snapshot_path: Path) -> GitSnapshot | None:
        metadata_path = snapshot_path / "metadata.json"
        if not (snapshot_path / "complete").is_file() or not metadata_path.is_file():
            return None
        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            commit = metadata["commit"]
        except (OSError, TypeError, ValueError, KeyError) as error:
            raise GitSourceError(
                f"Cached Git snapshot is invalid: {snapshot_path}"
            ) from error
        if not isinstance(commit, str) or not re.fullmatch(r"[0-9a-f]{40}", commit):
            raise GitSourceError(
                f"Cached Git snapshot has an invalid commit: {snapshot_path}"
            )
        return GitSnapshot(path=snapshot_path, commit=commit)

    def _snapshot_path(self, owner: str, name: str, ref: str) -> Path:
        ref_digest = hashlib.sha256(ref.encode("utf-8")).hexdigest()[:16]
        return self.cache_dir / "provider-sources" / owner / name / ref_digest

    @contextmanager
    def _snapshot_lock(self, snapshot_path: Path) -> Iterator[None]:
        lock_path = snapshot_path.parent / f".{snapshot_path.name}.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+") as lock_file:
            deadline = time.monotonic() + self.timeout
            while True:
                try:
                    fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise GitSourceError(
                            f"Timed out waiting for local Git cache lock: {snapshot_path}"
                        )
                    time.sleep(0.05)
            try:
                yield
            finally:
                fcntl.flock(lock_file, fcntl.LOCK_UN)

    @staticmethod
    def _repository_parts(repository: str) -> tuple[str, str]:
        parts = repository.split("/")
        if len(parts) != 2 or not all(
            _REPOSITORY_COMPONENT.fullmatch(part) for part in parts
        ):
            raise ValueError("repository must have the form 'owner/name'")
        return parts[0], parts[1]
