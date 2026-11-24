import tempfile
import unittest
from pathlib import Path
from scripts.build_indicators import build, normalize, SOURCES

class IndicatorTests(unittest.TestCase):
    def test_normalization(self):
        self.assertEqual(normalize("sha256","A"*64), ("sha256","a"*64))
        for value in ("127.0.0.1","10.0.0.1","::1","bad","fe80::1%eth0"):
            with self.assertRaises(ValueError):
                normalize("ip",value)
    def test_local_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for quarter, kind, rel in SOURCES:
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(("10.0.0.1\n" if kind=="ip" else "a"*64+"\n"), encoding="utf-8")
            records, audit = build(root)
            self.assertEqual(len(records),1)
            self.assertEqual(records[0]["source_periods"],["Q1","Q2"])
            self.assertEqual(len(records[0]["source_references"]),2)
            self.assertEqual(sum(a["excluded_rows"] for a in audit),2)
