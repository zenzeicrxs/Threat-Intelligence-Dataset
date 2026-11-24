# Local indicator metadata build
Use only four approved source text files. No executables, URLs or session metadata are processed. No network access in the core builder. Run from the repository root:
```sh
python scripts/build_indicators.py --source /path/to/approved/text-metadata --out .local/2026 --authorized-input
```
Output CSV, JSONL and checksum manifest stay in ignored .local. One record per canonical global address or SHA256; deterministic ID, source membership and source line references. No reputation verdict or actor attribution.
## Pinned empirical verification
```sh
python -m pip install -r requirements-verification.txt
python scripts/verify_empirical.py
```
The verifier retrieves only four authorized text files from the pinned GitHub source commit, checks Git blob integrity, validates the schema and checks CSV, JSONL and Parquet round trips. All row-level output remains local; only aggregate counts are logged. CI does not upload generated row-level files. Artifact-level review and the annual release gate still apply.
