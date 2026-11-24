import tempfile
import unittest
from pathlib import Path
from scripts.quality_summary import summarize

class SummaryTest(unittest.TestCase):
    def test_missing_and_duplicate(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "fixture.csv"
            p.write_text("category,time\na,N/A\na,N/A\nb,\nc\n", encoding="utf-8")
            self.assertEqual(summarize(p), {"rows":4,"malformed_rows":1,"exact_duplicate_rows":1,"missing_by_column":{"category":0,"time":3}})
