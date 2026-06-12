import requests
from app.config import settings

ABUSEIPDB_URL = "https://api.abuseipdb.com/api/v2/check"

def scan_ip(ip: str) -> dict:
    headers = {
        "Key": settings.ABUSEIPDB_API_KEY,
        "Accept": "application/json"
    }
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    response = requests.get(ABUSEIPDB_URL, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()["data"]

    risk_score = data["abuseConfidenceScore"]  # déjà 0-100
    verdict = "malicious" if risk_score > 25 else "benign"

    return {
        "verdict": verdict,
        "risk_score": float(risk_score),
        "country": data.get("countryCode"),
        "total_reports": data.get("totalReports"),
        "isp": data.get("isp")
    }