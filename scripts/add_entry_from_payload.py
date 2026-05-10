#!/usr/bin/env python3
"""Add an entry to the appropriate data file from a JSON payload."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
import urllib.error
from urllib.parse import urlparse

import yaml

try:
    from scripts.github_metadata import fetch_default_branch_commit_date, fetch_json
except ModuleNotFoundError:
    from github_metadata import fetch_default_branch_commit_date, fetch_json

USER_AGENT = "awesome-collision-detection-bot"
ISSUE_FORM_EMPTY_VALUES = {"_no response_"}


def clean_issue_form_value(value: object) -> str:
    if not isinstance(value, str):
        return ""
    value = value.strip()
    return "" if value.lower() in ISSUE_FORM_EMPTY_VALUES else value


def split_csv(value: str) -> list[str]:
    value = clean_issue_form_value(value)
    return [
        item.strip()
        for item in value.replace("\n", ",").split(",")
        if item.strip() and item.strip().lower() not in {"not applicable", "n/a"}
    ]


def parse_links(value: str) -> list[dict]:
    links = []
    value = clean_issue_form_value(value)
    for raw in value.splitlines():
        raw = raw.strip().lstrip("-*").strip()
        if not raw:
            continue
        if raw.startswith(("http://", "https://")):
            links.append({"label": "link", "url": raw})
            continue
        if ":" in raw:
            label, url = raw.split(":", 1)
            if url.strip().startswith(("http://", "https://")):
                links.append({"label": label.strip(), "url": url.strip()})
    return links


def apply_repo_fields(entry: dict, github_repo: str, alternative_repo: str) -> None:
    if github_repo:
        entry["github"] = github_repo
        return
    if not alternative_repo:
        return
    parsed = urlparse(alternative_repo.strip())
    host = parsed.netloc.lower()
    path = parsed.path.strip("/")
    if host == "gitlab.com" and path:
        entry["gitlab"] = path
    elif host == "bitbucket.org" and path:
        entry["bitbucket"] = path
    else:
        entry["code_url"] = alternative_repo.strip()


def add_repo_link_if_needed(links: list[dict], payload: dict) -> list[dict]:
    github_repo = payload.get("github_repo", "")
    alternative_repo = payload.get("alternative_repo", "").strip()
    urls = {link["url"] for link in links}
    if github_repo:
        repo_url = f"https://github.com/{github_repo}"
        if repo_url not in urls:
            links.append({"label": "code", "url": repo_url})
    elif alternative_repo and alternative_repo not in urls:
        parsed = urlparse(alternative_repo)
        label = "repo"
        if parsed.netloc.lower() == "gitlab.com":
            label = "gitlab"
        elif parsed.netloc.lower() == "bitbucket.org":
            label = "bitbucket"
        links.append({"label": label, "url": alternative_repo})
    return links


def fetch_meta(github_repo: str) -> tuple[dict, str | None, str | None]:
    if not github_repo:
        return {}, None, None
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    try:
        data = fetch_json(
            f"https://api.github.com/repos/{github_repo}",
            token,
            USER_AGENT,
        )
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        print(f"WARN: Could not fetch metadata for {github_repo}: {exc}", file=sys.stderr)
        return {}, None, None
    if not isinstance(data, dict):
        return {}, None, None

    meta = {}
    if "stargazers_count" in data:
        meta["stars"] = data["stargazers_count"]
    last_commit = None
    default_branch = data.get("default_branch") or ""
    if default_branch:
        try:
            last_commit = fetch_default_branch_commit_date(
                github_repo,
                default_branch,
                token,
                USER_AGENT,
            )
        except Exception:
            last_commit = None
    if not last_commit and data.get("pushed_at"):
        last_commit = data["pushed_at"][:10]
    if last_commit:
        meta["last_commit"] = last_commit
    if data.get("archived"):
        meta["archived"] = True

    license_text = None
    if data.get("license"):
        license_data = data["license"]
        spdx = license_data.get("spdx_id")
        if spdx and spdx != "NOASSERTION":
            license_text = spdx
            meta["license"] = spdx
        elif license_data.get("name"):
            license_text = license_data["name"]
            meta["license"] = license_text

    language_text = data.get("language") or None
    if language_text:
        meta["language"] = language_text
    return meta, license_text, language_text


def insert_entry(entries: list[dict], entry: dict, yaml_file: str) -> list[dict]:
    if yaml_file == "libraries":
        subsection_order = {"Active": 0, "Inactive": 1}
        entries.append(entry)
        entries.sort(
            key=lambda item: (
                subsection_order.get(item.get("_subsection", ""), 99),
                item["name"].lower(),
            )
        )
        return entries

    if yaml_file in {"mesh-processing", "other-awesome-lists"}:
        entries.append(entry)
        entries.sort(key=lambda item: item["name"].lower())
        return entries

    if yaml_file in {"papers", "articles"}:
        subsection = entry.get("_subsection", "")
        insert_at = None
        for index, existing in enumerate(entries):
            if existing.get("_subsection", "") == subsection:
                insert_at = index + 1
        if insert_at is None:
            entries.append(entry)
        else:
            entries.insert(insert_at, entry)
        return entries

    entries.append(entry)
    return entries


def build_entry(payload: dict) -> dict:
    entry = {"name": payload["name"]}
    url = clean_issue_form_value(payload.get("url", ""))
    if url:
        entry["url"] = url

    github_repo = clean_issue_form_value(payload.get("github_repo", ""))
    alternative_repo = clean_issue_form_value(payload.get("alternative_repo", ""))
    apply_repo_fields(entry, github_repo, alternative_repo)
    meta, meta_license, meta_language = fetch_meta(github_repo)
    if meta:
        entry["_meta"] = meta

    category = payload["category"]
    description = clean_issue_form_value(payload.get("description", ""))
    if category == "Libraries":
        library_status = clean_issue_form_value(payload.get("library_status", ""))
        subsection = "Inactive" if library_status == "Inactive" else "Active"
        entry["_subsection"] = subsection
        shapes = split_csv(payload.get("shapes", ""))
        features = split_csv(payload.get("features", ""))
        languages = split_csv(payload.get("languages", ""))
        if shapes:
            entry["shapes"] = shapes
        if features:
            entry["features"] = features
        if languages:
            entry["languages"] = languages
        elif meta_language:
            entry["languages"] = [meta_language]
        license_text = clean_issue_form_value(payload.get("license", ""))
        if license_text:
            entry["license"] = license_text
        elif meta_license:
            entry["license"] = meta_license
        if description:
            entry["description"] = description
    elif category == "Mesh Processing":
        if description:
            entry["description"] = description
    elif category in {"Papers", "Books", "Articles"}:
        subsection = clean_issue_form_value(payload.get("subsection", ""))
        if subsection and category in {"Papers", "Articles"}:
            entry["_subsection"] = subsection
        elif category in {"Papers", "Articles"}:
            entry["_subsection"] = "Other"
        if description:
            entry["description"] = description
        links = parse_links(payload.get("additional_links", ""))
        links = add_repo_link_if_needed(
            links,
            {
                **payload,
                "github_repo": github_repo,
                "alternative_repo": alternative_repo,
            },
        )
        if links:
            entry["links"] = links
    elif category == "Other Awesome Lists":
        if description:
            entry["description"] = description

    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description="Add an entry from a JSON payload")
    parser.add_argument("payload_json", help="Path to the payload JSON file")
    args = parser.parse_args()

    payload_path = Path(args.payload_json)
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    yaml_file = payload["yaml_file"]
    yaml_path = Path(__file__).resolve().parent.parent / "data" / f"{yaml_file}.yaml"
    if not yaml_path.exists():
        print(f"ERROR: {yaml_path} not found", file=sys.stderr)
        return 1

    with yaml_path.open(encoding="utf-8") as f:
        entries = yaml.safe_load(f) or []

    entry = build_entry(payload)
    entries = insert_entry(entries, entry, yaml_file)

    with yaml_path.open("w", encoding="utf-8") as f:
        yaml.dump(
            entries,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )

    print(f"Updated {yaml_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
