"""Render fictional prompt text locally. Python 3.11+. No model/network calls."""
import csv
import json
from pathlib import Path
from string import Template
import sys

FIELDS = ["case_id", "topic", "audience", "notes"]
VARIABLES = {"topic", "audience", "notes"}

def render(template_text, csv_path):
    template = Template(template_text)
    if not template.is_valid() or set(template.get_identifiers()) != VARIABLES:
        raise ValueError("Template must contain exactly topic, audience and notes variables")
    result = []
    seen = set()
    with Path(csv_path).open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        if reader.fieldnames != FIELDS:
            raise ValueError("CSV headers must be case_id,topic,audience,notes in that order")
        for number, row in enumerate(reader, 2):
            if set(row) != set(FIELDS) or any(v is None or not v.strip() for v in row.values()):
                raise ValueError(f"Row {number} must supply four nonblank fields")
            if row["case_id"] in seen:
                raise ValueError(f"Duplicate case_id at row {number}")
            seen.add(row["case_id"])
            result.append({"case_id": row["case_id"], "prompt": template.substitute({k: row[k] for k in VARIABLES})})
    if not result:
        raise ValueError("CSV must contain at least one case")
    return result

def main():
    if sys.version_info < (3, 11):
        raise ValueError("Python 3.11 or newer is required")
    if len(sys.argv) != 3:
        raise ValueError("Usage: python3 render_prompt.py prompt-template.txt prompt-cases.csv")
    template = Path(sys.argv[1]).read_text(encoding="utf-8")
    result = render(template, sys.argv[2])
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, csv.Error) as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
