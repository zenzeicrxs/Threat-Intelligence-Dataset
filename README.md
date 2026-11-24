# VulneraX | Annual Threat Intelligence Dataset
Evidence-driven cybersecurity research for defensive security.

**Development edition — not an official release.** 2026 coverage: Q1 February 20–March 21; Q2 March 24–June 20; Q3/Q4 unavailable. Official release after December 31, subject to artifact review.

## Research data
[Aggregate CSV](data/2026/aggregate_statistics.csv) · [JSONL](data/2026/aggregate_statistics.jsonl) · [Cross-collection summary](data/2026/cross_collection_summary.csv) · [Annual report draft](reports/2026/ANNUAL_REPORT.md) · [Quality report](reports/2026/QUALITY_REPORT.md) · [Normalization audit](reports/2026/NORMALIZATION_AUDIT.md).

## Reproducibility
```sh
python scripts/build_summary.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
python examples/analyze_summary.py
```
For authorized local indicator metadata, see [indicator build and empirical verification](docs/INDICATOR_BUILD.md). Local CSV, JSONL and Parquet exports are not public release assets.

## Governance
[Dataset card](DATASET_CARD.md) · [Provenance](docs/DATA_PROVENANCE.md) · [Limitations](docs/LIMITATIONS.md) · [Release checklist](docs/RELEASE_CHECKLIST.md) · [Publication authorization](docs/PUBLICATION_AUTHORIZATION.md).

Code: Apache-2.0. Approved released data: CC BY 4.0; TLP:CLEAR only after artifact review. Source: Blacklist-Artifact. No malware binaries, automatic blocking or live threat feed.
