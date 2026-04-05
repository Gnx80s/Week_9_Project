import requests
import os
from config import ABUSEIPDB_API_KEY, OTX_API_KEY

def fetch_otx():
    if not OTX_API_KEY:
        print("[!] OTX API key missing. Skipping...")
        return []

    url = "https://otx.alienvault.com/api/v1/pulses/subscribed"
    headers = {"X-OTX-API-KEY": OTX_API_KEY}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] OTX fetch failed: {e}")
        return []

    iocs = []
    for pulse in data.get("results", []):
        for indicator in pulse.get("indicators", []):
            iocs.append({
                "type": indicator.get("type"),
                "value": indicator.get("indicator"),
                "source": "OTX"
            })

    return iocs

def fetch_abuseipdb():
    if not ABUSEIPDB_API_KEY:
        print("[!] AbuseIPDB API key missing. Skipping...")
        return []

    url = "https://api.abuseipdb.com/api/v2/blacklist"
    headers = {
        "Key": ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"[!] AbuseIPDB fetch failed: {e}")
        return []

    iocs = []
    for item in data.get("data", []):
        iocs.append({
            "type": "IP",
            "value": item.get("ipAddress"),
            "confidence": item.get("abuseConfidenceScore", 50),
            "source": "AbuseIPDB"
        })

    return iocs

def fetch_feodo(file_path):
    if not os.path.exists(file_path):
        print(f"[!] Feodo file not found: {file_path}")
        return []

    iocs = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                ip = line.strip()
                if ip and not ip.startswith("#"):
                    iocs.append({
                        "type": "IP",
                        "value": ip,
                        "source": "Feodo"
                    })
    except Exception as e:
        print(f"[!] Error reading Feodo file: {e}")

    return iocs

def fetch_feodo_live():
    url = "https://feodotracker.abuse.ch/downloads/ipblocklist.txt"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        lines = response.text.splitlines()
    except Exception as e:
        print(f"[!] Feodo fetch failed: {e}")
        return []

    iocs = []
    for line in lines:
        if line.startswith("#") or not line.strip():
            continue

        iocs.append({
            "type": "IP",
            "value": line.strip(),
            "source": "Feodo"
        })

    return iocs