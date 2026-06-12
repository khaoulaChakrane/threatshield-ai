import requests
import base64
from app.config import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3"

def scan_url(url: str) -> dict:
    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}

    # 1. Soumet l'URL pour analyse
    response = requests.post(
        f"{VT_BASE_URL}/urls",
        headers=headers,
        data={"url": url}
    )
    response.raise_for_status()
    analysis_id = response.json()["data"]["id"]

    # 2. Récupère le rapport d'analyse
    report = requests.get(
        f"{VT_BASE_URL}/analyses/{analysis_id}",
        headers=headers
    )
    report.raise_for_status()
    data = report.json()["data"]["attributes"]

    stats = data["stats"]
    # stats = {"malicious": 2, "suspicious": 0, "harmless": 60, "undetected": 10, "timeout": 0}

    total_engines = sum(stats.values())
    malicious_count = stats["malicious"] + stats["suspicious"]

    risk_score = round((malicious_count / total_engines) * 100, 2) if total_engines > 0 else 0
    verdict = "malicious" if risk_score > 10 else "benign"

    return {
        "verdict": verdict,
        "risk_score": risk_score,
        "stats": stats,
        "status": data.get("status")
    }