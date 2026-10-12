"""The validator must reject data the README generator would silently drop."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import validate_entries  # noqa: E402


class DroppedDataTest(unittest.TestCase):
    def check(self, files: dict[str, str]) -> bool:
        with tempfile.TemporaryDirectory() as tmp:
            for name, text in files.items():
                (Path(tmp) / name).write_text(text, encoding="utf-8")
            return validate_entries.validate_entries(tmp)

    def test_valid_category(self):
        self.assertTrue(self.check({"libraries.yaml": "- name: Tool\n  github: o/r\n"}))

    def test_entries_without_a_list(self):
        self.assertFalse(self.check({"libraries.yaml": "name: Tool\ngithub: o/r\n"}))  # missing "- "

    def test_file_that_is_not_a_category(self):
        self.assertFalse(self.check({"library.yaml": "- name: Tool\n  github: o/r\n"}))

    def test_empty_file_is_not_a_list(self):
        self.assertFalse(self.check({"libraries.yaml": ""}))

    def test_list_specific_fields_and_metadata_are_allowed(self):
        self.assertTrue(self.check({"libraries.yaml": """- name: Tool
  github: owner-name/repo.name_1
  badge_github: old-owner/old-repo
  shapes: [Mesh]
  notes: [Note]
  links:
    - label: Paper
      url: https://example.com/paper
  _type: header
  _indent: 1
  _meta:
    id: 123
    gone_since: '2026-10-12'
"""}))

    def test_invalid_formats_are_rejected(self):
        for field in ("_meta: {last_commit: '2026-99-12'}", "_meta: {gone_since: '2026-02-30'}"):
            with self.subTest(field=field):
                self.assertFalse(self.check({"libraries.yaml": f"- name: Tool\n  {field}\n"}))

    def test_invalid_github_slugs_are_rejected(self):
        for slug in ("-owner/repo", "owner-/repo", "owner/repo/extra", "owner/repo name", "https://github.com/o/r"):
            with self.subTest(slug=slug):
                self.assertFalse(self.check({"libraries.yaml": f"- name: Tool\n  github: {slug}\n"}))


if __name__ == "__main__":
    unittest.main()
