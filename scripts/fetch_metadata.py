#!/usr/bin/env python3
"""Fetch GitHub metadata for all entries in data/*.yaml and update _meta fields."""

from __future__ import annotations

import os
import sys
import time
import urllib.error
import urllib.parse
from datetime import date
from pathlib import Path

import yaml

try:
    from scripts.generate_readme import MANUAL_REVIEW
    from scripts.github_metadata import fetch_default_branch_commit_date, fetch_json
except ModuleNotFoundError:
    from generate_readme import MANUAL_REVIEW
    from github_metadata import fetch_default_branch_commit_date, fetch_json

RATE_LIMIT_PAUSE = 2  # seconds between requests to avoid abuse detection
USER_AGENT = "awesome-collision-detection-metadata-bot"
GONE = "gone"
GONE_GRACE_DAYS = 7  # removed when still gone on the next weekly refresh


def fetch_repo_metadata(owner_repo: str) -> tuple[dict, str] | str | None:
    """Return (_meta, current owner/repo), GONE for a deleted repository, or None on errors.

    The API follows repository renames. Looked up by owner/repo, not the stored ID, so a
    corrected `github` link takes effect and refreshes the ID.
    """
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        data = fetch_json(
            f"https://api.github.com/repos/{owner_repo}",
            token,
            USER_AGENT,
        )
    except urllib.error.HTTPError as e:
        if e.code in (404, 451):
            print(f"  WARN: {owner_repo} - HTTP {e.code}", file=sys.stderr)
            return GONE
        if e.code == 403:
            print(f"  WARN: {owner_repo} — 403 rate limited", file=sys.stderr)
        else:
            print(f"  WARN: {owner_repo} — HTTP {e.code}", file=sys.stderr)
        return None
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"  WARN: {owner_repo} — {e}", file=sys.stderr)
        return None

    # The repository ID survives renames and transfers, so suggestion triage matches it exactly.
    meta: dict = {"id": data["id"]} if "id" in data else {}
    full_name = data.get("full_name") or owner_repo
    last_commit = None
    if "stargazers_count" in data:
        meta["stars"] = data["stargazers_count"]
    default_branch = data.get("default_branch") or ""
    if default_branch:
        try:
            last_commit = fetch_default_branch_commit_date(
                full_name, default_branch, token, USER_AGENT
            )
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) or e.code >= 500:
                meta["_commit_lookup_failed"] = True
            print(
                f"  WARN: {owner_repo} - commit lookup HTTP {e.code}",
                file=sys.stderr,
            )
        except (urllib.error.URLError, TimeoutError) as e:
            meta["_commit_lookup_failed"] = True
            print(
                f"  WARN: {owner_repo} - commit lookup failed ({e})",
                file=sys.stderr,
            )
    # No pushed_at fallback: it counts pushes to any branch, not default-branch commits.
    if last_commit:
        meta["last_commit"] = last_commit
    if data.get("archived") is True:
        meta["archived"] = True
    if data.get("license"):
        license_data = data["license"]
        spdx = license_data.get("spdx_id")
        if spdx and spdx != "NOASSERTION":
            meta["license"] = spdx
        elif license_data.get("name"):
            meta["license"] = license_data["name"]
    if data.get("language"):
        meta["language"] = data["language"]
    return meta, full_name


def in_repository(url: str, slug: str) -> bool:
    """Whether a URL points into a GitHub repository, however written (scheme, www., query,
    fragment, .git)."""
    parts = urllib.parse.urlsplit((url or "").strip())
    path = parts.path.lower().removesuffix(".git").rstrip("/")
    root = "/" + slug.lower()
    return (parts.hostname or "").removeprefix("www.") == "github.com" and (path == root or path.startswith(root + "/"))


def process_yaml_file(yaml_path: Path, dry_run: bool = False, today: date | None = None) -> tuple[int, int]:
    with open(yaml_path, encoding="utf-8") as f:
        entries = yaml.safe_load(f)
    if not isinstance(entries, list):
        return 0, 0

    today = today or date.today()
    updated = 0
    total = 0
    kept = []
    for entry in entries:
        kept.append(entry)
        github = entry.get("github")
        if not github:
            continue
        total += 1
        print(f"  {github}...", end=" ", flush=True)

        previous = entry.get("_meta") or {}
        fetched = fetch_repo_metadata(github)
        if fetched == GONE:
            # Mark on the first miss; drop on a later refresh, so the PR proposes the removal.
            meta = entry.setdefault("_meta", {})
            since = meta.get("gone_since")
            if since and (today - date.fromisoformat(str(since))).days >= GONE_GRACE_DAYS:
                links = entry.get("links") or []
                other_links = [link for link in links if not in_repository(link.get("url", ""), github)]
                own_url = entry.get("url") or ""
                if yaml_path.stem in MANUAL_REVIEW and ((own_url and not in_repository(own_url, github)) or other_links):
                    # A paper or book outlives its code: drop every link into the dead repository and
                    # keep the entry. One whose only home was that repository goes with it, like software.
                    for key in ("github", "badge_github", "_meta"):
                        entry.pop(key, None)
                    if own_url and in_repository(own_url, github):
                        entry.pop("url")
                    if len(other_links) < len(links):
                        entry["links"] = other_links
                    print(f"repository gone since {since}; links to it removed")
                else:
                    kept.pop()
                    print(f"removed (gone since {since})")
            else:
                meta.setdefault("gone_since", today.isoformat())
                print("gone")
            updated += 1
        elif fetched:
            meta, full_name = fetched
            # Only transient failures for the same repository retain the last known commit date.
            commit_lookup_failed = meta.pop("_commit_lookup_failed", False)
            if (commit_lookup_failed and previous.get("last_commit")
                    and meta.get("id") is not None and previous.get("id") == meta["id"]):
                meta["last_commit"] = previous["last_commit"]
            entry["_meta"] = meta
            if full_name.lower() != github.lower():
                print(f"(renamed to {full_name})", end=" ")
                entry["github"] = full_name
            updated += 1
            stars = meta.get("stars", "?")
            print(f"★ {stars}")
        else:
            print("skipped")

        time.sleep(RATE_LIMIT_PAUSE)

    if not dry_run and updated > 0:
        with open(yaml_path, "w", encoding="utf-8") as f:
            yaml.dump(
                kept,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120,
            )

    return total, updated


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Fetch GitHub metadata for YAML entries"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Print metadata without writing"
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"

    if not data_dir.exists():
        print(f"ERROR: {data_dir} not found", file=sys.stderr)
        sys.exit(1)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        print("WARNING: No GITHUB_TOKEN set — rate limit is 60 req/hr", file=sys.stderr)

    yaml_files = sorted(data_dir.glob("*.yaml"))
    grand_total = 0
    grand_updated = 0

    for yaml_file in yaml_files:
        print(f"\n{yaml_file.name}:")
        total, updated = process_yaml_file(yaml_file, dry_run=args.dry_run)
        grand_total += total
        grand_updated += updated

    print(f"\nDone: {grand_updated}/{grand_total} entries updated")
    if args.dry_run:
        print("(dry run — no files written)")
    elif grand_updated:
        # Reference date for README activity badges (see generate_readme.py).
        (data_dir / "as-of.txt").write_text(f"{date.today().isoformat()}\n", encoding="utf-8")


if __name__ == "__main__":
    main()
