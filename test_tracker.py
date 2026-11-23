import json
import os
import tempfile
import unittest

import tracker


class TrackerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "projects.json")

    def tearDown(self):
        self.tmp.cleanup()

    def test_create_saves_project(self):
        tracker.create_project("Website", "Acme", "2026-12-31", "Sam", path=self.path)
        with open(self.path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(
            data,
            [{"title": "Website", "client": "Acme", "due_date": "2026-12-31", "owner": "Sam"}],
        )

    def test_list_shows_projects_in_order(self):
        tracker.create_project("First", "A", "2026-01-01", "Sam", path=self.path)
        tracker.create_project("Second", "B", "2026-02-02", "Lee", path=self.path)
        output = tracker.format_projects(tracker.list_projects(self.path))
        self.assertIn("First", output)
        self.assertIn("Second", output)
        self.assertLess(output.index("First"), output.index("Second"))

    def test_create_rejects_empty_fields(self):
        valid = {"title": "T", "client": "C", "due_date": "2026-01-01", "owner": "O"}
        for field in valid:
            for bad in ("", "   "):
                args = dict(valid, **{field: bad})
                with self.subTest(field=field, value=bad):
                    with self.assertRaises(ValueError):
                        tracker.create_project(path=self.path, **args)
        self.assertFalse(os.path.exists(self.path))

    def test_create_rejects_bad_date(self):
        for bad in ("31-12-2026", "2026/12/31", "2026-13-01", "2026-02-30", "tomorrow"):
            with self.subTest(date=bad):
                with self.assertRaises(ValueError):
                    tracker.create_project("T", "C", bad, "O", path=self.path)
        self.assertFalse(os.path.exists(self.path))

    def test_list_empty_prints_no_projects_yet(self):
        output = tracker.format_projects(tracker.list_projects(self.path))
        self.assertEqual(output, "No projects yet")


if __name__ == "__main__":
    unittest.main()
