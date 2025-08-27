import requests
import pandas as pd
from domain_lookup import get_domain_info   # jo function humne domain_lookup.py me likha tha

# Function: Alexa Top Sites se domains lena
def fetch_alexa_top_sites(limit=50):
    """
    Alexa Top Sites (public list) se top domains fetch karega.
    Ab Alexa band hai, isliye hum alternative site use karte hain:
    https://www.similarweb.com/ or static dataset
    """
    # For now hum ek sample static list le rahe hain
    top_domains = [
        "google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com",
        "wikipedia.org", "amazon.com", "yahoo.com", "reddit.com", "linkedin.com"
    ]
    return top_domains[:limit]

# Function: PhishTank se phishing domains lena
def fetch_phishtank(limit=50):
    url = "https://data.phishtank.com/data/online-valid.csv"
    try:
        df = pd.read_csv(url)
        domains = df['url'].dropna().head(limit).tolist()
        return domains
    except Exception as e:
        print("⚠️ Error fetching PhishTank:", e)
        return []

# Main Crawler
def crawler(output_file="data/domain_dataset.csv", limit=20):
    print("🔍 Fetching domains...")

    # Alexa + PhishTank
    alexa_domains = fetch_alexa_top_sites(limit)
    phishing_domains = fetch_phishtank(limit)

    # Normalize domains (remove http://, https://, etc.)
    clean_domains = []
    for d in alexa_domains + phishing_domains:
        if "://" in d:
            d = d.split("://")[1]
        d = d.split("/")[0]
        clean_domains.append(d)

    print(f"✅ Total domains collected: {len(clean_domains)}")

    # Get WHOIS + DNS info
    results = []
    for domain in clean_domains:
        print(f"🔎 Checking {domain}...")
        info = get_domain_info(domain)
        results.append(info)

    # Save to CSV
    df = pd.DataFrame(results)
    df.to_csv(output_file, index=False)
    print(f"\n✅ Dataset saved to {output_file}")


if __name__ == "__main__":
    crawler(limit=30)
