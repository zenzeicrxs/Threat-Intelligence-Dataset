# Cross-collection analysis — development draft
String-level audit of source TXT lists on 2026-11-24:
| Type | Q1 | Q2 | Intersection | Union |
|---|---:|---:|---:|---:|
| IP | 14550 | 8356 | 1370 | 21536 |
| SHA256 | 26 | 658 | 2 | 682 |
| URL | 9 | 14 | 0 | 23 |

All lists had distinct nonempty trimmed strings within each source. Hash comparisons are case-insensitive; both hash CSV/TXT pairs agree. All 684 hash entries meet SHA256 syntax. Three IP strings contain colons (2 Q1, 1 Q2); canonical validation still needed. IP recurrence in Q2 is 16.4% by string comparison. Collection differences and partial coverage preclude actor attribution or year-wide incidence conclusions. URL figures are aggregate-only; no live destinations distributed.
Source blob IDs: Q1 IP b4f116c9d6adab72bc9b8e15a59fbdb47a7e3606; Q2 IP 7758ec23941e766e1b70391d881b4157de893966; Q1 hash e0008fe8d26d9cce88ad050966840327e8dc70f0; Q2 hash ba5344848742f0e9566924d43868cc7b660c4211; Q1 URL c6762663c6f5f60a6776ef9800c85cefcd146019; Q2 URL 664a62ab492c22024ae92417acd7461a346e33dc.
