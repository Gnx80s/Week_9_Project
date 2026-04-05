import os
import csv
from datetime import datetime  # FIXED: Proper import to allow datetime.now()
from collections import defaultdict
from utils import timestamp

def update_history(data, history_file):
    file_exists = os.path.isfile(history_file)

    with open(history_file, "a", newline="") as f:
        fieldnames = ["timestamp", "type", "value", "risk"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for item in data:
            writer.writerow({
                "timestamp": now,
                "type": item["type"],
                "value": item["value"],
                "risk": item["risk"]
            })

def deduplicate(data):
    unique = {}

    for item in data:
        key = (item["type"], item["value"])

        if key not in unique:
            unique[key] = item
        else:
            # Keep highest confidence
            if item["confidence"] > unique[key]["confidence"]:
                unique[key]["confidence"] = item["confidence"]

            # Update last seen
            unique[key]["last_seen"] = item["last_seen"]

    return list(unique.values())

def save_csv(data, output_path):
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["type", "value", "source", "confidence", "risk", "first_seen", "last_seen"]
        )
        writer.writeheader()
        writer.writerows(data)

def generate_report(data, report_dir):
    ts = timestamp()
    report_file = f"{report_dir}/report_{ts}.txt"

    stats = defaultdict(int)

    for item in data:
        stats[item["risk"]] += 1

    with open(report_file, "w") as f:
        f.write("Threat Intelligence Report\n")
        f.write(f"Generated: {ts}\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total IOCs: {len(data)}\n\n")

        for risk, count in stats.items():
            f.write(f"{risk}: {count}\n")

    return report_file