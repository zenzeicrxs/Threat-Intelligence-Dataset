# VulneraX | Annual Threat Intelligence Dataset
Evidence-driven cybersecurity research for defensive security.

**Development edition — not an official release.** 2026 coverage is partial: Q1 February 20–March 21; Q2 March 24–June 20; Q3/Q4 unavailable. Release after December 31, subject to review and distribution authorization.

## Research data
Reviewed aggregate statistics: [CSV](data/2026/aggregate_statistics.csv) and [JSONL](data/2026/aggregate_statistics.jsonl). Seventeen metrics describe source tables, not incidents or current maliciousness. [Dataset card](DATASET_CARD.md) · [Dictionary](docs/AGGREGATE_DATA_DICTIONARY.md) · [Provenance](docs/DATA_PROVENANCE.md) · [Draft report](reports/2026/ANNUAL_REPORT.md) · [Quality report](reports/2026/QUALITY_REPORT.md).

## Reproduce aggregate export
```sh
python scripts/build_summary.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
python examples/analyze_summary.py
python scripts/checksums.py
```

## Governance
Historical source: [Blacklist-Artifact](https://github.com/zenzeicrxs/Blacklist-Artifact). Source TLP:AMBER marking requires explicit redistribution review. No raw indicators or executable samples included. No live feed or automatic blocking. See [limitations](docs/LIMITATIONS.md), [release checklist](docs/RELEASE_CHECKLIST.md), [release policy](docs/RELEASE_POLICY.md) and [integration guide](docs/INTEGRATION_GUIDE.md).
