"""Validate annual coverage metadata; no network access or data publication."""
import json
from datetime import date
from pathlib import Path

def validate(data):
    errors = []
    quarters = data["quarters"]
    if [q["label"] for q in quarters] != ["Q1", "Q2", "Q3", "Q4"]:
        errors.append("Expected four ordered unique quarter labels")
    for q in quarters:
        a,b = q["start"],q["end"]
        if q["availability"] == "unavailable":
            if a is not None or b is not None:
                errors.append("Unavailable period must not invent dates")
        elif q["availability"] == "available_at_source":
            try:
                if date.fromisoformat(a) > date.fromisoformat(b):
                    errors.append("Reversed observation dates")
            except (TypeError, ValueError):
                errors.append("Invalid observation dates")
        else:
            errors.append("Unknown availability")
    if data["status"] == "released":
        if not data["redistribution_approved"]:
            errors.append("Distribution approval missing")
        if date.today() <= date(data["year"],12,31):
            errors.append("Annual release window not reached")
    return errors

if __name__ == "__main__":
    path = Path(__file__).resolve().parents[1] / "data/2026/metadata.json"
    errors = validate(json.loads(path.read_text(encoding="utf-8")))
    if errors:
        raise SystemExit("\n".join(errors))
    print("Coverage metadata checks passed")
