"""Example: inspect reviewed aggregate statistics using Python standard library."""
import csv
from pathlib import Path

root = Path(__file__).resolve().parents[1]
with (root / "data/2026/aggregate_statistics.csv").open(encoding="utf-8", newline="") as stream:
    metrics = {(r["period"], r["metric"]): int(r["count"]) for r in csv.DictReader(stream)}
total = metrics["Q1", "distinct_ip_strings"]
for tier in ("critical", "high", "medium", "low"):
    count = metrics["Q1", f"ip_{tier}_rows"]
    print(f"{tier}: {count:,} ({count / total:.1%})")
print(f"Timestamp coverage: {metrics['Q1', 'ip_timestamp_present'] / total:.1%}")
print("Q3/Q4: unavailable; no estimates. Q1 and Q2 are not comparable incidence series.")
