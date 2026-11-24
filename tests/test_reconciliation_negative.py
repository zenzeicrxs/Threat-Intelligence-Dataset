import csv
import tempfile
import unittest
from pathlib import Path
from scripts.build_summary import read_metrics

class NegativeReconciliationTest(unittest.TestCase):
    def test_reject_inconsistent_tier(self):
        source = Path(__file__).resolve().parents[1] / "data/2026/aggregate_statistics.csv"
        with source.open(newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            if row["metric"] == "ip_critical_rows":
                row["count"] = str(int(row["count"]) + 1)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            with path.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["period","metric","count","verification"])
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "Tier counts"):
                read_metrics(path)
