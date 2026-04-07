#!/usr/bin/env python3
"""One-time script: parse the existing README.md into YAML data files."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_STARS = re.compile(r"github/stars/([^.]+?)\.svg")
RE_MD_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
RE_DOUBLE_LINK_GROUP = re.compile(
    r"\[\[[^\]]+\]\([^)]+\)(?:,\s*\[[^\]]+\]\([^)]+\))*\]"
)
RE_PAREN_LINK_GROUP = re.compile(
    r"\(\s*(?:\[[^\]]+\]\([^)]+\))(?:,\s*\[[^\]]+\]\([^)]+\))*\s*\)"
)


def extract_github_slug(text: str) -> str | None:
    badge = RE_STARS.search(text)
    if badge:
        return badge.group(1)
    match = re.search(r"github\.com/([^/]+/[^/)\s]+)", text)
    if match:
        return match.group(1).rstrip("/").split("?")[0].split("#")[0]
    return None


def extract_gitlab_slug(text: str) -> str | None:
    match = re.search(r"gitlab\.com/([^/]+/[^/)\s]+)", text)
    if match:
        return match.group(1).rstrip("/")
    return None


def extract_bitbucket_slug(text: str) -> str | None:
    match = re.search(r"bitbucket\.org/([^/]+/[^/)\s]+)", text)
    if match:
        return match.group(1).rstrip("/")
    return None


def split_html_lines(text: str) -> list[str]:
    items = [
        part.strip()
        for part in re.split(r"<br\s*/?>", text)
        if part.strip() and part.strip() != "(todo)"
    ]
    return items


def parse_primary_name_and_url(text: str) -> tuple[str, str | None, str]:
    if text.startswith("[") and not text.startswith("[["):
        match = RE_LINK.match(text)
        if match:
            name = match.group(1).strip()
            url = match.group(2).strip()
            rest = text[match.end():].strip()
            return name, url, rest
    name = text
    for marker in (" [[", " ([", " - "):
        index = name.find(marker)
        if index != -1:
            return name[:index].strip(), None, name[index:].strip()
    return name.strip(), None, ""


def extract_repo_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    github = extract_github_slug(text)
    if github:
        fields["github"] = github
    gitlab = extract_gitlab_slug(text)
    if gitlab:
        fields["gitlab"] = gitlab
    bitbucket = extract_bitbucket_slug(text)
    if bitbucket:
        fields["bitbucket"] = bitbucket
    if not fields:
        matches = RE_MD_LINK.findall(text)
        if matches:
            label, url = matches[0]
            if label.lower() == "code":
                fields["code_url"] = url
    badge_github = RE_STARS.search(text)
    if badge_github:
        fields["badge_github"] = badge_github.group(1)
    return fields


def extract_grouped_links(text: str) -> tuple[str, list[dict[str, str]]]:
    links: list[dict[str, str]] = []

    def _replace(match: re.Match[str]) -> str:
        for label, url in RE_MD_LINK.findall(match.group(0)):
            links.append({"label": label.strip("[]"), "url": url})
        return ""

    cleaned = RE_DOUBLE_LINK_GROUP.sub(_replace, text)
    cleaned = RE_PAREN_LINK_GROUP.sub(_replace, cleaned)
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip(), links


def find_block(lines: list[str], start: str, end: str | None) -> list[str]:
    start_idx = None
    end_idx = len(lines)
    for idx, line in enumerate(lines):
        if line.startswith(start):
            start_idx = idx + 1
            break
    if start_idx is None:
        return []
    if end:
        for idx in range(start_idx, len(lines)):
            if lines[idx].startswith(end):
                end_idx = idx
                break
    return lines[start_idx:end_idx]


def parse_active_libraries(lines: list[str]) -> list[dict]:
    entries: list[dict] = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("| Name |"):
            in_table = True
            continue
        if not in_table or not stripped.startswith("|"):
            continue
        if stripped.startswith("|:----:|"):
            continue
        cells = [cell.strip() for cell in stripped.split("|")[1:-1]]
        if len(cells) != 7:
            continue

        name, url, _ = parse_primary_name_and_url(cells[0])
        entry: dict = {"name": name, "_subsection": "Active"}
        if url:
            entry["url"] = url
        shapes = split_html_lines(cells[1])
        features = split_html_lines(cells[2])
        languages = [item.strip() for item in cells[3].split(",") if item.strip() and item.strip() != "(todo)"]
        if shapes:
            entry["shapes"] = shapes
        if features:
            entry["features"] = features
        if languages:
            entry["languages"] = languages
        if cells[4] and cells[4] != "(todo)":
            entry["license"] = cells[4]
        entry.update(extract_repo_fields(cells[5]))
        badge_fields = extract_repo_fields(cells[6])
        if "badge_github" in badge_fields:
            entry["badge_github"] = badge_fields["badge_github"]
        entries.append(entry)
    return entries


def parse_simple_bullet(line: str) -> dict | None:
    stripped = line.strip()
    if not stripped.startswith("* "):
        return None
    body = stripped[2:].strip()
    body_without_groups, _ = extract_grouped_links(body)
    name, url, rest = parse_primary_name_and_url(body_without_groups)
    entry: dict = {"name": name}
    if url:
        entry["url"] = url
    entry.update(extract_repo_fields(body))

    description = ""
    if " - " in body:
        description = body.split(" - ", 1)[1].strip()
    elif rest:
        cleaned = rest.strip()
        if cleaned:
            description = cleaned.lstrip("- ").strip()
    if description:
        entry["description"] = description
    return entry


def parse_libraries_section(lines: list[str]) -> tuple[list[dict], list[dict]]:
    active = parse_active_libraries(lines)
    inactive: list[dict] = []
    mesh: list[dict] = []

    mode = ""
    for line in lines:
        stripped = line.strip()
        if stripped == "**Inactive**":
            mode = "inactive"
            continue
        if stripped == "### Mesh Processing":
            mode = "mesh"
            continue
        if not stripped.startswith("* "):
            continue
        entry = parse_simple_bullet(stripped)
        if not entry:
            continue
        if mode == "inactive":
            entry["_subsection"] = "Inactive"
            inactive.append(entry)
        elif mode == "mesh":
            mesh.append(entry)
    return active + inactive, mesh


def parse_resource_line(line: str, *, section: str) -> dict:
    indent = (len(line) - len(line.lstrip(" "))) // 2
    body = line.strip()[2:].strip()
    body_without_groups, grouped_links = extract_grouped_links(body)
    entry: dict = {}
    entry["_indent"] = indent

    if section == "books" and "," in body_without_groups and not body_without_groups.startswith("["):
        head = body_without_groups
        title, _, tail = head.partition(",")
        entry["name"] = title.strip()
        if tail.strip():
            entry["description"] = f", {tail.strip()}"
    else:
        name, url, rest = parse_primary_name_and_url(body_without_groups)
        entry["name"] = name
        if url:
            entry["url"] = url
        cleaned = rest.strip()
        if cleaned.startswith("- "):
            cleaned = f"- {cleaned[2:].strip()}"
        if cleaned and cleaned != name:
            entry["description"] = cleaned

    if grouped_links:
        entry["links"] = grouped_links
    return entry


def parse_grouped_resources(lines: list[str], *, section: str) -> list[dict]:
    entries: list[dict] = []
    subsection = ""
    last_entry: dict | None = None
    current_header: dict | None = None
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#### "):
            subsection = stripped[5:].strip()
            last_entry = None
            current_header = None
            continue
        if not stripped.startswith("* "):
            continue

        indent = (len(line) - len(line.lstrip(" "))) // 2
        if indent > 0 and section == "articles" and current_header is not None:
            child = parse_resource_line(line, section=section)
            child["_subsection"] = subsection
            entries.append(child)
            last_entry = child
            continue
        if indent > 0 and last_entry is not None:
            notes = last_entry.setdefault("notes", [])
            notes.append(stripped[2:].strip())
            continue

        body = stripped[2:].strip()
        if section == "articles" and not body.startswith("[") and " - " not in body and "[[" not in body and "([" not in body and "http" not in body:
            entry = {"name": body, "_subsection": subsection, "_type": "header"}
            current_header = entry
        else:
            entry = parse_resource_line(line, section=section)
            entry["_subsection"] = subsection
            if entry.get("_indent") == 0:
                entry.pop("_indent", None)
            if indent == 0:
                current_header = None
        entries.append(entry)
        last_entry = entry
    return entries


def parse_books(lines: list[str]) -> list[dict]:
    entries: list[dict] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("* "):
            continue
        entry = parse_resource_line(line, section="books")
        entry.pop("_indent", None)
        entries.append(entry)
    return entries


def parse_other_lists(lines: list[str]) -> list[dict]:
    entries: list[dict] = []
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("* "):
            continue
        entry = parse_simple_bullet(line)
        if entry:
            entries.append(entry)
    return entries


def dump_yaml(path: Path, entries: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        yaml.dump(
            entries,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=120,
        )


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    readme_lines = (root / "README.md").read_text(encoding="utf-8").splitlines()

    libraries_block = find_block(readme_lines, "## [Libraries]", "## [Papers]")
    papers_block = find_block(readme_lines, "## [Papers]", "## [Books]")
    books_block = find_block(readme_lines, "## [Books]", "## [Articles]")
    articles_block = find_block(readme_lines, "## [Articles]", "## [Other Awesome Lists]")
    other_lists_block = find_block(readme_lines, "## [Other Awesome Lists]", "## [Contributing]")

    libraries, mesh_processing = parse_libraries_section(libraries_block)
    papers = parse_grouped_resources(papers_block, section="papers")
    books = parse_books(books_block)
    articles = parse_grouped_resources(articles_block, section="articles")
    other_lists = parse_other_lists(other_lists_block)

    data_dir = root / "data"
    dump_yaml(data_dir / "libraries.yaml", libraries)
    dump_yaml(data_dir / "mesh-processing.yaml", mesh_processing)
    dump_yaml(data_dir / "papers.yaml", papers)
    dump_yaml(data_dir / "books.yaml", books)
    dump_yaml(data_dir / "articles.yaml", articles)
    dump_yaml(data_dir / "other-awesome-lists.yaml", other_lists)

    print("Wrote data/*.yaml from README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
