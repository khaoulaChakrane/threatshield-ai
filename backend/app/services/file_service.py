import hashlib
import requests
from app.config import settings

VT_BASE_URL = "https://www.virustotal.com/api/v3"

def scan_file(file_bytes: bytes, filename: str) -> dict:
    # 1. Calcule le hash SHA-256 du fichier
    sha256 = hashlib.sha256(file_bytes).hexdigest()

    headers = {"x-apikey": settings.VIRUSTOTAL_API_KEY}
    response = requests.get(f"{VT_BASE_URL}/files/{sha256}", headers=headers)

    # 2. Si VirusTotal ne connaît pas ce fichier (404)
    if response.status_code == 404:
        return {
            "verdict": "benign",
            "risk_score": 0,
            "sha256": sha256,
            "filename": filename,
            "note": "Fichier inconnu de VirusTotal (jamais analysé)"
        }

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
        "sha256": sha256,
        "filename": filename,
        "stats": stats,
        "type_description": data.get("type_description"),
    }