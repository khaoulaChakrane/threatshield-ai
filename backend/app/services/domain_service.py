import requests
from app.config import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3"

def scan_domain(domain: str) -> dict:
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}

    response = requests.get(f"{VT_BASE_URL}/domains/{domain}", headers=headers)
    response.raise_for_status()
    data = response.json()["data"]["attributes"]

    stats = data.get("last_analysis_stats", {})
    total = sum(stats.values()) if stats else 0
    malicious_count = stats.get("malicious", 0) + stats.get("suspicious", 0)

    risk_score = round((malicious_count / total) * 100, 2) if total > 0 else 0
    verdict = "malicious" if risk_score > 10 else "benign"

    return {
        "verdict": verdict,
        "risk_score": risk_score,
        "reputation": data.get("reputation"),
        "creation_date": data.get("creation_date"),
        "registrar": data.get("registrar"),
        "stats": stats,
    }