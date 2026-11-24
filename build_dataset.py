"""Build local research indicator metadata from explicitly authorized text lists.
No IOC endpoint access, enrichment, malware handling or public export. Use ignored .local.
"""
import argparse
import csv
import hashlib
import ipaddress
import json
import re
from pathlib import Path

SOURCES = (
    ("Q1", "ip", "Q1 (March 2026)/blocklist_ip_all.txt"),
    ("Q2", "ip", "Q2 (June 2026)/IOC/ip_addresses.txt"),
    ("Q1", "sha256", "Q1 (March 2026)/blocklist_sha256.txt"),
    ("Q2", "sha256", "Q2 (June 2026)/IOC/sha256.txt"),
)
FIELDS = ["indicator_id", "indicator_type", "indicator_value", "source_periods", "source_references"]

def normalize(kind, value):
    value = value.strip()
    if kind == "ip":
        if "%" in value:
            raise ValueError("Scoped address")
        addr = ipaddress.ip_address(value)
        if not addr.is_global or addr.is_multicast:
            raise ValueError("Non-global or multicast address excluded")
        return ("ipv4" if addr.version == 4 else "ipv6"), str(addr)
    if kind == "sha256" and re.fullmatch(r"[0-9a-fA-F]{64}", value):
        return "sha256", value.lower()
    raise ValueError("Unsupported or malformed indicator")

def build(source):
    records, audit = {}, []
    source = Path(source).resolve()
    for period, kind, relative in SOURCES:
        path = (source / relative).resolve()
        if not path.is_relative_to(source) or not path.is_file():
            raise ValueError("Missing or out-of-scope source")
        raw = path.read_bytes()
        summary = {"period":period, "source":relative, "sha256":hashlib.sha256(raw).hexdigest(),
                   "input_rows":0, "accepted_rows":0, "excluded_rows":0, "duplicate_normalized_rows":0}
        seen = set()
        for line_no, line in enumerate(raw.decode("utf-8-sig").splitlines(), 1):
            if not line.strip():
                continue
            summary["input_rows"] += 1
            try:
                typ, value = normalize(kind, line)
            except ValueError:
                summary["excluded_rows"] += 1
                continue
            summary["accepted_rows"] += 1
            key = (typ, value)
            if key in seen:
                summary["duplicate_normalized_rows"] += 1
            seen.add(key)
            record = records.setdefault(key, {"indicator_id":hashlib.sha256((typ+":"+value).encode()).hexdigest(),
                "indicator_type":typ, "indicator_value":value, "source_periods":[], "source_references":[]})
            if period not in record["source_periods"]:
                record["source_periods"].append(period)
            record["source_references"].append({"path":relative, "line":line_no, "source_sha256":summary["sha256"]})
        audit.append(summary)
    return [records[k] for k in sorted(records)], audit

# Pinned, owner-authorized text metadata only; no malware or IOC destinations fetched.
from tempfile import TemporaryDirectory
from urllib.parse import quote
from urllib.request import urlopen

PIN = "14e732e6acd8002a5ada7c729e34aeeda04cd70d"
BLOBS = ("b4f116c9d6adab72bc9b8e15a59fbdb47a7e3606",
         "7758ec23941e766e1b70391d881b4157de893966",
         "e0008fe8d26d9cce88ad050966840327e8dc70f0",
         "ba5344848742f0e9566924d43868cc7b660c4211")

def main():
    parser = argparse.ArgumentParser(description="Generate the local 2026 research dataset.")
    parser.add_argument("--source", type=Path, help="Authorized local source directory; otherwise retrieve the four pinned text files")
    args = parser.parse_args()
    if args.source:
        records, audit = build(args.source)
    else:
        with TemporaryDirectory() as tmp:
            source = Path(tmp)
            for (_, _, relative), expected in zip(SOURCES, BLOBS):
                url = f"https://raw.githubusercontent.com/zenzeicrxs/Blacklist-Artifact/{PIN}/{quote(relative, safe='/')}"
                with urlopen(url, timeout=30) as stream:
                    raw = stream.read(2_000_001)
                if len(raw) > 2_000_000 or hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() != expected:
                    raise ValueError("Source integrity check failed")
                path = source / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            records, audit = build(source)
        if len(records) != 22190:
            raise ValueError("Normalized count differs from verified snapshot")
    # Keep only the requested CSV and the compact provenance manifest.
    out = Path(__file__).resolve().parent / ".local/2026"
    out.mkdir(parents=True, exist_ok=True)
    path = out / "indicators.csv"
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for row in records:
            writer.writerow({k:json.dumps(v,separators=(",",":")) if isinstance(v,list) else v for k,v in row.items()})
    manifest = {"status":"local_review_only","rows":len(records),"source_commit":PIN if not args.source else None,
                "sources":audit,"csv_sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n", encoding="utf-8")
    print(f"Generated {len(records):,} records in {path}; not an official release.")

if __name__ == "__main__":
    main()
