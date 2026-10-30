import json
from pathlib import Path

data_file = Path(__file__).parent / "data" / "opportunities.json"

with data_file.open(encoding="utf-8") as file:
    opportunities = json.load(file)

for opportunity in opportunities:
    print(
        opportunity["company"],
        "-",
        opportunity["title"],
        "-",
        opportunity["work_mode"],
    )