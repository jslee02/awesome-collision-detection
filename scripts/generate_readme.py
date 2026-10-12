#!/usr/bin/env python3
"""Generate README.md from structured YAML data."""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml


REPO = "jslee02/awesome-collision-detection"

# (yaml_key, title, scope), in README order. Shared triage imports this registry.
SECTIONS = [
    (
        "libraries",
        "Libraries",
        "Collision detection, distance query, and proximity query libraries. "
        "See also [Comparisons](COMPARISONS.md).",
    ),
    (
        "mesh-processing",
        "Mesh Processing",
        "Geometry processing libraries useful for collision-ready meshes and convex approximations.",
    ),
    (
        "papers",
        "Papers",
        "Research papers on collision detection, distance and proximity queries, and supporting algorithms.",
    ),
    ("books", "Books", "Books on collision detection algorithms and their implementation."),
    (
        "articles",
        "Articles",
        "Articles, talks, tutorials, and blog posts about collision detection and related geometry algorithms.",
    ),
    ("other-awesome-lists", "Other Awesome Lists", "Related curated lists and collections."),
]

RESOURCE_SECTIONS = {"papers", "books", "articles"}
# Reviewed by hand by the shared suggestion triage, even when they link code on GitHub.
MANUAL_REVIEW = RESOURCE_SECTIONS
ACTIVE_DAYS = 365
INACTIVE_DAYS = 3 * 365
AS_OF_FILE = "as-of.txt"


def as_of_date(data_dir: Path) -> date:
    """Use the metadata snapshot date so activity does not change between refreshes."""
    path = data_dir / AS_OF_FILE
    if path.exists():
        return date.fromisoformat(path.read_text(encoding="utf-8").strip())
    return date.today()


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


def stars(entry: dict) -> int | None:
    return (entry.get("_meta") or {}).get("stars")


def is_archived(entry: dict) -> bool:
    return bool(entry.get("archived") or (entry.get("_meta") or {}).get("archived"))


def idle_days(entry: dict, as_of: date) -> int | None:
    last_commit = (entry.get("_meta") or {}).get("last_commit")
    if not last_commit:
        return None
    try:
        return (as_of - date.fromisoformat(str(last_commit))).days
    except ValueError:
        return None


def is_inactive(entry: dict, as_of: date) -> bool:
    days = idle_days(entry, as_of)
    # Preserve legacy inactive projects whose commit history is not on GitHub.
    return (
        entry.get("_subsection") == "Inactive"
        or is_archived(entry)
        or (days is not None and days > INACTIVE_DAYS)
    )


def format_stars(count: int) -> str:
    if count >= 1000:
        return f"{count / 1000:.1f}k".replace(".0k", "k")
    return str(count)


def activity_emoji(entry: dict, as_of: date, folded: bool = False) -> str:
    if is_archived(entry):
        return "💀"
    days = idle_days(entry, as_of)
    if not folded and days is not None:
        return "🟢" if days <= ACTIVE_DAYS else "🟡"
    return ""


def render_name(entry: dict, link_repo: bool = False) -> str:
    """The name, linked to the website; for a resource without one, to its repository."""
    name = entry.get("name", "")
    url = entry.get("url") or ((code_link(entry) or (None, None))[1] if link_repo else None)
    return f"[{name}]({url})" if url else name


def render_repo_ref(entry: dict) -> str:
    link = code_link(entry)
    if not link:
        return ""

    meta = entry.get("_meta") or {}
    if entry.get("github") and meta.get("stars") is not None:
        return f" [⭐ {format_stars(meta['stars'])}]({link[1]})"
    return f" [[{link[0]}]({link[1]})]"


def render_library_bullet(entry: dict, as_of: date, folded: bool = False) -> str:
    parts = ["*"]
    emoji = activity_emoji(entry, as_of, folded)
    if emoji:
        parts.append(emoji)

    parts.append(render_name(entry))

    description = entry.get("description") or ""
    if description:
        parts.append(f"- {description}")

    repo_ref = render_repo_ref(entry)
    if repo_ref:
        parts.append(repo_ref.strip())

    last_commit = (entry.get("_meta") or {}).get("last_commit")
    if folded and last_commit:
        parts.append(f"· last commit {str(last_commit)[:4]}")
    return " ".join(parts)


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

    line = f"{indent}* {render_name(entry, link_repo=True)}"
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

    # A resource with both a website and a repository (as triage writes them) shows both,
    # unless the repository is already among its links.
    link = code_link(entry)
    if entry.get("url") and link and link[1] not in {item.get("url") for item in entry.get("links") or []}:
        line += render_repo_ref(entry)

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


