#!/usr/bin/env python3
"""Evaluate a GitHub repository against the inclusion criteria.

Usage:
    python3 scripts/evaluate_entry.py owner/repo
    python3 scripts/evaluate_entry.py --json owner/repo
    python3 scripts/evaluate_entry.py --data-dir data/ owner/repo

Exit codes:
    0 = accept, 1 = incubator, 2 = reject, 3 = manual review/error
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
from datetime import date
from pathlib import Path

import yaml

try:
    from scripts.github_metadata import (
        API_BASE,
        fetch_default_branch_commit_date,
        fetch_json,
    )
except ModuleNotFoundError:
    from github_metadata import API_BASE, fetch_default_branch_commit_date, fetch_json

GUIDANCE = {
    "popularity": (
        "The project has fewer than 50 GitHub stars. "
        "This threshold helps ensure community adoption. "
        "As the project gains traction, it will automatically qualify."
    ),
    "activity": (
        "No commits detected on the default branch in the last 2 years. "
        "We look for signs of active maintenance."
    ),
    "documentation": (
        "We could not find a README file. "
        "A README with examples or API docs makes the project much easier to evaluate."
    ),
    "maturity": (
        "The project is less than 6 months old. "
        "We wait for projects to stabilize before listing them."
    ),
}
USER_AGENT = "awesome-collision-detection-evaluator"
MANUAL_CHECKS = {"uniqueness"}


def _fetch_json(url: str, token: str | None = None) -> dict | list | None:
    try:
        return fetch_json(url, token, USER_AGENT)
    except urllib.error.HTTPError as e:
        print(f"ERROR: HTTP {e.code} for {url}", file=sys.stderr)
        return None
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"ERROR: {e} for {url}", file=sys.stderr)
        return None


def fetch_readme_status(owner_repo: str, token: str | None = None) -> tuple[bool | None, str]:
    url = f"{API_BASE}/repos/{owner_repo}/readme"
    try:
        readme_data = fetch_json(url, token, USER_AGENT)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False, "no README"
        print(f"ERROR: HTTP {e.code} for {url}", file=sys.stderr)
        return None, "README status unknown (fetch failed)"
    except (urllib.error.URLError, TimeoutError) as e:
        print(f"ERROR: {e} for {url}", file=sys.stderr)
        return None, "README status unknown (fetch failed)"

    has_readme = isinstance(readme_data, dict) and "content" in readme_data
    return has_readme, "README found" if has_readme else "no README"


def find_duplicates(owner_repo: str, data_dir: Path) -> list[dict]:
    slug = owner_repo.lower()
    matches = []
    for yaml_path in sorted(data_dir.glob("*.yaml")):
        with yaml_path.open(encoding="utf-8") as f:
            entries = yaml.safe_load(f)
        if not isinstance(entries, list):
            continue
        for entry in entries:
            if entry.get("github", "").lower() == slug:
                matches.append(
                    {
                        "name": entry.get("name", ""),
                        "file": yaml_path.name,
                        "section": yaml_path.stem,
                    }
                )
    return matches


def evaluate(
    owner_repo: str,
    token: str | None = None,
    data_dir: Path | None = None,
) -> dict:
    result_base = {"repo": owner_repo}

    duplicates = []
    if data_dir and data_dir.exists():
        duplicates = find_duplicates(owner_repo, data_dir)
    if duplicates:
        entry = duplicates[0]
        return {
            **result_base,
            "duplicate": True,
            "duplicate_of": entry["name"],
            "duplicate_section": entry["section"],
            "recommendation": "duplicate",
            "reason": f'Already listed as "{entry["name"]}" in {entry["file"]}',
        }

    data = _fetch_json(f"{API_BASE}/repos/{owner_repo}", token)
    if data is None:
        return {
            **result_base,
            "error": "Could not fetch repository data",
            "recommendation": "error",
        }
    if data.get("message") == "Not Found":
        return {
            **result_base,
            "error": "Repository not found",
            "recommendation": "error",
        }

    today = date.today()
    stars = data.get("stargazers_count", 0)
    archived = data.get("archived", False)
    created_at = data.get("created_at", "")[:10]
    pushed_at = data.get("pushed_at", "")[:10]
    default_branch = data.get("default_branch") or ""
    last_commit = None
    if default_branch:
        try:
            last_commit = fetch_default_branch_commit_date(
                owner_repo, default_branch, token, USER_AGENT
            )
        except urllib.error.HTTPError as e:
            print(
                f"ERROR: HTTP {e.code} for {API_BASE}/repos/{owner_repo}/commits",
                file=sys.stderr,
            )
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"ERROR: {e} for {API_BASE}/repos/{owner_repo}/commits", file=sys.stderr)
    if not last_commit:
        last_commit = pushed_at

    license_spdx = None
    if (
        data.get("license")
        and data["license"].get("spdx_id", "NOASSERTION") != "NOASSERTION"
    ):
        license_spdx = data["license"]["spdx_id"]
    description = data.get("description") or ""
    has_homepage = bool(data.get("homepage"))
    homepage_url = data.get("homepage") or ""
    language = data.get("language") or ""

    has_readme, readme_detail = fetch_readme_status(owner_repo, token)

    checks: dict[str, dict] = {}
    checks["popularity"] = {
        "pass": stars >= 50,
        "detail": f"{stars} stars (threshold: 50)",
    }

    active = False
    if last_commit:
        try:
            latest_commit = date.fromisoformat(last_commit)
            active = (today - latest_commit).days <= 730
        except ValueError:
            pass
    checks["activity"] = {
        "pass": active and not archived,
        "detail": f"last default-branch commit {last_commit or 'unknown'}"
        + (" ⚠️ ARCHIVED" if archived else ""),
    }

    checks["documentation"] = {
        "pass": has_readme,
        "detail": readme_detail,
    }

    mature = False
    age_days = 0
    if created_at:
        try:
            created = date.fromisoformat(created_at)
            age_days = (today - created).days
            mature = age_days >= 180
        except ValueError:
            pass
    checks["maturity"] = {
        "pass": mature,
        "detail": f"created {created_at}" + (f" ({age_days} days ago)" if created_at else ""),
    }

    checks["uniqueness"] = {
        "pass": None,
        "detail": "requires manual review",
    }

    auto_checks = {name: check for name, check in checks.items() if name not in MANUAL_CHECKS}
    auto_score = sum(1 for check in auto_checks.values() if check["pass"] is True)
    auto_total = len(auto_checks)
    failed_checks = [name for name, check in checks.items() if check["pass"] is False]
    unknown_checks = [name for name, check in auto_checks.items() if check["pass"] is None]

    if archived:
        recommendation = "reject"
        reason = "Repository is archived"
    elif unknown_checks:
        recommendation = "needs_review"
        reason = (
            "Could not complete auto-checkable criteria "
            f"({', '.join(unknown_checks)}); maintainer review is required before acceptance"
        )
    elif auto_score >= 3:
        recommendation = "accept"
        reason = (
            f"Passes {auto_score}/{auto_total} auto-checkable criteria "
            "(uniqueness needs manual review)"
        )
    elif auto_score >= 2:
        recommendation = "likely_accept"
        reason = (
            f"Passes {auto_score}/{auto_total} auto-checkable criteria; "
            "if uniqueness is confirmed, meets ≥ 3 threshold"
        )
    elif auto_score >= 1:
        recommendation = "incubator"
        reason = f"Passes {auto_score}/{auto_total} auto-checkable criteria; needs to mature"
    else:
        recommendation = "reject"
        reason = f"Passes {auto_score}/{auto_total} auto-checkable criteria"

    meta = {"stars": stars}
    if last_commit:
        meta["last_commit"] = last_commit
    if archived:
        meta["archived"] = True
    if license_spdx:
        meta["license"] = license_spdx
    if language:
        meta["language"] = language

    return {
        **result_base,
        "description": description,
        "homepage": homepage_url,
        "has_homepage": has_homepage,
        "language": language,
        "stars": stars,
        "created_at": created_at,
        "last_commit": last_commit,
        "archived": archived,
        "has_readme": has_readme,
        "license": license_spdx,
        "checks": checks,
        "auto_score": auto_score,
        "auto_total": auto_total,
        "failed_checks": failed_checks,
        "unknown_checks": unknown_checks,
        "recommendation": recommendation,
        "reason": reason,
        "meta": meta,
    }


def render_report(result: dict) -> str:
    if result.get("recommendation") == "error":
        return (
            f"## ⚠️ Evaluation failed: {result['repo']}\n\n"
            f"{result.get('error', 'Unknown error')}\n"
        )

    if result.get("recommendation") == "duplicate":
        return "\n".join(
            [
                f"## 📋 Duplicate suggestion: {result['repo']}",
                "",
                f'This repository is already listed as **{result["duplicate_of"]}** '
                f'in `{result["duplicate_section"]}`.',
                "",
                f'Reason: {result["reason"]}',
            ]
        )

    lines = [
        f"## 👋 Evaluation: {result['repo']}",
        "",
        "Thanks for suggesting this project! Here's our automated evaluation:",
        "",
    ]
    if result.get("description"):
        lines.append(f"> {result['description']}")
        lines.append("")

    if result.get("has_readme") is True:
        readme_display = "✅"
    elif result.get("has_readme") is False:
        readme_display = "❌"
    else:
        readme_display = "Unknown"

    lines.extend(
        [
            "### Repository Info",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| Stars | {result.get('stars', 0)} |",
            f"| Created | {result.get('created_at', 'unknown')} |",
            f"| Last Commit (default branch) | {result.get('last_commit', 'unknown')} |",
            f"| Archived | {'Yes' if result.get('archived') else 'No'} |",
            f"| README | {readme_display} |",
            f"| License | {'✅ ' + result['license'] if result.get('license') else '❌'} |",
            f"| Homepage | {'✅' if result.get('has_homepage') else '❌'} |",
            "",
            "### Scoring Checklist",
            "",
        ]
    )

    for key in ["popularity", "activity", "documentation", "maturity", "uniqueness"]:
        check = result["checks"][key]
        if check["pass"] is True:
            prefix = "✅"
        elif check["pass"] is False:
            prefix = "❌"
        else:
            prefix = "🔍"
        lines.append(f"- {prefix} **{key.capitalize()}**: {check['detail']}")

    rec_map = {
        "accept": "🟢 Accept",
        "likely_accept": "🟢 Likely Accept",
        "needs_review": "⚠️ Needs Review",
        "incubator": "🟡 Incubator",
        "reject": "🔴 Reject",
    }
    lines.extend(
        [
            "",
            f"**Auto-score**: {result['auto_score']}/{result['auto_total']} (excludes manual checks)",
            "",
            f"### Recommendation: {rec_map.get(result['recommendation'], result['recommendation'])}",
            "",
            result["reason"],
        ]
    )

    if result.get("failed_checks"):
        lines.extend(["", "### What would help"])
        for name in result["failed_checks"]:
            guidance = GUIDANCE.get(name)
            if guidance:
                lines.extend(["", f"**{name.capitalize()}**", guidance])

    if result.get("unknown_checks"):
        lines.extend(["", "### Needs manual review"])
        for name in result["unknown_checks"]:
            detail = result["checks"].get(name, {}).get("detail", "status unknown")
            lines.extend(["", f"**{name.capitalize()}**", detail])

    lines.extend(
        [
            "",
            "---",
            "*🤖 Auto-evaluated by [evaluate_entry.py](../scripts/evaluate_entry.py). "
            "Uniqueness and relevance require manual review by a maintainer.*",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate a GitHub repo for inclusion")
    parser.add_argument("repo", help="GitHub owner/repo slug")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--data-dir", type=Path, default=None, help="data/ directory for duplicate detection")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    result = evaluate(args.repo, token=token, data_dir=args.data_dir)

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(render_report(result))

    recommendation = result.get("recommendation")
    if recommendation == "accept":
        return 0
    if recommendation == "incubator":
        return 1
    if recommendation in {"reject", "duplicate"}:
        return 2
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
