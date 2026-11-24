# Local usage
Requires Python 3.10+; no third-party dependencies for core tools.
From the repository root:
```sh
python scripts/validate.py
python scripts/build_summary.py --check
python -m unittest discover -s tests -v
python examples/analyze_summary.py
python scripts/checksums.py
```
For authorized local CSV quality inspection only:
```sh
python scripts/audit_tables.py /path/to/authorized/table.csv
python scripts/quality_summary.py /path/to/authorized/table.csv
```
These tools do not emit individual data rows, contact indicators or retrieve samples. Keep local input outside the repository. Review aggregates for sensitivity before sharing. CSV/JSONL are analytical summaries, not a blocklist or operational indicator feed.
