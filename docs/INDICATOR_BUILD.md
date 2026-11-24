# Local indicator metadata build
Input: only the four explicitly named, authorized IP and SHA256 text files, preserving source directory paths. Do not clone or fetch malware samples. No network activity is performed. From the repository root run:
```sh
python scripts/build_indicators.py --source /path/to/approved/text-metadata --out .local/2026 --authorized-input
```
Output is restricted to an ignored local directory. CSV and JSONL contain one record per canonical address or SHA256, deterministic identifiers, quarter membership and source file SHA256/line references. The manifest records accepted, excluded and normalized duplicate counts. Non-global, multicast, scoped and malformed addresses are excluded; no automatic verdict or threat attribution. No URL, session identifier, filename or executable included. Schema describes JSONL records; CSV array fields are JSON-encoded. Artifact-level review and annual release gate still apply. Tests use synthetic fixtures; execution against the complete real source is not yet independently verified.
