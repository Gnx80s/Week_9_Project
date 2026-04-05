import csv
import os
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from utils import ensure_dirs

def load_data(csv_path):
    data = []
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def plot_risk_distribution(data, output_dir):
    risks = [item["risk"] for item in data]
    counter = Counter(risks)

    labels = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(8, 6))
    plt.bar(labels, values)
    plt.title("Risk Distribution of IOCs")
    plt.xlabel("Risk Level")
    plt.ylabel("Count")
    plt.tight_layout() 

    output_path = os.path.join(output_dir, "risk_distribution.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_type_distribution(data, output_dir):
    types = [item["type"] for item in data]
    counter = Counter(types)

    labels = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(10, 6)) 
    plt.bar(labels, values)
    plt.title("IOC Type Distribution")
    plt.xlabel("Type")
    plt.ylabel("Count")

  
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout() 

    output_path = os.path.join(output_dir, "type_distribution.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_trend(history_file, output_dir):
    trend = defaultdict(int)

    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                date = row["timestamp"].split(" ")[0]
                trend[date] += 1

    if not trend:
        return None

    dates = sorted(trend.keys())
    counts = [trend[d] for d in dates]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, counts, marker='o')
    plt.title("Threat Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of IOCs")
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    output_path = os.path.join(output_dir, "threat_trend.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_risk_pie(data, output_dir):
    risks = [item["risk"] for item in data]
    counter = Counter(risks)

    labels = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(8, 6))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title("Risk Distribution (Pie Chart)")
    plt.tight_layout()

    output_path = os.path.join(output_dir, "risk_distribution_pie.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def plot_type_pie(data, output_dir):
    types = [item["type"] for item in data]
    counter = Counter(types)

    labels = list(counter.keys())
    values = list(counter.values())

    plt.figure(figsize=(10, 6)) 
    
    
    wedges, texts, autotexts = plt.pie(
        values, 
        autopct=lambda p: f'{p:.1f}%' if p > 2 else '',
        startangle=140
    )
    
    plt.title("IOC Type Distribution (Pie Chart)")

    
    plt.legend(wedges, labels, title="IOC Types", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.tight_layout()

    output_path = os.path.join(output_dir, "type_distribution_pie.png")
    plt.savefig(output_path)
    plt.close()

    return output_path

def generate_visuals(csv_path, output_dir, history_file):
    ensure_dirs(output_dir)
    print("[+] Generating visualizations...")
    data = load_data(csv_path)

    risk_chart = plot_risk_distribution(data, output_dir)
    type_chart = plot_type_distribution(data, output_dir)
    risk_pie = plot_risk_pie(data, output_dir)
    type_pie = plot_type_pie(data, output_dir)
    trend_chart = plot_trend(history_file, output_dir)

    print(f"[✓] Visualizations saved to: {output_dir}")