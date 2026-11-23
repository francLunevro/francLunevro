"""Offline checks for the profile generator and its public-data boundary."""

from datetime import date
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

import refresh
import render

NS = {"svg": "http://www.w3.org/2000/svg"}
SNAPSHOT = {
    "week_start": "2026-08-30",
    "days": {"2026-09-04": 10, "2026-11-18": 1},
    "languages": {"JavaScript": 900, "CSS": 80, "HTML": 15, "Shell": 4, "Python": 1},
    "primary_language": "JavaScript",
}
REPOSITORY = "example/public-project"
PROJECT_PATH = f"/repos/{REPOSITORY}"
PUBLIC_PROJECT = {
    "visibility": "public",
    "private": False,
    "full_name": REPOSITORY,
    "default_branch": "main",
    "language": "JavaScript",
}


class DataTests(unittest.TestCase):
    def test_public_default_branch_is_pinned_and_paginated(self):
        def commit(sha, timestamp):
            return {"sha": sha, "commit": {"committer": {"date": timestamp}}}

        shown = commit("a", "2026-11-18T22:00:00Z")
        responses = [
            (PUBLIC_PROJECT, ""),
            (SNAPSHOT["languages"], ""),
            ([{"sha": "tip"}], ""),
            ([shown], '<https://api.github.com/next>; rel="next"'),
            ([shown, commit("b", "2026-11-19T01:00:00+03:00"),
              commit("old", "2026-08-29T23:59:59Z"),
              commit("future", "2026-11-20T00:00:00Z")], ""),
        ]
        with patch.object(refresh, "get_json", side_effect=responses) as api:
            result = refresh.collect_snapshot(date(2026, 11, 19), REPOSITORY)
        self.assertEqual(result["week_start"], "2026-08-30")
        self.assertEqual(result["days"], {"2026-11-18": 2})
        self.assertEqual(result["languages"], SNAPSHOT["languages"])
        requests = [call.args[1] for call in api.call_args_list[3:]]
        self.assertEqual([item["page"] for item in requests], [1, 2])
        self.assertTrue(all(item["sha"] == "tip" for item in requests))

    def test_unconfigured_and_invalid_projects_make_no_api_calls(self):
        with patch.object(refresh, "get_json") as api:
            today = date(2026, 11, 19)
            snapshot = refresh.collect_snapshot(today, "")
            self.assertIsNone(snapshot["week_start"])
            self.assertIn("when a public project is configured", render.activity(snapshot))
            self.assertIn("when a public project is configured", render.languages(snapshot))
            with self.assertRaises(refresh.RefreshError):
                refresh.collect_snapshot(today, "https://example.com/repo")
            api.assert_not_called()

    def test_private_or_renamed_project_stops_before_collecting_details(self):
        for change in ({"private": True}, {"visibility": "internal"}, {"full_name": "example/other"}):
            with self.subTest(change=change), patch.object(
                refresh, "get_json", return_value=({**PUBLIC_PROJECT, **change}, "")
            ) as api:
                with self.assertRaises(refresh.RefreshError):
                    refresh.collect_snapshot(date(2026, 11, 19), REPOSITORY)
                api.assert_called_once_with(PROJECT_PATH)

    def test_failed_api_preserves_snapshot_and_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            files = refresh.build_files(SNAPSHOT)
            refresh.write_files(files, output)
            with patch.object(refresh, "collect_snapshot", side_effect=refresh.RefreshError("Unavailable")), patch(
                "sys.argv", ["refresh.py", "--live", "--output", directory]
            ), patch("sys.stderr"):
                self.assertEqual(refresh.main(), 1)
            for relative, expected in files.items():
                self.assertEqual((output / relative).read_text(encoding="utf-8"), expected)

    def test_identical_bytes_are_never_rewritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            files = refresh.build_files(SNAPSHOT)
            self.assertEqual(len(refresh.write_files(files, output)), 6)
            before = {path: (output / path).stat().st_mtime_ns for path in files}
            self.assertEqual(refresh.write_files(files, output), [])
            self.assertEqual(before, {path: (output / path).stat().st_mtime_ns for path in files})

    def test_public_api_request_excludes_credentials(self):
        with patch.object(refresh, "build_opener") as create:
            response = create.return_value.open.return_value.__enter__.return_value
            response.read.return_value = b"{}"
            refresh.get_json(PROJECT_PATH, {"per_page": 100})
            request = create.return_value.open.call_args.args[0]
        self.assertEqual(request.host, "api.github.com")
        self.assertIsNone(request.get_header("Authorization"))
        self.assertTrue(request.full_url.endswith("?per_page=100"))


class SvgTests(unittest.TestCase):
    def test_cards_have_accessible_metadata_and_no_active_external_content(self):
        cards = render.cards(SNAPSHOT)
        self.assertEqual(len(cards), 4)
        self.assertLess(sum(len(svg.encode()) for svg in cards.values()), 40_000)
        for path, svg in cards.items():
            with self.subTest(path=path):
                root = ET.fromstring(svg)
                self.assertEqual(root.attrib["width"], "720")
                self.assertTrue(root.find("svg:title", NS).text)
                self.assertTrue(root.find("svg:desc", NS).text)
                self.assertIn("prefers-reduced-motion:reduce", svg)
                self.assertIsNone(re.search(r"<(?:script|foreignObject|iframe)\b|\son\w+=|url\((?!#)", svg))

    def test_calendar_and_language_summary_are_consistent(self):
        files = refresh.build_files(SNAPSHOT)
        graph = files[Path("assets/activity.svg")]
        table = files[Path("data/activity-summary.md")]
        self.assertEqual(graph.count(" commits</title></rect>"), 84)
        self.assertIn("11 commits across 2 days", graph)
        self.assertIn("11 commits · 2 active days", table)
        self.assertIn("| JavaScript | 900 |", table)
        self.assertIn("Other 0.5 percent", files[Path("assets/languages.svg")])

    def test_empty_window_and_language_pending_render_without_fake_totals(self):
        snapshot = {**SNAPSHOT, "days": {}, "languages": {}}
        self.assertIn("0 commits across 0 days", render.activity(snapshot))
        self.assertIn("GitHub has not reported byte totals", render.languages(snapshot))
        self.assertIn("No commits in this window", render.activity_summary(snapshot))

    def test_readme_references_valid_assets_and_text_alternatives(self):
        readme = (refresh.ROOT / "README.md").read_text(encoding="utf-8")
        paths = re.findall(r"\./((?:assets|data)/[a-z.-]+)", readme)
        self.assertEqual(len(paths), 5)
        for relative in paths:
            self.assertTrue((refresh.ROOT / relative).is_file())
        self.assertEqual(len(re.findall(r'alt="[^"]+"|!\[[^\]]+\]', readme)), 4)


if __name__ == "__main__":
    unittest.main()
