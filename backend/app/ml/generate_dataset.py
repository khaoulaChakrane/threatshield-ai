import random
import csv
import os

random.seed(42)

LEGITIMATE_BRANDS = [
    "paypal", "amazon", "google", "microsoft", "apple",
    "facebook", "netflix", "instagram", "twitter", "linkedin",
    "bankofamerica", "chase", "wellsfargo", "citibank", "hsbc",
    "dropbox", "outlook", "office365", "yahoo", "ebay"
]

SUSPICIOUS_TLDS = [
    "xyz", "tk", "ml", "ga", "cf", "gq", "top", "club",
    "online", "site", "live", "buzz", "click", "link"
]

PHISHING_PATHS = [
    "/login", "/signin", "/verify", "/account/verify",
    "/secure/login", "/update/account", "/confirm/email",
    "/banking/secure", "/auth/login", "/user/verify",
    "/password/reset", "/account/suspended", "/verify/identity",
]

LEGIT_SITES = [
    "google.com", "github.com", "stackoverflow.com",
    "wikipedia.org", "mozilla.org", "python.org",
    "reactjs.org", "docker.com", "postgresql.org",
    "cloudflare.com", "digitalocean.com", "vercel.com",
    "netlify.com", "stripe.com", "auth0.com",
    "elastic.co", "mongodb.com", "ubuntu.com",
    "owasp.org", "letsencrypt.org", "reddit.com",
    "medium.com", "dev.to", "hackernews.com",
    "youtube.com", "linkedin.com", "twitter.com",
]

LEGIT_PATHS = [
    "", "/", "/about", "/contact", "/blog", "/news",
    "/products", "/docs", "/help", "/faq",
    "/terms", "/privacy", "/search", "/articles",
    "/questions/tagged/python", "/wiki/Machine_learning",
    "/user/profile", "/category/tech", "/page/1",
    "/learn/tutorial", "/en-US/docs/Web",
]

def generate_phishing_urls(count=5000):
    urls = []
    patterns = [
        lambda b, t, p: f"http://{b.replace('a','4').replace('o','0')}-secure.{t}{p}",
        lambda b, t, p: f"http://{b}-verify-account.{t}{p}",
        lambda b, t, p: f"http://secure-{b}-login.{t}{p}",
        lambda b, t, p: f"http://{b}-account-update.{t}{p}",
        lambda b, t, p: f"http://{''.join(random.choices('abcdefghij',k=8))}.{b}-login.{t}{p}",
        lambda b, t, p: f"http://{b}{random.randint(10,99)}-secure.{t}{p}",
        lambda b, t, p: f"http://{b}-secure-login-verify.{t}{p}",
        lambda b, t, p: f"http://{b}-verify.{t}/?token={''.join(random.choices('abcdef0123456789',k=32))}",
        lambda b, t, p: f"http://login-{b}-secure.{t}{p}",
        lambda b, t, p: f"http://{b}.verify-account.{t}{p}",
    ]

    while len(urls) < count:
        brand = random.choice(LEGITIMATE_BRANDS)
        tld = random.choice(SUSPICIOUS_TLDS)
        path = random.choice(PHISHING_PATHS)
        pattern = random.choice(patterns)
        try:
            url = pattern(brand, tld, path)
            urls.append(url)
        except:
            pass

    return urls[:count]

def generate_benign_urls(count=5000):
    urls = []
    while len(urls) < count:
        site = random.choice(LEGIT_SITES)
        path = random.choice(LEGIT_PATHS)
        urls.append(f"https://{site}{path}")
    return urls[:count]

def generate_csv(output_path, count=5000):
    print(f"Génération de {count} URLs malveillantes...")
    phishing = generate_phishing_urls(count)

    print(f"Génération de {count} URLs bénignes...")
    benign = generate_benign_urls(count)

    print(f"Sauvegarde dans {output_path}...")
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["url", "label"])
        for url in phishing:
            writer.writerow([url, 1])
        for url in benign:
            writer.writerow([url, 0])

    print(f"Dataset généré : {len(phishing) + len(benign)} URLs")
    print(f"Phishing : {len(phishing)}")
    print(f"Bénignes : {len(benign)}")

if __name__ == "__main__":
    output = os.path.join(os.path.dirname(__file__), "phishing_dataset.csv")
    generate_csv(output, count=5000)

    # Aperçu
    print("\n=== Exemples phishing ===")
    for u in generate_phishing_urls(5):
        print(f"  {u}")
    print("\n=== Exemples bénins ===")
    for u in generate_benign_urls(5):
        print(f"  {u}")
