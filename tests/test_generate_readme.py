"""README conventions and the list's resource rendering stay compatible."""

import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest import mock

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import generate_readme as readme  # noqa: E402


class GenerateReadmeTest(unittest.TestCase):
    def test_registry_covers_every_data_file(self):
        self.assertEqual(
            {f"{key}.yaml" for key, *_ in readme.SECTIONS},
            {path.name for path in (ROOT / "data").glob("*.yaml")},
        )

    def test_sorting_distinguishes_missing_stars_from_zero(self):
        entries = [
            {"name": "Absent Z"},
            {"name": "Zero", "_meta": {"stars": 0}},
            {"name": "Absent A"},
            {"name": "Tie Z", "_meta": {"stars": 10}},
            {"name": "Tie A", "_meta": {"stars": 10}},
        ]
        self.assertEqual(
            [entry["name"] for entry in readme.sort_libraries(entries)],
            ["Tie A", "Tie Z", "Zero", "Absent A", "Absent Z"],
        )

    def test_snapshot_controls_badges_and_inactive_block(self):
        as_of = date(2026, 10, 12)
        entries = [
            {"name": "Old", "_meta": {"last_commit": (as_of - timedelta(days=1096)).isoformat()}},
            {"name": "Archived", "archived": True},
            {"name": "Legacy", "_subsection": "Inactive"},
            {"name": "Unknown"},
            {"name": "Recent", "_meta": {"last_commit": as_of.isoformat()}},
            {"name": "Slow", "_meta": {"last_commit": (as_of - timedelta(days=366)).isoformat()}},
        ]
        with tempfile.TemporaryDirectory() as tmp:
            data_dir = Path(tmp)
            (data_dir / "as-of.txt").write_text(f"{as_of}\n", encoding="utf-8")
            (data_dir / "libraries.yaml").write_text(yaml.safe_dump(entries), encoding="utf-8")
            with mock.patch.object(readme, "date") as today:
                today.fromisoformat.side_effect = date.fromisoformat
                today.today.return_value = date(2040, 1, 1)
                output = readme.generate(data_dir)
                today.today.assert_not_called()
        active, folded = output.split("<details>", 1)
        self.assertIn("* 🟢 Recent", active)
        self.assertIn("* 🟡 Slow", active)
        self.assertIn("* Unknown", active)
        self.assertIn("Inactive (3)", folded)
        self.assertIn("* 💀 Archived", folded)
        self.assertIn("* Legacy", folded)
        self.assertIn("* Old · last commit 2023", folded)
        self.assertIn("stars as of 2026-10-12", output)

    def test_missing_snapshot_falls_back_to_today(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(readme.as_of_date(Path(tmp)), date.today())

    def test_resources_keep_order_links_notes_and_indentation(self):
        entries = [
            {"name": "Z group", "_type": "header", "_subsection": "Topic"},
            {
                "name": "B resource",
                "url": "https://example.com/b",
                "links": [{"label": "code", "url": "https://example.com/code"}],
                "description": ", Author 2026",
                "notes": ["A note"],
                "_indent": 1,
                "_subsection": "Topic",
            },
            {"name": "A resource", "_subsection": "Topic"},
        ]
        self.assertEqual(readme.render_grouped_resource_section(entries), [
            "#### Topic", "", "* Z group",
            "  * [B resource](https://example.com/b) ([code](https://example.com/code)), Author 2026",
            "    * A note", "* A resource", "",
        ])


class TriageEntryTest(unittest.TestCase):
    def test_resource_without_a_website_links_its_repository(self):
        # The shared triage stores a GitHub-hosted resource's repository in `github`, not `url`.
        entry = {"name": "Notes", "github": "o/notes", "description": "- Collision detection notes."}
        self.assertEqual(readme.render_resource_entry(entry), ["* [Notes](https://github.com/o/notes) - Collision detection notes."])

    def test_unclassified_resources_get_their_own_heading(self):
        entries = [{"name": "A", "url": "https://a.example", "_subsection": "Survey"},
                   {"name": "New", "url": "https://n.example"}]  # as triage adds it: no subsection
        lines = readme.render_grouped_resource_section(entries)
        self.assertEqual([l for l in lines if l.startswith("####")], ["#### Survey", "#### Other"])
        self.assertLess(lines.index("#### Other"), lines.index("* [New](https://n.example)"))

    def test_resource_with_a_website_also_links_its_repository(self):
        entry = {"name": "Paper", "url": "https://arxiv.org/abs/1", "github": "o/code", "description": "- A paper."}
        self.assertEqual(readme.render_resource_entry(entry), ["* [Paper](https://arxiv.org/abs/1) - A paper. [[github](https://github.com/o/code)]"])
        listed = {**entry, "links": [{"label": "code", "url": "https://github.com/o/code"}]}
        self.assertNotIn("[[github]", readme.render_resource_entry(listed)[0])


if __name__ == "__main__":
    unittest.main()
