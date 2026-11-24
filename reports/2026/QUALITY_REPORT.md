# Quality report — development draft
## Source audit, 2026-11-24
Twelve source CSV tables parsed: 23,749 rows including overlapping aggregate views; zero column-count mismatches, one exact duplicate row (Q1 downloads). Q1 tier tables contain 14,550 distinct address strings without cross-tier overlap. Two low-tier addresses require IPv6 validation. Q1 critical/high timestamps parse in initial checks; all 10,804 medium/low records use literal N/A for both time fields. Q1 hash table has 26 syntactically valid SHA256 rows; Q2 hash table has 658. Q1 download URL availability: 33/6552; destination path availability: 6518/6552. Q2 download SHA256 availability: 20/55; filename availability: 0/55. These are structural checks, not independent verification of threat attribution.
## Release blockers
Documented redistribution permission and data license; complete source reconciliation (including text and JSON metadata); normalization, provenance and schema testing; review of comparable metrics and publication sensitivity; annual release window after December 31, 2026.
Q3/Q4 unavailable, not zero. Raw samples excluded. No final processed dataset has been published.
