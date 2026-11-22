#!/usr/bin/env python3
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Check an OKF v0.3 bundle for conformance and field shape.

Errors are conformance failures under SPEC.md section 11.1. Warnings are
values that do not follow the other sections, including Markdown files that
are not concepts (section 3.2 asks validators to warn about them). Info
findings need no fix, for example a concept that is past its stale_after date.

Usage:
    validate.py BUNDLE_ROOT [--json] [--strict] [--now DATETIME]

Exit status:
    0  no errors (and no warnings, with --strict)
    1  errors (or warnings, with --strict)
    2  usage or setup problem
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("validate.py needs PyYAML. Install it with: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

STATUSES = ("draft", "stable", "deprecated")
DATETIME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ACTOR_RE = re.compile(r"^([^\s/:]+/\S+|[A-Za-z][A-Za-z0-9+.-]*:\S+)$")
SPDX_RE = re.compile(r"^[A-Za-z0-9.+-]+( (AND|OR|WITH) [A-Za-z0-9.+-]+)*$")
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FOOTNOTE_RE = re.compile(r"\[\^([^\]\s]+)\]")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
SCHEME_RE = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")
BOM = "\ufeff"
KNOWN_KEYS = frozenset({
    "type", "title", "description", "resource", "tags", "sources", "usage_window",
    "generated", "verified", "status", "superseded_by", "stale_after", "runtime",
    "parameters", "computation", "executor", "attester", "timestamp",
})


class DuplicateKeyError(Exception):
    def __init__(self, key: Any, line: int) -> None:
        super().__init__(f"duplicate key {key!r}")
        self.key = key
        self.line = line


class _Loader(yaml.SafeLoader):
    """SafeLoader that keeps timestamps as text and refuses duplicate keys.

    PyYAML follows YAML 1.1 and turns 2026-06-30T14:00:00Z into a datetime,
    which hides the form that the author wrote. Section 4 also forbids
    duplicate keys, which PyYAML would otherwise accept silently.
    """

    def construct_mapping(self, node, deep=False):
        seen = set()
        for key_node, _ in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in seen:
                raise DuplicateKeyError(key, key_node.start_mark.line + 1)
            seen.add(key)
        return super().construct_mapping(node, deep=deep)


_Loader.yaml_implicit_resolvers = {
    ch: [(tag, rx) for tag, rx in resolvers if tag != "tag:yaml.org,2002:timestamp"]
    for ch, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


@dataclass
class Finding:
    path: str
    line: int | None
    level: str  # "error", "warning", or "info"
    code: str
    message: str


def blank(value: Any) -> bool:
    """Section 11.2: null, an empty string, and an empty list mean an absent key."""
    return value is None or value == "" or value == []


def as_list(value: Any) -> list:
    """Section 11.2: one item stands for a list with one item."""
    if blank(value):
        return []
    return value if isinstance(value, list) else [value]


def parse_timestamp(value: Any) -> datetime | None:
    """Parse the two RFC 3339 forms that section 5 allows. Return None otherwise."""
    if not isinstance(value, str):
        return None
    try:
        if DATE_RE.match(value):
            return datetime.fromisoformat(value + "T00:00:00+00:00")
        if DATETIME_RE.match(value):
            # Python 3.9 and 3.10 fromisoformat() does not accept "Z".
            return datetime.fromisoformat(value.upper().replace("Z", "+00:00"))  # noqa: FURB162
    except ValueError:
        return None
    return None


def split_frontmatter(text: str) -> tuple[str, dict, str, int]:
    """Return (state, frontmatter, body, first body line number).

    state is "ok", "absent", "duplicate:<line>:<key>", or a message that says
    why the block is not readable.
    """
    lines = text.splitlines()
    if not lines or lines[0].rstrip("\r") != "---":
        return "absent", {}, text, 1
    for index in range(1, len(lines)):
        if lines[index].rstrip("\r") == "---":
            block = "\n".join(lines[1:index])
            body = "\n".join(lines[index + 1:])
            try:
                meta = yaml.load(block, Loader=_Loader)
            except DuplicateKeyError as exc:
                return f"duplicate:{exc.line + 1}:{exc.key}", {}, body, index + 2
            except yaml.YAMLError as exc:
                return f"invalid YAML ({str(exc).splitlines()[0]})", {}, body, index + 2
            if meta is None:
                meta = {}
            if not isinstance(meta, dict):
                return "frontmatter is not a YAML mapping", {}, body, index + 2
            return "ok", meta, body, index + 2
    return "the closing --- line is missing", {}, "", len(lines) + 1


def starts_with_frontmatter(text: str) -> bool:
    lines = text.splitlines()
    return bool(lines) and lines[0].rstrip("\r") == "---"


def prose_lines(body: str):
    """Yield (offset, line) for body lines outside fenced and indented code."""
    fence = None
    for offset, line in enumerate(body.splitlines()):
        stripped = line.lstrip()
        if fence is None and stripped.startswith(("```", "~~~")):
            fence = stripped[:3]
            continue
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if line.startswith(("    ", "\t")):
            continue
        yield offset, INLINE_CODE_RE.sub("", line)


def computation_fences(body: str) -> int:
    """Count fenced code blocks in the Computation section (section 10.3).

    The section starts at a heading named Computation at any ATX level and
    ends at the next heading of the same or a higher level.
    """
    level = None
    count = 0
    fence = None
    for line in body.splitlines():
        stripped = line.lstrip()
        if fence is not None:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith(("```", "~~~")):
            fence = stripped[:3]
            if level is not None:
                count += 1
            continue
        match = HEADING_RE.match(line)
        if match:
            depth = len(match.group(1))
            if level is not None and depth <= level:
                break
            if level is None and match.group(2).strip().lower() == "computation":
                level = depth
    return count


def version_tuple(value: Any) -> tuple[int, ...] | None:
    try:
        return tuple(int(part) for part in str(value).split("."))
    except ValueError:
        return None


class Checker:
    def __init__(self, bundle: Path, now: datetime) -> None:
        self.bundle = bundle
        self.now = now
        self.findings: list[Finding] = []
        self.files_checked = 0
        self.okf_version = self.read_okf_version()
        declared = version_tuple(self.okf_version) if self.okf_version is not None else None
        # Section 6.2: a bundle that declares 0.2 or earlier, or no version,
        # may resolve a bare path field from the bundle root as a fallback.
        self.root_fallback = declared is None or declared <= (0, 2)

    def read_okf_version(self) -> Any:
        root_index = self.bundle / "index.md"
        if not root_index.is_file():
            return None
        state, meta, _, _ = split_frontmatter(root_index.read_text(encoding="utf-8").lstrip(BOM))
        return meta.get("okf_version") if state == "ok" else None

    # ---- reporting ----------------------------------------------------------

    def add(self, path: Path, line: int | None, level: str, code: str, message: str) -> None:
        rel = path.relative_to(self.bundle).as_posix() if path != self.bundle else "."
        self.findings.append(Finding(rel, line, level, code, message))

    def error(self, path: Path, line: int | None, code: str, message: str) -> None:
        self.add(path, line, "error", code, message)

    def warn(self, path: Path, line: int | None, code: str, message: str) -> None:
        self.add(path, line, "warning", code, message)

    def info(self, path: Path, line: int | None, code: str, message: str) -> None:
        self.add(path, line, "info", code, message)

    # ---- traversal ----------------------------------------------------------

    def run(self) -> None:
        if not (self.bundle / "index.md").is_file():
            self.warn(self.bundle, None, "W125", 'add a bundle-root index.md with okf_version: "0.3" (section 8.1)')
        for path in sorted(self.bundle.rglob("*.md")):
            parts = path.relative_to(self.bundle).parts
            if any(p.startswith(".") for p in parts):
                continue  # Section 3.2: dot-paths are not part of the bundle.
            if not self.inside(path.resolve()):
                continue  # Section 3.2: do not follow links out of the bundle root.
            self.files_checked += 1
            text = path.read_text(encoding="utf-8").lstrip(BOM)
            if path.name == "index.md":
                self.check_index(path, text)
            elif path.name == "log.md":
                self.check_log(path, text)
            else:
                self.check_markdown(path, text)

    def inside(self, path: Path) -> bool:
        try:
            path.relative_to(self.bundle)
        except ValueError:
            return False
        return True

    def frontmatter(self, path: Path, text: str) -> tuple[str, dict, str, int]:
        """Split and report the two conformance failures that any block can have."""
        state, meta, body, body_line = split_frontmatter(text)
        if state.startswith("duplicate:"):
            _, line, key = state.split(":", 2)
            self.error(path, int(line), "E007", f"frontmatter repeats the key {key!r}; keys must be unique (section 4)")
        elif state not in ("ok", "absent"):
            self.error(path, 1, "E002", f"frontmatter does not parse as a YAML mapping: {state} (section 4)")
        return state, meta, body, body_line

    # ---- reserved files (sections 8 and 9) ----------------------------------

    def check_index(self, path: Path, text: str) -> None:
        if path.parent != self.bundle:
            if starts_with_frontmatter(text):
                self.error(path, 1, "E004", "an index.md below the bundle root has no frontmatter (section 8)")
            return
        state, meta, _, _ = self.frontmatter(path, text)
        if state == "absent":
            self.warn(path, 1, "W125", 'give the root index.md frontmatter with okf_version: "0.3" (section 8.1)')
            return
        if state != "ok":
            return
        version = meta.get("okf_version")
        if blank(version):
            self.warn(path, 1, "W125", 'add okf_version: "0.3" to the root index.md (section 8.1)')
        elif not isinstance(version, str):
            self.warn(path, 1, "W117", f'quote okf_version as a string, for example "0.3" (section 8.1); found {version!r}')
        license_value = meta.get("license")
        if (
            isinstance(license_value, str)
            and not SPDX_RE.match(license_value)
            and self.resolve_path(path, license_value, field=True)[0] == "missing"
        ):
            self.warn(path, 1, "W116", f"license {license_value!r} is not an SPDX expression or a file in the bundle (section 8.1)")

    def check_log(self, path: Path, text: str) -> None:
        if starts_with_frontmatter(text):
            self.error(path, 1, "E006", "log.md has no frontmatter (section 9)")
        dates: list[tuple[int, str]] = []
        for number, line in enumerate(text.splitlines(), start=1):
            if line.startswith("## "):
                heading = line[3:].strip()
                if DATE_RE.match(heading):
                    dates.append((number, heading))
                else:
                    self.error(path, number, "E005", f"a log.md date heading must be YYYY-MM-DD (section 9); found {heading!r}")
        # zip() instead of itertools.pairwise(), which needs Python 3.10.
        for (_, newer), (number, older) in zip(dates, dates[1:]):  # noqa: RUF007
            if older > newer:
                self.warn(path, number, "W118", f"log.md puts the newest date first (section 9); {older} follows {newer}")

    # ---- concepts (sections 3.2, 4, 5, 6, 10) -------------------------------

    def check_markdown(self, path: Path, text: str) -> None:
        state, meta, body, body_line = self.frontmatter(path, text)
        if state == "absent":
            self.warn(path, 1, "W120", "not a concept: the file has no frontmatter (section 3.2)")
            return
        if state != "ok":
            return
        concept_type = meta.get("type")
        if not isinstance(concept_type, str) or not concept_type.strip():
            self.warn(path, 1, "W120", "not a concept: the frontmatter has no non-empty type (section 3.2)")
            return

        self.check_strings(path, meta)
        self.check_tags(path, meta)
        self.check_lifecycle(path, meta)
        generated_at = self.check_generated(path, meta)
        self.check_verified(path, meta, generated_at)
        source_ids = self.check_sources(path, meta)
        self.check_stale_after(path, meta)
        if not blank(meta.get("resource")):
            self.check_path_field(path, "resource", meta.get("resource"))
        self.check_body(path, body, body_line, source_ids)
        if concept_type == "Attested Computation":
            self.check_computation(path, meta, body)
        unknown = sorted(str(k) for k in meta if str(k) not in KNOWN_KEYS and not str(k).startswith("x-"))
        if unknown:
            self.info(path, 1, "I203", f"extension keys without the x- prefix: {', '.join(unknown)} (section 4.1)")

    def check_strings(self, path: Path, meta: dict) -> None:
        for key in ("type", "title", "description", "status"):
            value = meta.get(key)
            if value is not None and not isinstance(value, str):
                self.warn(path, 1, "W117", f"quote {key}: it parses as {type(value).__name__}, not a string (section 4)")

    def check_tags(self, path: Path, meta: dict) -> None:
        tags = meta.get("tags")
        if isinstance(tags, str) and tags.strip():
            hint = f"; consumers read it as the single tag {tags!r}" if "," in tags else ""
            self.warn(path, 1, "W110", f"write tags as a YAML list (sections 4.1 and 11.2){hint}")
        elif tags is not None and not isinstance(tags, (list, str)):
            self.warn(path, 1, "W110", "write tags as a YAML list of strings (section 4.1)")

    def check_lifecycle(self, path: Path, meta: dict) -> None:
        status = meta.get("status")
        if not blank(status) and status not in STATUSES:
            self.warn(path, 1, "W105", f"status is draft, stable, or deprecated; consumers treat {status!r} as not current (section 5.4)")
        superseded_by = meta.get("superseded_by")
        if blank(superseded_by):
            return
        if status != "deprecated":
            self.warn(path, 1, "W123", "superseded_by has a meaning only with status: deprecated (section 5.4)")
        self.check_path_field(path, "superseded_by", superseded_by)

    def check_generated(self, path: Path, meta: dict) -> datetime | None:
        generated = meta.get("generated")
        if blank(generated):
            return None
        if not isinstance(generated, dict) or blank(generated.get("by")):
            self.warn(path, 1, "W102", "generated is a mapping with a by field (section 5.2)")
            return None
        self.check_actor(path, "generated.by", generated.get("by"))
        if blank(generated.get("at")):
            return None
        moment = self.check_timestamp(path, "generated.at", generated.get("at"))
        if moment is not None and DATE_RE.match(str(generated.get("at"))):
            self.warn(path, 1, "W122", "write generated.at as a date-time, because consumers compare it with verified[].at (section 5)")
        return moment

    def check_verified(self, path: Path, meta: dict, generated_at: datetime | None) -> None:
        times = []
        for index, event in enumerate(as_list(meta.get("verified"))):
            field = f"verified[{index}]"
            if not isinstance(event, dict) or blank(event.get("by")) or blank(event.get("at")):
                self.warn(path, 1, "W104", f"{field} needs by and at; consumers ignore it (section 5.2)")
                continue
            self.check_actor(path, f"{field}.by", event.get("by"))
            moment = self.check_timestamp(path, f"{field}.at", event.get("at"))
            if moment is not None:
                times.append(moment)
                if DATE_RE.match(str(event.get("at"))):
                    self.warn(path, 1, "W122", f"write {field}.at as a date-time, because consumers compare it with generated.at (section 5)")
        if times and generated_at is not None and all(t < generated_at for t in times):
            self.info(path, 1, "I204", "no verification is current: each verified event is older than generated.at, so consumers read the concept as unverified (section 5.3)")

    def check_sources(self, path: Path, meta: dict) -> set[str]:
        ids: set[str] = set()
        shared_window = meta.get("usage_window")
        if not blank(shared_window):
            self.check_window(path, "usage_window", shared_window)
        for index, entry in enumerate(as_list(meta.get("sources"))):
            field = f"sources[{index}]"
            if not isinstance(entry, dict) or blank(entry.get("resource")):
                self.warn(path, 1, "W106", f"{field} needs a resource; consumers ignore it (section 5.1)")
                continue
            source_id = entry.get("id")
            if not blank(source_id):
                source_id = str(source_id)
                if source_id in ids:
                    self.warn(path, 1, "W107", f"{field}.id {source_id!r} is not unique (section 5.1)")
                ids.add(source_id)
            if not blank(entry.get("author")):
                self.check_actor(path, f"{field}.author", entry.get("author"))
            if not blank(entry.get("last_modified")):
                self.check_timestamp(path, f"{field}.last_modified", entry.get("last_modified"))
            if not blank(entry.get("usage_window")):
                self.check_window(path, f"{field}.usage_window", entry.get("usage_window"))
            if not blank(entry.get("usage_count")) and blank(shared_window) and blank(entry.get("usage_window")):
                self.warn(path, 1, "W109", f"{field}.usage_count needs a usage_window that gives its period (section 5.1)")
            resource = entry.get("resource")
            if isinstance(resource, str) and not re.search(r"\s", resource):
                self.check_path_field(path, f"{field}.resource", resource)
        return ids

    def check_window(self, path: Path, field: str, window: Any) -> None:
        if not isinstance(window, dict) or blank(window.get("from")) or blank(window.get("to")):
            self.warn(path, 1, "W101", f"{field} is a {{ from, to }} mapping of timestamps (section 5.1)")
            return
        self.check_timestamp(path, f"{field}.from", window.get("from"))
        self.check_timestamp(path, f"{field}.to", window.get("to"))

    def check_stale_after(self, path: Path, meta: dict) -> None:
        value = meta.get("stale_after")
        if blank(value):
            return
        moment = parse_timestamp(value)
        if moment is None:
            self.warn(path, 1, "W101", f"stale_after does not parse, so consumers never treat the concept as fresh (section 5.5); found {value!r}")
        elif self.now >= moment:
            self.info(path, 1, "I201", f"the concept is stale: stale_after {value} has passed (section 5.5)")

    def check_computation(self, path: Path, meta: dict, body: str) -> None:
        if blank(meta.get("runtime")):
            self.warn(path, 1, "W111", "an Attested Computation needs runtime (section 10.2)")
        fences = computation_fences(body)
        if not blank(meta.get("computation")):
            self.check_path_field(path, "computation", meta.get("computation"))
            if fences:
                self.warn(path, 1, "W112", "with a computation field, do not also put a fenced block in the Computation section (section 10.3)")
        elif fences == 0:
            self.warn(path, 1, "W112", "no computation: no computation field and no fenced block in a Computation section, so the concept is not attestable (section 10.3)")
        elif fences > 1:
            self.warn(path, 1, "W126", f"put exactly one fenced block in the Computation section; consumers use the first of {fences} (section 10.3)")
        for index, entry in enumerate(as_list(meta.get("parameters"))):
            if not isinstance(entry, dict) or blank(entry.get("name")) or blank(entry.get("type")):
                self.warn(path, 1, "W113", f"parameters[{index}] needs name and type (section 10.2)")
        for key in ("executor", "attester"):
            value = meta.get(key)
            if blank(value):
                continue
            if not isinstance(value, dict) or blank(value.get("resource")):
                self.warn(path, 1, "W114", f"{key} is a mapping with a resource field (section 10.2)")
                continue
            if key == "executor" and not isinstance(value.get("receipt"), list):
                self.warn(path, 1, "W114", "executor.receipt lists the fields that a run returns (section 10.2)")
            self.check_path_field(path, f"{key}.resource", value.get("resource"))
        if blank(meta.get("attester")):
            self.info(path, 1, "I205", "without an attester, consumers cannot show values from this computation as attested (section 10.2)")

    # ---- body (sections 5.1 and 6.1) ----------------------------------------

    def check_body(self, path: Path, body: str, body_line: int, source_ids: set[str]) -> None:
        reported: set[str] = set()
        for offset, line in prose_lines(body):
            number = body_line + offset
            for label in FOOTNOTE_RE.findall(line):
                if label not in source_ids and label not in reported:
                    reported.add(label)
                    self.warn(path, number, "W108", f"footnote [^{label}] has no sources entry with that id (section 5.1)")
            for target in LINK_RE.findall(line):
                if target.startswith("#"):
                    continue
                if self.resolve_path(path, target, field=False)[0] == "missing":
                    self.warn(path, number, "W115", f"link target {target!r} is not in the bundle (section 6.1)")

    # ---- value checks -------------------------------------------------------

    def check_actor(self, path: Path, field: str, value: Any) -> None:
        if not isinstance(value, str) or not ACTOR_RE.match(value):
            self.warn(path, 1, "W103", f"{field} is an actor: <producer>/<version> or <scheme>:<id>, such as human:<id> (section 7); found {value!r}")

    def check_timestamp(self, path: Path, field: str, value: Any) -> datetime | None:
        moment = parse_timestamp(value)
        if moment is None:
            self.warn(path, 1, "W101", f"{field} is an RFC 3339 date-time with an offset, such as 2026-06-30T14:00:00Z, or a date such as 2026-06-30 (section 5); found {value!r}")
        return moment

    def check_path_field(self, path: Path, field: str, value: Any) -> None:
        if not isinstance(value, str):
            return
        kind, _ = self.resolve_path(path, value, field=True)
        if kind == "missing":
            self.warn(path, 1, "W116", f"{field} {value!r} does not resolve to a file in the bundle (section 6.2)")
        elif kind == "fallback":
            self.warn(path, 1, "W119", f"{field} {value!r} resolves only from the bundle root, through the v0.2 fallback; write it as /{value} (section 6.2)")

    def resolve_path(self, source: Path, target: str, field: bool) -> tuple[str, Path | None]:
        """Resolve a link target or path field with the section 6 rules.

        Returns (kind, path). kind is "external" for a URL or a location
        outside the bundle root, "found", "fallback" for a bare path field
        that resolves only from the bundle root in a v0.2 bundle, or "missing".
        """
        if SCHEME_RE.match(target) or target.startswith("//"):
            return "external", None
        clean = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not clean:
            return "found", source
        base = self.bundle if clean.startswith("/") else source.parent
        candidate = Path(os.path.normpath(base / clean.lstrip("/")))
        if not self.inside(candidate):
            return "external", None
        if candidate.exists():
            return "found", candidate
        if field and self.root_fallback and not clean.startswith("/"):
            alternative = Path(os.path.normpath(self.bundle / clean))
            if self.inside(alternative) and alternative.exists():
                return "fallback", alternative
        return "missing", None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check an OKF v0.3 bundle for conformance and field shape.")
    parser.add_argument("bundle", type=Path, help="bundle root directory")
    parser.add_argument("--json", action="store_true", help="print findings as JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 when there are warnings")
    parser.add_argument("--now", help="current time as an RFC 3339 date-time, for staleness checks")
    args = parser.parse_args(argv)

    bundle = args.bundle.resolve()
    if not bundle.is_dir():
        print(f"validate.py: {args.bundle} is not a directory", file=sys.stderr)
        return 2
    now = datetime.now(timezone.utc)  # noqa: UP017 (datetime.UTC needs Python 3.11)
    if args.now:
        parsed = parse_timestamp(args.now)
        if parsed is None:
            print("validate.py: --now must be an RFC 3339 date-time with an offset", file=sys.stderr)
            return 2
        now = parsed

    checker = Checker(bundle, now)
    checker.run()
    counts = {level: sum(f.level == level for f in checker.findings) for level in ("error", "warning", "info")}

    if args.json:
        print(json.dumps({
            "bundle": str(bundle),
            "okf_version": checker.okf_version,
            "files_checked": checker.files_checked,
            "errors": counts["error"],
            "warnings": counts["warning"],
            "info": counts["info"],
            "findings": [asdict(f) for f in checker.findings],
        }, indent=2))
    else:
        for f in checker.findings:
            location = f"{f.path}:{f.line}" if f.line else f.path
            print(f"{location}: {f.level} {f.code} {f.message}")
        verdict = "conformant" if counts["error"] == 0 else "not conformant"
        print(f"{checker.files_checked} files checked: {counts['error']} errors, "
              f"{counts['warning']} warnings, {counts['info']} info. The bundle is {verdict}.")

    if counts["error"] or (args.strict and counts["warning"]):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
