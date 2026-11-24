"""Offline aggregate quality audit of authorized CSV files. No network or row export."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

def audit(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, [])
        if not header or len(set(header)) != len(header) or any(not x.strip() for x in header):
            raise ValueError("Invalid header")
        rows = malformed = 0
        missing = [0] * len(header)
        for row in reader:
            rows += 1
            if len(row) != len(header):
                malformed += 1
                continue
            for i, value in enumerate(row):
                missing[i] += not value.strip()
    return {"sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "rows": rows, "malformed_rows": malformed,
            "missing_by_column": dict(zip(header, missing))}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    args = parser.parse_args()
    result = audit(args.csv)
    print(json.dumps(result, indent=2))
    return int(result["malformed_rows"] > 0)

if __name__ == "__main__":
    raise SystemExit(main())
