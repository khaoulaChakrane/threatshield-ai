import re
from email import message_from_bytes
from email.policy import default

def analyze_email(file_bytes: bytes, filename: str) -> dict:
    msg = message_from_bytes(file_bytes, policy=default)

    subject = msg.get("Subject", "")
    sender = msg.get("From", "")
    received_spf = msg.get("Received-SPF", "")
    auth_results = msg.get("Authentication-Results", "")

    # Analyse SPF
    spf_pass = "pass" in received_spf.lower() or "spf=pass" in auth_results.lower()

    # Analyse DKIM
    dkim_pass = "dkim=pass" in auth_results.lower()

    # Analyse DMARC
    dmarc_pass = "dmarc=pass" in auth_results.lower()

    # Détection de liens suspects dans le corps
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_content()
    else:
        body = msg.get_content()

    urls_found = re.findall(r'https?://[^\s<>"]+', body)
    suspicious_keywords = ["urgent", "verify your account", "click here", "suspended", "winner"]
    keyword_hits = sum(1 for kw in suspicious_keywords if kw.lower() in body.lower())

    # Calcul du score de risque
    risk_score = 0
    if not spf_pass:
        risk_score += 30
    if not dkim_pass:
        risk_score += 30
    if not dmarc_pass:
        risk_score += 20
    risk_score += min(keyword_hits * 5, 20)

    verdict = "malicious" if risk_score > 40 else "benign"

    return {
        "verdict": verdict,
        "risk_score": float(risk_score),
        "subject": subject,
        "sender": sender,
        "spf_pass": spf_pass,
        "dkim_pass": dkim_pass,
        "dmarc_pass": dmarc_pass,
        "urls_count": len(urls_found),
        "suspicious_keywords_found": keyword_hits,
    }