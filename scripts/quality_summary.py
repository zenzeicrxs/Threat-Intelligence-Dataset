"""Offline aggregate quality checks for approved analytical tables."""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

def summarize(path):
    with Path(path).open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, strict=True)
        header = next(reader, [])
        if not header or len(set(header)) != len(header) or any(not x.strip() for x in header):
            raise ValueError("Invalid header")
        counts = Counter()
        missing = dict.fromkeys(header, 0)
        rows = malformed = 0
        for row in reader:
            rows += 1
            if len(row) != len(header):
                malformed += 1
                continue
            counts[tuple(row)] += 1
            for key, value in zip(header, row):
                if not value.strip() or value.strip().upper() == "N/A":
                    missing[key] += 1
    return {"rows": rows, "malformed_rows": malformed,
            "exact_duplicate_rows": sum(n-1 for n in counts.values()),
            "missing_by_column": missing}

if __name__ == "__main__":
    print(json.dumps(summarize(sys.argv[1]), indent=2))
