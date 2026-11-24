"""Verify the approved text metadata snapshot in an isolated local build.
Only four pinned GitHub source files are retrieved. No IOC destinations are contacted.
No individual values or generated files are uploaded by this script.
"""
import csv
import hashlib
import json
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen
from build_indicators import build, write_local, SOURCES

PIN = "14e732e6acd8002a5ada7c729e34aeeda04cd70d"
BLOBS = (
    "b4f116c9d6adab72bc9b8e15a59fbdb47a7e3606",
    "7758ec23941e766e1b70391d881b4157de893966",
    "e0008fe8d26d9cce88ad050966840327e8dc70f0",
    "ba5344848742f0e9566924d43868cc7b660c4211",
)
ROOT = Path(__file__).resolve().parents[1]

def main():
    import jsonschema
    import pyarrow as pa
    import pyarrow.parquet as pq
    out = ROOT / ".local/empirical-verification"
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp)
        for (_, _, relative), expected in zip(SOURCES, BLOBS):
            url = f"https://raw.githubusercontent.com/zenzeicrxs/Blacklist-Artifact/{PIN}/{quote(relative, safe='/')}"
            with urlopen(url, timeout=30) as stream:
                raw = stream.read(2_000_001)
            if len(raw) > 2_000_000:
                raise ValueError("Source exceeds size limit")
            actual = hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()
            if actual != expected:
                raise ValueError("Source blob integrity check failed")
            path = source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        records, audit = build(source)
    schema = json.loads((ROOT/"schemas/indicator.schema.json").read_text())
    validator = jsonschema.Draft202012Validator(schema)
    for record in records:
        if not validator.is_valid(record):
            raise ValueError("Record schema validation failed")
    if [a["input_rows"] for a in audit] != [14550,8356,26,658]:
        raise ValueError("Source counts changed")
    if any(a["input_rows"] != a["accepted_rows"] + a["excluded_rows"] for a in audit):
        raise ValueError("Input counts do not reconcile")
    write_local(records, audit, out)
    actual_json = [json.loads(line) for line in (out/"indicators.jsonl").read_text().splitlines()]
    with (out/"indicators.csv").open(newline="", encoding="utf-8") as stream:
        actual_csv = list(csv.DictReader(stream))
    for row in actual_csv:
        for field in ("source_periods","source_references"):
            row[field] = json.loads(row[field])
    if records != actual_json or records != actual_csv:
        raise ValueError("CSV/JSONL round-trip mismatch")
    pq.write_table(pa.Table.from_pylist(records), out/"indicators.parquet", compression="zstd")
    if pq.read_table(out/"indicators.parquet").to_pylist() != records:
        raise ValueError("Parquet round-trip mismatch")
    manifest_path = out/"manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["files"]["indicators.parquet"] = hashlib.sha256((out/"indicators.parquet").read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps({"source_commit":PIN,"unique_records":len(records),
        "type_counts":dict(Counter(r["indicator_type"] for r in records)),
        "source_counts":[{k:a[k] for k in ("period","input_rows","accepted_rows","excluded_rows","duplicate_normalized_rows")} for a in audit],
        "round_trip_formats":["CSV","JSONL","Parquet"],"schema_validation":"passed"}, indent=2))

if __name__ == "__main__":
    main()
