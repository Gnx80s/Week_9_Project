def assign_risk(confidence):
    try:
        confidence = int(confidence)
    except:
        confidence = 50

    if confidence >= 80:
        return "HIGH"
    elif confidence >= 50:
        return "MEDIUM"
    else:
        return "LOW"


def enrich_with_risk(data):
    for item in data:
        item["risk"] = assign_risk(item.get("confidence", 50))
    return data
