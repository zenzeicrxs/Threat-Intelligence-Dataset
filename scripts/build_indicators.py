"""Build local research indicator metadata from explicitly authorized text lists.
No network, enrichment, malware handling, or public export. Use an ignored .local directory.
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

def write_local(records, audit, out):
    out = Path(out).resolve()
    local = Path(__file__).resolve().parents[1] / ".local"
    if out == local or not out.is_relative_to(local):
        raise ValueError("Output must be a subdirectory of ignored .local")
    out.mkdir(parents=True, exist_ok=True)
    with (out/"indicators.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for r in records:
            f.write(json.dumps(r, separators=(",",":"))+"\n")
    with (out/"indicators.csv").open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        for r in records:
            writer.writerow({k:json.dumps(v,separators=(",",":")) if isinstance(v,list) else v for k,v in r.items()})
    manifest = {"status":"local_review_only","rows":len(records),"sources":audit,
                "classification":"pending_artifact_review","files":{}}
    for name in ("indicators.csv","indicators.jsonl"):
        manifest["files"][name] = hashlib.sha256((out/name).read_bytes()).hexdigest()
    (out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n", encoding="utf-8")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--out", default=".local/2026", type=Path)
    parser.add_argument("--authorized-input", action="store_true", required=True)
    args = parser.parse_args()
    records, audit = build(args.source)
    write_local(records, audit, args.out)
    print(f"Local review package: {len(records)} normalized indicators; not published")
