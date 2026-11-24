import unittest
import json
from pathlib import Path
from scripts.validate import validate

class CoverageTest(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).resolve().parents[1] / "data/2026/metadata.json").read_text())
    def test_valid(self):
        self.assertEqual(validate(self.data), [])
    def test_missing_period(self):
        self.data["quarters"][2]["start"] = "2026-07-01"
        self.assertTrue(validate(self.data))
    def test_unapproved_release(self):
        self.data["status"] = "released"
        self.assertTrue(validate(self.data))
    def test_duplicate_label(self):
        self.data["quarters"][1]["label"] = "Q1"
        self.assertTrue(validate(self.data))
