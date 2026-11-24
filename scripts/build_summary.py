"""Validate reviewed aggregate CSV and generate deterministic JSONL; never processes raw IOC values."""
import argparse
import csv
import json
from pathlib import Path

def read_metrics(path):
    with Path(path).open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != ["period","metric","count","verification"]:
            raise ValueError("Unexpected columns")
        records = []
        seen = set()
        for row in reader:
            if None in row or any(v is None for v in row.values()):
                raise ValueError("Malformed record")
            key = (row["period"], row["metric"])
            if key in seen or row["period"] not in ("Q1","Q2") or not row["metric"]:
                raise ValueError("Invalid or duplicate metric")
            seen.add(key)
            if not row["count"].isascii() or not row["count"].isdigit() or row["verification"] != "structural_audit":
                raise ValueError("Invalid count or verification")
            row["count"] = int(row["count"])
            records.append(row)
        m = {(r["period"], r["metric"]):r["count"] for r in records}
        def q(metric):
            return m["Q1",metric]
        if sum(q("ip_"+tier+"_rows") for tier in ("critical","high","medium","low")) != q("distinct_ip_strings"):
            raise ValueError("Tier counts do not reconcile")
        if q("ip_timestamp_present")+q("ip_timestamp_missing") != q("distinct_ip_strings"):
            raise ValueError("Timestamp counts do not reconcile")
        for period,metric in [("Q1","download_url_present"),("Q1","download_destination_present"),("Q2","download_hash_present"),("Q2","download_filename_present")]:
            if m[period,metric] > m[period,"download_rows"]:
                raise ValueError("Completeness count exceeds denominator")
        return records

def render(records):
    return "".join(json.dumps(r, separators=(",",":"), ensure_ascii=False)+"\n" for r in records)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[1]/"data/2026"
    output = render(read_metrics(root/"aggregate_statistics.csv"))
    target = root/"aggregate_statistics.jsonl"
    if args.check:
        if target.read_text(encoding="utf-8") != output:
            raise SystemExit("CSV/JSONL mismatch")
        print("Aggregate reconciliation passed")
    else:
        target.write_text(output, encoding="utf-8")
