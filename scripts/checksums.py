"""Generate deterministic SHA-256 manifest for reviewed aggregate artifacts only."""
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
paths = ("data/2026/aggregate_statistics.csv", "data/2026/aggregate_statistics.jsonl")
for name in paths:
    print(f"{hashlib.sha256((root / name).read_bytes()).hexdigest()}  {name}")
