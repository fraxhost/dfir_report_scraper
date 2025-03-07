import json
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ReportItem:
    title: str
    url: str
    publish_date: datetime
    description: List[str]


# Open and read the JSON file
with open("dfir_reports.json", "r", encoding="utf-8") as file:
    data = json.load(file)  # Parse JSON into a Python dictionary

# Convert to list of NewsItem objects
report_list = [
    ReportItem(
        title=item["title"],
        url=item["url"],
        publish_date=datetime.fromisoformat(item["publish_date"]),
        description=item["description"],
    )
    for item in data
]

csv_filename = "dfir_sentences.csv"

with open(csv_filename, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Print formatted output
    for report in report_list:
        writer.writerow([f"---------- {report.title} starts ----------"])
        for sentence in report.description:
            writer.writerow([sentence])
        writer.writerow([f"---------- {report.title} ends ----------"])
        writer.writerow(["\n"])
