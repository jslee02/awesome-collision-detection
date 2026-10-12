"""Tests for removing deleted repositories in scripts/fetch_metadata.py."""

import sys
import tempfile
import unittest
import urllib.error
from datetime import date
from pathlib import Path
from unittest import mock

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import fetch_metadata  # noqa: E402


def setUpModule():
    global network_guard
    network_guard = mock.patch("urllib.request.urlopen", side_effect=AssertionError("Tests must stay offline"))
    network_guard.start()


def tearDownModule():
    network_guard.stop()


class GoneRepoTest(unittest.TestCase):
    def refresh(self, entries, today, results):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "x.yaml"
            path.write_text(yaml.dump(entries), encoding="utf-8")
            with mock.patch.object(fetch_metadata, "fetch_repo_metadata", side_effect=lambda r: results[r]), \
                    mock.patch.object(fetch_metadata.time, "sleep"):
                fetch_metadata.process_yaml_file(path, today=today)
            return yaml.safe_load(path.read_text(encoding="utf-8"))

    def test_marks_then_removes_after_a_week(self):
        entries = [{"name": "Gone", "github": "a/gone"}, {"name": "Alive", "github": "a/alive"}]
        results = {"a/gone": fetch_metadata.GONE, "a/alive": ({"stars": 5}, "a/alive")}
        first = self.refresh(entries, date(2026, 10, 12), results)
        self.assertEqual(first[0]["_meta"]["gone_since"], "2026-10-12")
        self.assertEqual(len(self.refresh(first, date(2026, 10, 15), results)), 2)  # grace period
        self.assertEqual([e["name"] for e in self.refresh(first, date(2026, 10, 19), results)], ["Alive"])

    def test_back_again_clears_the_mark(self):
        entries = [{"name": "Back", "github": "a/back", "_meta": {"gone_since": "2026-10-12"}}]
        back = self.refresh(entries, date(2026, 10, 19), {"a/back": ({"stars": 1}, "a/back")})
        self.assertEqual(back[0]["_meta"], {"stars": 1})


    def test_failed_commit_lookup_keeps_the_previous_date(self):
        entries = [{"name": "X", "github": "a/x", "_meta": {"id": 1, "stars": 1, "last_commit": "2026-01-02"}}]
        kept = self.refresh(entries, date(2026, 10, 19), {
            "a/x": ({"id": 1, "stars": 2, "_commit_lookup_failed": True}, "a/x")
        })
        self.assertEqual(kept[0]["_meta"], {"id": 1, "stars": 2, "last_commit": "2026-01-02"})
        # A link corrected to another repository doesn't inherit the old repository's date.
        moved = self.refresh(entries, date(2026, 10, 19), {
            "a/x": ({"id": 2, "stars": 2, "_commit_lookup_failed": True}, "a/x")
        })
        self.assertEqual(moved[0]["_meta"], {"id": 2, "stars": 2})

    def test_missing_repository_ids_do_not_preserve_a_date(self):
        entries = [{"name": "X", "github": "a/x", "_meta": {"last_commit": "2026-01-02"}}]
        refreshed = self.refresh(entries, date(2026, 10, 19), {
            "a/x": ({"stars": 2, "_commit_lookup_failed": True}, "a/x")
        })
        self.assertEqual(refreshed[0]["_meta"], {"stars": 2})

    def test_successfully_empty_commit_lookup_clears_the_previous_date(self):
        entries = [{"name": "X", "github": "a/x", "_meta": {"id": 1, "last_commit": "2026-01-02"}}]
        refreshed = self.refresh(entries, date(2026, 10, 19), {"a/x": ({"id": 1, "stars": 2}, "a/x")})
        self.assertNotIn("last_commit", refreshed[0]["_meta"])

    def test_rename_preserves_list_specific_fields(self):
        entry = {"name": "X", "github": "old/x", "badge_github": "old/x", "shapes": ["Mesh"],
                 "links": [{"label": "Paper", "url": "https://example.com/paper"}], "notes": ["Note"]}
        refreshed = self.refresh([entry], date(2026, 10, 19), {"old/x": ({"id": 1}, "new/y")})[0]
        self.assertEqual(refreshed["github"], "new/y")
        for field in ("badge_github", "shapes", "links", "notes"):
            self.assertEqual(refreshed[field], entry[field])

    def test_transient_repository_failure_keeps_the_entry_unchanged(self):
        entry = {"name": "X", "github": "a/x", "_meta": {"id": 1, "gone_since": "2026-10-01"}}
        self.assertEqual(self.refresh([entry], date(2026, 10, 19), {"a/x": None}), [entry])

    def test_dry_run_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "libraries.yaml"
            original = "- name: X\n  github: a/x\n"
            path.write_text(original, encoding="utf-8")
            with mock.patch.object(fetch_metadata, "fetch_repo_metadata", return_value=fetch_metadata.GONE), \
                    mock.patch.object(fetch_metadata.time, "sleep"):
                fetch_metadata.process_yaml_file(path, dry_run=True, today=date(2026, 10, 19))
            self.assertEqual(path.read_text(encoding="utf-8"), original)


