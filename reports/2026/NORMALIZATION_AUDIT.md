# Independent normalization audit — development
Source commit: 14e732e6acd8002a5ada7c729e34aeeda04cd70d. Four text files inspected, no executable retrieval. Independent JavaScript check on 2026-11-24, using strict IPv4/IPv6 syntax and conservative global-unicast checks. This is not the Python builder run.
| Source | Input | Accepted | Excluded non-global | Malformed |
|---|---:|---:|---:|---:|
| Q1 IP | 14550 | 14548 | 2 | 0 |
| Q2 IP | 8356 | 8330 | 25 | 1 |
| Q1 SHA256 | 26 | 26 | 0 | 0 |
| Q2 SHA256 | 658 | 658 | 0 | 0 |
| Total | 23590 | 23562 | 27 | 1 |

After canonical deduplication: 21,508 IPv4 and 682 SHA256, total 22,190 unique indicators. No accepted IPv6 in this independent check. Q1/Q2 overlap: 1,370 IPv4 and 2 SHA256. No indicator values reproduced. Python ipaddress policies may differ; reconcile the empirical CI result before claiming final counts. URL and observation-level metadata are outside this pipeline. These are research observations, not blocking verdicts.
