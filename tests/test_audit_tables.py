import tempfile
import unittest
from pathlib import Path
from scripts.audit_tables import audit

class TableAuditTest(unittest.TestCase):
    def test_counts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "fixture.csv"
            path.write_text("category,count\na,2\nb,\nc\n", encoding="utf-8")
            result = audit(path)
            self.assertEqual(result["rows"], 3)
            self.assertEqual(result["malformed_rows"], 1)
            self.assertEqual(result["missing_by_column"], {"category": 0, "count": 1})
    def test_duplicate_header(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "fixture.csv"
            path.write_text("a,a\n1,2\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                audit(path)
