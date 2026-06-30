import re
import math
import tldextract
from urllib.parse import urlparse

def extract_url_features(url: str) -> dict:
    parsed = urlparse(url)
    ext = tldextract.extract(url)

    url_length = len(url)
    domain = ext.domain + "." + ext.suffix if ext.suffix else ext.domain
    domain_length = len(domain)
    subdomain_count = len(ext.subdomain.split(".")) if ext.subdomain else 0
    path = parsed.path
    path_length = len(path)

    def entropy(s):
        if not s:
            return 0
        freq = {c: s.count(c)/len(s) for c in set(s)}
        return -sum(p * math.log2(p) for p in freq.values())

    domain_entropy = entropy(ext.domain)
    digit_count = sum(c.isdigit() for c in domain)
    hyphen_count = domain.count("-")
    dot_count = url.count(".")
    has_ip = bool(re.match(r'https?://\d+\.\d+\.\d+\.\d+', url))
    has_at = "@" in url
    has_double_slash = "//" in parsed.path

    phishing_keywords = [
        "login", "verify", "secure", "account", "update",
        "banking", "confirm", "password", "signin", "wallet",
        "paypal", "amazon", "microsoft", "apple", "google"
    ]
    keyword_count = sum(1 for kw in phishing_keywords if kw in url.lower())
    path_depth = path.count("/")
    is_https = int(parsed.scheme == "https")

    # ← 3 features supplémentaires importantes
    url_length_ratio = len(ext.domain) / url_length if url_length > 0 else 0
    special_char_count = sum(url.count(c) for c in ['%', '=', '?', '&', '+'])
    tld_suspicious = int(ext.suffix in [
        "tk", "ml", "ga", "cf", "gq", "xyz", "top",
        "club", "online", "site", "live", "buzz"
    ])

    return {
        "url_length": url_length,
        "domain_length": domain_length,
        "subdomain_count": subdomain_count,
        "path_length": path_length,
        "domain_entropy": round(domain_entropy, 4),
        "digit_count": digit_count,
        "hyphen_count": hyphen_count,
        "dot_count": dot_count,
        "has_ip": int(has_ip),
        "has_at": int(has_at),
        "has_double_slash": int(has_double_slash),
        "keyword_count": keyword_count,
        "path_depth": path_depth,
        "is_https": is_https,
        "url_length_ratio": round(url_length_ratio, 4),
        "special_char_count": special_char_count,
        "tld_suspicious": tld_suspicious,
    }