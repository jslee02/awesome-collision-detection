#!/usr/bin/env python3
"""Generate README.md from structured YAML data."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml


REPO = "jslee02/awesome-collision-detection"

RESOURCE_SECTIONS = [
    ("papers", "Papers"),
    ("books", "Books"),
    ("articles", "Articles"),
]


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


def repo_url(entry: dict) -> str | None:
    link = code_link(entry)
    return link[1] if link else None


def format_stars(count: int) -> str:
    if count >= 1000:
        return f"{count / 1000:.1f}k".replace(".0k", "k")
    return str(count)


def activity_emoji(entry: dict) -> str:
    if entry.get("archived") or (entry.get("_meta") or {}).get("archived"):
        return "💀"

    last_commit = (entry.get("_meta") or {}).get("last_commit")
    if not last_commit:
        return ""

    try:
        commit_date = date.fromisoformat(str(last_commit))
    except (TypeError, ValueError):
        return ""

    days_ago = (date.today() - commit_date).days
    if days_ago <= 365:
        return "🟢"
    if days_ago <= 730:
        return "🟡"
    return "🔴"


def render_name(entry: dict) -> str:
    name = entry.get("name", "")
    url = entry.get("url")
    return f"[{name}]({url})" if url else name


def render_repo_ref(entry: dict) -> str:
    link = code_link(entry)
    if not link:
        return ""

    meta = entry.get("_meta") or {}
    if entry.get("github") and meta.get("stars") is not None:
        return f" [⭐ {format_stars(meta['stars'])}]({link[1]})"
    return f" [[{link[0]}]({link[1]})]"


def render_library_bullet(entry: dict) -> str:
    parts = ["*"]
    emoji = activity_emoji(entry)
    if emoji:
        parts.append(emoji)

    parts.append(render_name(entry))

    description = entry.get("description") or ""
    if description:
        parts.append(f"- {description}")

    repo_ref = render_repo_ref(entry)
    if repo_ref:
        parts.append(repo_ref.strip())

    return " ".join(parts)


def render_standard_bullet(entry: dict) -> str:
    line = f"* {render_name(entry)}"
    repo_ref = render_repo_ref(entry)
    if repo_ref:
        line += repo_ref

    description = entry.get("description") or ""
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
    for note in entry.get("notes") or []:
        lines.append(f"{indent}  * {note}")
    return lines


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


def sort_libraries(entries: list[dict], sort_key: str) -> list[dict]:
    if sort_key == "none":
        return entries
    if sort_key == "stars":
        return sorted(
            entries,
            key=lambda entry: (entry.get("_meta") or {}).get("stars") or 0,
            reverse=True,
        )
    if sort_key == "last_commit":
        return sorted(
            entries,
            key=lambda entry: (entry.get("_meta") or {}).get("last_commit") or "",
            reverse=True,
        )
    return sorted(entries, key=lambda entry: entry.get("name", "").lower())


def render_library_section(
    libraries: list[dict],
    mesh_processing: list[dict],
    *,
    sort_key: str,
) -> list[str]:
    active = [
        entry for entry in libraries if entry.get("_subsection") == "Active"
    ]
    inactive = [
        entry for entry in libraries if entry.get("_subsection") == "Inactive"
    ]

    lines = [
        "## [Libraries](#contents)",
        "",
        "### [Active](#contents)",
        "",
        "_Collision detection, distance query, and proximity query libraries. See also [Comparisons](COMPARISONS.md)._",
        "",
    ]

    for entry in sort_libraries(active, sort_key):
        lines.append(render_library_bullet(entry))

    lines.extend(
        [
            "",
            "> Some libraries, such as ODE and Bullet, are physics engines that can also be used as collision detection libraries.",
            "",
            "### [Inactive](#contents)",
            "",
        ]
    )
    for entry in sort_libraries(inactive, sort_key):
        lines.append(render_library_bullet(entry))

    lines.extend(
        [
            "",
            "### [Mesh Processing](#contents)",
            "",
            "_Geometry processing libraries useful for collision-ready meshes and convex approximations._",
            "",
        ]
    )
    for entry in sort_libraries(mesh_processing, sort_key):
        lines.append(render_library_bullet(entry))

    lines.append("")
    return lines


def render_toc() -> str:
    return """\
## Contents
* [Libraries](#libraries)
  * [Active](#active)
  * [Inactive](#inactive)
  * [Mesh Processing](#mesh-processing)
* [Comparisons](COMPARISONS.md)
* [Papers](#papers)
* [Books](#books)
* [Articles](#articles)
* [Other Awesome Lists](#other-awesome-lists)
* [Contributing](#contributing)
* [Star History](#star-history)
* [License](#license)"""


def generate_readme(sort_key: str = "name") -> str:
    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    libraries = load_yaml(data_dir / "libraries.yaml")
    mesh_processing = load_yaml(data_dir / "mesh-processing.yaml")
    other_lists = load_yaml(data_dir / "other-awesome-lists.yaml")

    lines: list[str] = [
        "# Awesome Collision Detection",
        "",
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        "A curated list of collision detection libraries, algorithms, papers, and related resources.",
        "",
        render_toc(),
        "",
        "> **Legend**: 🟢 Active (<1yr) · 🟡 Slow (1-2yr) · 🔴 Stale (>2yr) · 💀 Archived",
        "",
    ]

    lines.extend(render_library_section(libraries, mesh_processing, sort_key=sort_key))

    for key, title in RESOURCE_SECTIONS:
        entries = load_yaml(data_dir / f"{key}.yaml")
        if not entries:
            continue
        lines.extend([f"## [{title}](#contents)", ""])
        lines.extend(render_grouped_resource_section(entries))

    lines.extend(["## [Other Awesome Lists](#contents)", ""])
    for entry in other_lists:
        lines.append(render_standard_bullet(entry))

    lines.extend(
        [
            "",
            "## [Contributing](#contents)",
            "",
            "Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/master/CONTRIBUTING.md) first. Also, please feel free to report any error.",
            "",
            "## [Star History](#contents)",
            "",
            f"[![Star History Chart](https://api.star-history.com/svg?repos={REPO}&type=Date)](https://star-history.com/#{REPO})",
            "",
            "## [License](#contents)",
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
    parser.add_argument(
        "--sort",
        choices=["name", "stars", "last_commit", "none"],
        default="name",
        help="Sort libraries and mesh-processing entries (default: name)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    if not data_dir.exists():
        print(f"ERROR: {data_dir} not found", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else root / "README.md"
    output_path.write_text(generate_readme(sort_key=args.sort), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