def sort_libraries(entries: list[dict]) -> list[dict]:
    return sorted(
        entries,
        key=lambda entry: (stars(entry) is None, -(stars(entry) or 0), entry["name"].lower()),
    )


def render_library_section(key: str, entries: list[dict], as_of: date) -> list[str]:
    active = [entry for entry in entries if not is_inactive(entry, as_of)]
    inactive = [entry for entry in entries if is_inactive(entry, as_of)]
    lines = [render_library_bullet(entry, as_of) for entry in sort_libraries(active)]
    if active:
        lines.append("")
    if key == "libraries":
        lines += [
            "> Some libraries, such as ODE and Bullet, are physics engines that can also be used as collision detection libraries.",
            "",
        ]
    if inactive:
        lines += [
            "<details>",
            f"<summary>Inactive ({len(inactive)}): archived or no commits for 3+ years</summary>",
            "",
        ]
        lines += [render_library_bullet(entry, as_of, folded=True) for entry in sort_libraries(inactive)]
        lines += ["", "</details>", ""]
    return lines


def anchor(title: str) -> str:
    """GitHub heading anchor: lowercase, drop punctuation, spaces to hyphens."""
    kept = "".join(ch for ch in title.lower() if ch.isalnum() or ch in " -")
    return kept.replace(" ", "-")


def generate(data_dir: Path) -> str:
    as_of = as_of_date(data_dir)
    sections = [
        (key, title, scope, load_yaml(data_dir / f"{key}.yaml"))
        for key, title, scope in SECTIONS
        if (data_dir / f"{key}.yaml").exists()
    ]

    lines: list[str] = [
        "# Awesome Collision Detection",
        "",
        "[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        "A curated list of collision detection libraries, algorithms, papers, and related resources.",
        "",
        "## Contents",
    ]
    lines += [f"* [{title}](#{anchor(title)})" for _, title, _, entries in sections if entries]
    lines += [
        "* [Comparisons](COMPARISONS.md)",
        "* [Contributing](#contributing)",
        "* [Star History](#star-history)",
        "* [License](#license)",
        "",
        "> **Legend**: 🟢 commit within 1 yr · 🟡 commit within 3 yr · 💀 archived · "
        f"⭐ GitHub stars as of {as_of.isoformat()}. Software entries are ordered by stars; inactive "
        "entries (archived, or no commits for 3+ years) are folded at the end of each category.",
        "",
    ]

    for key, title, scope, entries in sections:
        if not entries:
            continue
        lines += [f"## [{title}](#contents)", "", f"_{scope}_", ""]
        if key in RESOURCE_SECTIONS:
            lines.extend(render_grouped_resource_section(entries))
        else:
            lines.extend(render_library_section(key, entries, as_of))

    lines.extend(
        [
            "## [Contributing](#contents)",
            "",
            "Contributions are very welcome! Please read the [contribution guidelines](https://github.com/jslee02/awesome-collision-detection/blob/main/CONTRIBUTING.md) first. Also, please feel free to report any error.",
            "",
            "## [Star History](#contents)",
            "",
            f'<a href="https://www.star-history.com/?repos={REPO.replace("/", "%2F")}">\n'
            "  <picture>\n"
            '    <source media="(prefers-color-scheme: dark)" '
            f'srcset="https://api.star-history.com/chart?repos={REPO}&type=date&theme=dark&legend=top-left" />\n'
            '    <source media="(prefers-color-scheme: light)" '
            f'srcset="https://api.star-history.com/chart?repos={REPO}&type=date&legend=top-left" />\n'
            '    <img alt="Star History Chart" '
            f'src="https://api.star-history.com/chart?repos={REPO}&type=date&legend=top-left" />\n'
            "  </picture>\n"
            "</a>",
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
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent
    data_dir = root / "data"
    if not data_dir.exists():
        print(f"ERROR: {data_dir} not found", file=sys.stderr)
        return 1

    output_path = Path(args.output) if args.output else root / "README.md"
    output_path.write_text(generate(data_dir), encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