class LookupTest(unittest.TestCase):
    def test_lookup_follows_the_link_and_never_pushed_at(self):
        urls = []
        repo = {"id": 99, "full_name": "new/correct", "stargazers_count": 3, "default_branch": "main",
                "pushed_at": "2026-10-01T00:00:00Z"}
        with mock.patch.object(fetch_metadata, "fetch_json", side_effect=lambda url, *a: urls.append(url) or repo), \
                mock.patch.object(fetch_metadata, "fetch_default_branch_commit_date", return_value=None) as commits:
            meta, full_name = fetch_metadata.fetch_repo_metadata("new/correct")
        # A corrected link wins over a stale stored ID, and its repository's ID is recorded.
        self.assertEqual(urls, ["https://api.github.com/repos/new/correct"])
        self.assertEqual((meta["id"], full_name), (99, "new/correct"))
        self.assertEqual(commits.call_args[0][0], "new/correct")
        self.assertNotIn("last_commit", meta)  # never pushed_at, which counts other branches

    def test_renamed_repository_uses_the_canonical_commit_path_and_keeps_license_name(self):
        repo = {"id": 99, "full_name": "new/correct", "default_branch": "main",
                "license": {"spdx_id": "NOASSERTION", "name": "Other"}, "archived": True, "language": "C++"}
        with mock.patch.object(fetch_metadata, "fetch_json", return_value=repo), \
                mock.patch.object(fetch_metadata, "fetch_default_branch_commit_date", return_value="2026-10-01") as commits:
            meta, full_name = fetch_metadata.fetch_repo_metadata("old/name")
        self.assertEqual(commits.call_args[0][0], "new/correct")
        self.assertEqual(full_name, "new/correct")
        self.assertEqual(meta, {"id": 99, "last_commit": "2026-10-01", "license": "Other",
                                "archived": True, "language": "C++"})

    def test_only_transient_commit_failures_are_marked_for_preservation(self):
        repo = {"id": 99, "default_branch": "main"}
        for code in (403, 429, 500, 503, 404, 409):
            with self.subTest(code=code), mock.patch.object(fetch_metadata, "fetch_json", return_value=repo), \
                    mock.patch.object(fetch_metadata, "fetch_default_branch_commit_date",
                                      side_effect=urllib.error.HTTPError("", code, "Error", {}, None)):
                meta, _ = fetch_metadata.fetch_repo_metadata("a/x")
            self.assertEqual(bool(meta.get("_commit_lookup_failed")), code in (403, 429, 500, 503))
        for error in (urllib.error.URLError("Temporary failure"), TimeoutError()):
            with self.subTest(error=error), mock.patch.object(fetch_metadata, "fetch_json", return_value=repo), \
                    mock.patch.object(fetch_metadata, "fetch_default_branch_commit_date", side_effect=error):
                meta, _ = fetch_metadata.fetch_repo_metadata("a/x")
            self.assertTrue(meta["_commit_lookup_failed"])

    def test_repository_errors_distinguish_gone_from_transient_failures(self):
        for code in (404, 451, 403, 429, 500):
            with self.subTest(code=code), mock.patch.object(fetch_metadata, "fetch_json",
                                                          side_effect=urllib.error.HTTPError("", code, "Error", {}, None)):
                result = fetch_metadata.fetch_repo_metadata("a/x")
            self.assertEqual(result, fetch_metadata.GONE if code in (404, 451) else None)


class ManualReviewGoneTest(unittest.TestCase):
    def test_a_resource_keeps_its_entry_when_its_code_is_gone(self):
        entries = [{"name": "Paper", "url": "https://arxiv.org/abs/1", "github": "a/code",
                    "_meta": {"gone_since": "2026-10-01"}}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "papers.yaml"
            path.write_text(yaml.dump(entries), encoding="utf-8")
            with mock.patch.object(fetch_metadata, "fetch_repo_metadata", return_value=fetch_metadata.GONE), \
                    mock.patch.object(fetch_metadata.time, "sleep"):
                fetch_metadata.process_yaml_file(path, today=date(2026, 10, 12))
            self.assertEqual(yaml.safe_load(path.read_text(encoding="utf-8")),
                             [{"name": "Paper", "url": "https://arxiv.org/abs/1"}])

    def test_a_resource_whose_home_was_the_repository_goes_with_it(self):
        entries = [{"name": "Tutorial", "url": "https://github.com/a/code", "github": "a/code",
                    "_meta": {"gone_since": "2026-10-01"}}]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "papers.yaml"
            path.write_text(yaml.dump(entries), encoding="utf-8")
            with mock.patch.object(fetch_metadata, "fetch_repo_metadata", return_value=fetch_metadata.GONE), \
                    mock.patch.object(fetch_metadata.time, "sleep"):
                fetch_metadata.process_yaml_file(path, today=date(2026, 10, 12))
            self.assertEqual(yaml.safe_load(path.read_text(encoding="utf-8")), [])


if __name__ == "__main__":
    unittest.main()
