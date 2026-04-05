## Threat Feed Aggregator

A centralized Cyber Threat Intelligence (CTI) tool designed to automate the collection, normalization, and analysis of Indicators of Compromise (IoCs) from multiple disparate threat feeds.
This project ingests raw data from live APIs and local files, assigns risk scores, removes duplicate entries, and generates both actionable CSV outputs and visual threat trend reports.

---

## Objectives

The Threat Feed Aggregator is a Python-based ETL pipeline designed to:

- Collect threat intelligence from APIs and local feeds.
- Normalize data into a unified schema.
- Enrich IOCs with risk scoring.
- Deduplicate and track IOC lifecycle.
- Store historical data for trend analysis.
- Generate reports and visual insights.

---

## Features

- **Multi-Source Ingestion:** Fetches intelligence from AlienVault OTX, AbuseIPDB, and the Feodo Tracker Botnet C2 blocklist.
- **Offline Fallback Capability:** Automatically detects network failures and falls back to processing local intelligence data (e.g., `feeds/feodo_tracker.txt`).
- **Data Normalization:** Translates inconsistent data structures (JSON APIs, plain text) into a unified internal schema.
- **Automated Threat Scoring:** Assigns standard risk levels (HIGH, MEDIUM, LOW) based on confidence scores.
- **Smart Deduplication:** Merges overlapping IoCs from different providers, ensuring the highest confidence score and latest timestamp are preserved.
- **Data Visualization:** Automatically generates Matplotlib pie charts, bar graphs, and historical trend lines to visualize threat distributions.

---

## API Setup

### 1. AlienVault OTX

- Visit: https://otx.alienvault.com
- Create account → Settings → API Key

---

### 2. AbuseIPDB

- Visit: https://www.abuseipdb.com
- Create account → API → Generate Key

### 3. Create `.env`

ABUSEIPDB_API_KEY=your_key_here
OTX_API_KEY=your_key_here

---

## Requirements

- Python 3.8 or higher
- Internet connection (for live API fetching)

---

## Installation

1. Clone the repository

```bash
git clone https://github.com/Gnx80s/Week_9_Projects.git
cd ThreatFeedAggregator

```

2. Install dependencies

```bash
pip install -r requirements.txt
```

## Usage

Run the main orchestration script from your terminal:

```bash
python main.py
```

---

## Project Structure

<pre>

Week_9_Project/
├── feeds/
│   └── feodo_tracker.txt         # Local fallback list of C2 IPs
|
├── output/                       #(Not tracked in version control)
│   ├── reports/                  # Generated text summaries
│   ├── visuals/                  # Generated Matplotlib PNG graphs
│   ├── consolidated_iocs.csv     # Final, deduplicated intelligence feed
│   └── history.csv               # Historical tracking database
|
├── .env                          # API Keys (Not tracked in version control)
|
├── aggregator.py                 # File I/O and deduplication orchestration
|
├── config.py                     # Environment variables and path mapping
|
├── fetch_feeds.py                # API request logic and local file reading
|
├── main.py                       # Main execution script
|
├── normalize_data.py             # Schema translation
|
├── requirements.txt              # Python dependencies
|
├── threat_scoring.py             # Risk assignment logic
|
├── utils.py                      # Helper functions (timestamps, directories)
|
├── visualise.py                  # Graphical reporting engine
|
└── README.md                     # Project documentation

</pre>

---

## Expected Console Output:

[+] Fetching threat feeds...
[+] Normalizing data...
[+] Enriching with threat scoring...
[+] Deduplicating...
[+] Saving results...
[+] Updating historical data...
[✓] Done. Output: /.../output/consolidated_iocs.csv
[✓] Report: /.../output/reports/report_202X-XX-XX_XX-XX-XX.txt
[+] Generating visualizations...
[✓] Visualizations saved to: /.../output/visuals

# Outputs

After a successful run, check the output/ directory:

- consolidated_iocs.csv: Your actionable blocklist ready to be ingested by a SIEM or firewall.
- history.csv: An appending database tracking every IoC ever seen by the aggregator over time.
- reports/: A time-stamped text summary of the current aggregation run.
- visuals/: Image files (.png) detailing the distribution of IoC types and risk levels, as well as line charts tracking threat volume over time.

---

## Disclaimer

This project is intended strictly for educational and defensive cybersecurity purposes.
The Threat Feed Aggregator collects and processes publicly available threat intelligence data to demonstrate concepts related to:

- Threat intelligence aggregation
- Data normalization and analysis
- Security monitoring and visualization

This tool must not be used for:

- Unauthorized scanning or targeting of systems
- Malicious activities or cyberattacks
- Any actions that violate applicable laws or regulations

The author does not guarantee the accuracy, completeness, or reliability of the threat intelligence data used or generated by this project. Users are responsible for verifying all data before using it in any security or operational environment.
By using this project, you agree to use it ethically, responsibly, and in compliance with all applicable laws and regulations.
