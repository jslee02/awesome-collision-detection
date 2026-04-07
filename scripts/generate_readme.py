#!/usr/bin/env python3
"""Generate README.md from structured YAML data."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def load_yaml(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else []


def code_link(entry: dict) -> tuple[str, str] | None:
    if entry.get("github"):
        return ("github", f"https://github.com/{entry['github']}")
    if entry.get("gitlab"):
        return ("gitlab", f"https://gitlab.com/{entry['gitlab']}")
    if entry.get("bitbucket"):
        return ("bitbucket", f"https://bitbucket.org/{entry['bitbucket']}")
    if entry.get("code_url"):
        return ("code", str(entry["code_url"]))
    return None


def popularity_badge(entry: dict) -> str:
    slug = entry.get("badge_github") or entry.get("github")
    if not slug:
        return ""
    alt = slug.split("/")[-1]
    return (
        f"![{alt}]"
        f"(https://img.shields.io/github/stars/{slug}.svg?style=social&label=Star&maxAge=2592000)"
    )


def render_name(entry: dict) -> str:
    name = entry.get("name", "")
    url = entry.get("url")
    return f"[{name}]({url})" if url else name


def render_active_library_row(entry: dict) -> str:
    shapes = "<br/>".join(entry.get("shapes") or []) or "(todo)"
    features = "<br/>".join(entry.get("features") or []) or "(todo)"
    languages = ", ".join(entry.get("languages") or []) or "(todo)"
    license_text = entry.get("license") or (entry.get("_meta") or {}).get("license") or "(todo)"
    code = code_link(entry)
    code_text = f"[{code[0]}]({code[1]})" if code else ""
    popularity = popularity_badge(entry)
    return (
        f"| {render_name(entry)} | {shapes} | {features} | {languages} | "
        f"{license_text} | {code_text} | {popularity} |"
    )


def render_repo_ref(entry: dict, *, include_badge: bool = False) -> str:
    code = code_link(entry)
    if not code:
        return ""

    if include_badge:
        badge = popularity_badge(entry)
        if badge:
            return f" ([{code[0]}]({code[1]}) {badge})"
        return f" ([{code[0]}]({code[1]}))"

    return f" [[{code[0]}]({code[1]})]"


def render_standard_bullet(entry: dict, *, include_badge: bool = False) -> str:
    line = f"* {render_name(entry)}"
    description = entry.get("description") or ""
    repo_ref = render_repo_ref(entry, include_badge=include_badge)
    if repo_ref:
        line += repo_ref
    if description:
        line += f" - {description}"
    return line


def render_resource_links(entry: dict) -> str:
    links = entry.get("links") or []
    if not links:
        return ""
    rendered = [f"[{link['label']}]({link['url']})" for link in links]
    if entry.get("url") or entry.get("description"):
        return f" ({', '.join(rendered)})"
    return f" [{', '.join(rendered)}]"


def render_resource_entry(entry: dict) -> list[str]:
    indent = "  " * int(entry.get("_indent", 0) or 0)
    if entry.get("_type") == "header":
        return [f"{indent}* {entry['name']}"]

    line = f"{indent}* {render_name(entry)}"
    if entry.get("url") and entry.get("links"):
        line += render_resource_links(entry)
    description = entry.get("description") or ""
    if description:
        if description.startswith((",", ".", ";", ":")):
            line += description
        else:
            line += f" {description}"
    if not (entry.get("url") and entry.get("links")):
        line += render_resource_links(entry)

    lines = [line]
    notes = entry.get("notes") or []
    for note in notes:
        lines.append(f"{indent}  * {note}")
    return lines


def render_other_list(entry: dict) -> str:
    line = f"* {render_name(entry)}"
    description = entry.get("description") or ""
    if description:
        line += f" - {description}"
    return line


def render_grouped_resource_section(entries: list[dict]) -> list[str]:
    lines: list[str] = []
    ordered_subsections: list[str] = []
    grouped: dict[str, list[dict]] = {}
    for entry in entries:
        subsection = entry.get("_subsection") or ""
        if subsection not in grouped:
            ordered_subsections.append(subsection)
            grouped[subsection] = []
        grouped[subsection].append(entry)

    for subsection in ordered_subsections:
        if subsection:
            lines.append(f"#### {subsection}")
            lines.append("")
        for entry in grouped[subsection]:
            lines.extend(render_resource_entry(entry))
        lines.append("")
    return lines


def generate_readme() -> str:
    root = Path(__file__).resolve().parent.parent
    libraries = load_yaml(root / "data" / "libraries.yaml")
    mesh_processing = load_yaml(root / "data" / "mesh-processing.yaml")
    papers = load_yaml(root / "data" / "papers.yaml")
    books = load_yaml(root / "data" / "books.yaml")
    articles = load_yaml(root / "data" / "articles.yaml")
    other_lists = load_yaml(root / "data" / "other-awesome-lists.yaml")

    active_libraries = [entry for entry in libraries if entry.get("_subsection") == "Active"]
    inactive_libraries = [entry for entry in libraries if entry.get("_subsection") == "Inactive"]

    lines: list[str] = [
        "# Awesome Collision Detection",
        "",
        "A curated list of collision detection open resources",
        "",
        "#### Table of Contents",
        "* [Libraries](#libraries)",
        "* [Papers](#papers)",
        "* [Books](#books)",
        "* [Articles](#articles)",
        "* [Other Awesome Lists](#other-awesome-lists)",
        "* [Contributing](#contributing)",
        "",
        "## [Libraries](#awesome-collision-detection)",
        "",
        "**Active**",
        "",
        "> :warning: The following table is not complete. Please feel free to report if you find something incorrect or missing.",
        "",
        "| Name | Shapes | Features | Languages | Licenses | Code | Popularity |",
        "|:----:| ------ | -------- | --------- | -------- | ---- | ---------- |",
    ]

    for entry in active_libraries:
        lines.append(render_active_library_row(entry))

    lines.extend(
        [
            "",
            "> Some libraries (e.g., ODE and Bullet) are physics engines that contain collision detection features, but they can be used just as collision detection libraries.",
            "",
            "**Inactive**",
            "",
        ]
    )

    for entry in inactive_libraries:
        lines.append(render_standard_bullet(entry))

    lines.extend(["", "### Mesh Processing", ""])
    for entry in mesh_processing:
        lines.append(render_standard_bullet(entry, include_badge=True))

    lines.extend(["", "## [Papers](#awesome-collision-detection)", ""])
    lines.extend(render_grouped_resource_section(papers))

    lines.extend(["## [Books](#awesome-collision-detection)", ""])
    for entry in books:
        lines.extend(render_resource_entry(entry))
    lines.append("")

    lines.extend(["## [Articles](#awesome-collision-detection)", ""])
    lines.extend(render_grouped_resource_section(articles))

    lines.extend(["## [Other Awesome Lists](#awesome-collision-detection)", ""])
    for entry in other_lists:
        lines.append(render_other_list(entry))

    lines.extend(
        [
            "",
            "## [Contributing](#awesome-collision-detection)",
            "",
            "Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/master/CONTRIBUTING.md) first. Also, please feel free to report any error.",
            "",
            "## [License](#awesome-collision-detection)",
            "",
            "[![CC0](https://licensebuttons.net/p/zero/1.0/88x31.png)](http://creativecommons.org/publicdomain/zero/1.0/)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate README.md from YAML data")
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Output file path (default: README.md in repo root)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    output_path = Path(args.output) if args.output else root / "README.md"
    output_path.write_text(generate_readme(), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
