import os
from config import FEEDS_DIR, OUTPUT_DIR, REPORT_DIR
from fetch_feeds import fetch_otx, fetch_abuseipdb, fetch_feodo_live, fetch_feodo
from normalize_data import normalize
from threat_scoring import enrich_with_risk
from aggregator import deduplicate, save_csv, generate_report, update_history
from utils import ensure_dirs
from visualise import generate_visuals

def run():
    # Ensure all output directories exist before writing
    ensure_dirs(OUTPUT_DIR, REPORT_DIR, os.path.join(OUTPUT_DIR, "visuals"))

    print("[+] Fetching threat feeds...")
    otx_data = fetch_otx()
    abuse_data = fetch_abuseipdb()
    
    # Try fetching live, fallback to local file if it fails
    feodo_data = fetch_feodo_live()
    if not feodo_data:
        local_feodo = os.path.join(FEEDS_DIR, "feodo_tracker.txt")
        print(f"[*] Falling back to local Feodo file: {local_feodo}")
        feodo_data = fetch_feodo(local_feodo)

    print("[+] Normalizing data...")
    combined = normalize(otx_data + abuse_data + feodo_data)

    print("[+] Enriching with threat scoring...")
    enriched = enrich_with_risk(combined)

    print("[+] Deduplicating...")
    final_data = deduplicate(enriched)

    output_file = os.path.join(OUTPUT_DIR, "consolidated_iocs.csv")

    print("[+] Saving results...")
    save_csv(final_data, output_file)

    history_file = os.path.join(OUTPUT_DIR, "history.csv")

    print("[+] Updating historical data...")
    update_history(final_data, history_file)
    report = generate_report(final_data, REPORT_DIR)

    print(f"[✓] Done. Output: {output_file}")
    print(f"[✓] Report: {report}")

    visuals_dir = os.path.join(OUTPUT_DIR, "visuals")
    generate_visuals(output_file, visuals_dir, history_file)

if __name__ == "__main__":
    run()