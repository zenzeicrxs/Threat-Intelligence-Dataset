# VulneraX — Annual Threat Intelligence Dataset

2026 edition · Defensive research · Partial-year coverage

**Status: development preview. Official annual release after 31 December 2026.**

| Source collection | Observation dates | Status |
|---|---|---|
| Q1 | 2026-02-20 – 2026-03-21 | Available |
| Q2 | 2026-03-24 – 2026-06-20 | Available |
| Q3 | — | No data available |
| Q4 | — | No data available |

## Dataset

[2026/summary.csv](2026/summary.csv) contains audited collection counts, completeness and deduplication metrics. Full individual indicator CSV is generated locally before artifact review and the annual release.

| Normalized indicator type | Unique records |
|---|---:|
| IPv4 | 21,508 |
| SHA-256 | 682 |
| Total | 22,190 |

The empirical build processed 23,590 input rows, excluded 28, and deduplicated across periods. Q1 and Q2 share 1,370 normalized IPv4 addresses and 2 SHA-256 hashes. These are observations, not confirmed maliciousness, incidents, or actor identities. Q1/Q2 collections differ in methodology; absent periods are not zero. Q1 timestamps are missing in 10,804 tier records.

## Obtain the full CSV for authorized local review

Python 3.12; standard library only. From the repository root:

```sh
python build_dataset.py
```

It retrieves only four pinned, owner-authorized source text files and checks their Git blob integrity. It writes `.local/2026/indicators.csv` and a checksum/provenance manifest. Alternatively provide authorized local copies using `--source /path/to/source`. Output stays outside Git tracking; no IOC endpoints are contacted and no malware is downloaded. Do not distribute the local candidate before artifact review and annual release.

CSV fields: `indicator_id` (deterministic SHA-256 identifier), `indicator_type` (ipv4, ipv6 or sha256), `indicator_value` (canonical observed value), `source_periods` (JSON array of source labels), `source_references` (JSON array of original file paths, row numbers and file checksums). Non-global, multicast, malformed and scoped addresses are excluded. URL, observation-level, binary, session and external enrichment data are outside this compact dataset.

## Source and verification

[Blacklist-Artifact](https://github.com/zenzeicrxs/Blacklist-Artifact/tree/14e732e6acd8002a5ada7c729e34aeeda04cd70d). Structural audit: 12 source CSVs, 23,749 rows across overlapping tables. The earlier full empirical Python verification passed schema and CSV/JSONL/Parquet round-trip checks at [commit 56587c1](https://github.com/zenzeicrxs/Threat-Intelligence-Dataset/tree/56587c18a49468d8f4b652ab870679bba4d66b85). The original engineering documentation and tests remain in that historical commit. The compact builder reuses the verified normalizer; it is not itself the previously tested CLI.

## License and release

Publisher: VulneraX. Software: Apache-2.0 ([LICENSE](LICENSE)). Reviewed, officially released data: CC BY 4.0 ([LICENSE-DATA.md](LICENSE-DATA.md)). Owner authorization recorded 2026-11-24; artifact-level rights and sensitivity review required before TLP:CLEAR classification. The original source TLP:AMBER label is not automatically changed. No malware binaries, live feed or blocking recommendation. Cite VulneraX, edition 2026, exact commit and license.

New editions are released annually after Q4. Unavailable periods are explicitly marked. This preview is not the official 2026 release.
