# Normalization specification
Status: proposed, not a published dataset.
- Preserve source records locally in authorized storage; distinguish source release labels from observation dates.
- Represent unavailable values (including literal N/A in timestamp fields) as null in analytical metadata. Never infer event time from release date.
- Separate IPv4 and IPv6 validation; do not discard a record merely because it is not IPv4.
- Distinguish exact duplicate rows from repeat observations; preserve source counts and document any removal.
- ASN organization labels are not numeric ASNs.
- Keep indicator, observation and aggregate table grains distinct. Do not sum overlapping representations.
- Q1 tier classifications are source assertions, not independent reputation determinations.
- Do not export restricted row-level values or executable artifacts to this public repository.
