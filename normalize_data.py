from datetime import datetime


def normalize(iocs):
    normalized = []
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for item in iocs:
        value = item.get("value")

        if not value:
            continue  # skip bad data

        normalized.append({
            "type": item.get("type", "unknown"),
            "value": value,
            "source": item.get("source", "unknown"),
            "confidence": item.get("confidence", 50),
            "first_seen": now,
            "last_seen": now
        })

    return normalized
