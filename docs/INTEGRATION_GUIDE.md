# Local quality review
Requires Python 3.10+; no third-party dependencies for these checks.

Run from repository root:
```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/audit_tables.py /path/to/authorized/table.csv
```

The CSV audit reports file checksum, row count, malformed-row count and missing cells by column. It does not emit data rows, contact indicators, fetch samples, enrich records or publish results. Review aggregates for sensitivity before sharing. A syntactically valid CSV is not proof of factual correctness. This development repository is not an operational blocklist.
