import unittest
from pathlib import Path
from scripts.build_summary import read_metrics, render

class SummaryExportTest(unittest.TestCase):
    def test_export_matches(self):
        root = Path(__file__).resolve().parents[1]/"data/2026"
        records = read_metrics(root/"aggregate_statistics.csv")
        self.assertEqual(len(records),17)
        self.assertEqual(render(records),(root/"aggregate_statistics.jsonl").read_text())
