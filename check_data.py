import json
import sys
from datetime import date
from pathlib import Path

data_file = Path(__file__).parent / "data" / "opportunities.json"

with data_file.open(encoding="utf-8") as file:
    opportunities = json.load(file)

if not isinstance(opportunities, list):
    print("ERROR: The JSON file must contain a list of opportunities.")
    sys.exit(1)

required_fields = {
    "id",
    "company",
    "title",
    "location",
    "work_mode",
    "employment_type",
    "experience_months",
    "graduation_year_requirement",
    "skills",
    "source_url",
    "last_checked",
    "fee_policy",
}

errors = []
seen_ids = set()
seen_urls = set()

for number, opportunity in enumerate(opportunities, start=1):
    if not isinstance(opportunity, dict):
        errors.append(f"Opportunity {number} must be a JSON object.")
        continue

    missing_fields = required_fields - opportunity.keys()
    if missing_fields:
        errors.append(
            f"Opportunity {number} is missing: {', '.join(sorted(missing_fields))}"
        )
        continue

    for field in ("id", "company", "title", "source_url"):
        value = opportunity[field]
        if not isinstance(value, str) or not value.strip():
            errors.append(f"Opportunity {number}: '{field}' must not be empty.")

    opportunity_id = opportunity["id"]
    if isinstance(opportunity_id, str) and opportunity_id:
        if opportunity_id in seen_ids:
            errors.append(f"Duplicate opportunity ID: {opportunity_id}")
        seen_ids.add(opportunity_id)

    source_url = opportunity["source_url"]
    if isinstance(source_url, str) and source_url:
        if not source_url.startswith(("https://", "http://")):
            errors.append(f"Opportunity {number}: source_url must start with http:// or https://.")
        if source_url in seen_urls:
            errors.append(f"Duplicate source URL: {source_url}")
        seen_urls.add(source_url)

    last_checked = opportunity["last_checked"]
    try:
        date.fromisoformat(last_checked)
    except (TypeError, ValueError):
        errors.append(
            f"Opportunity {number}: last_checked must use YYYY-MM-DD format."
        )

if errors:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)

print("Data is valid.")

for opportunity in opportunities:
    print(
        opportunity["company"],
        "-",
        opportunity["title"],
        "-",
        opportunity["work_mode"],
    )