import requests
import pandas as pd

def get_legit_domains(n=500):
    url = "https://tranco-list.eu/top-1m.csv.zip"
    legit = pd.read_csv(url, compression="zip", header=None, names=["rank", "domain"])
    legit = legit.head(n)
    legit["label"] = 0
    return legit[["domain", "label"]]

def get_phishing_domains(n=500):
    url = "https://openphish.com/feed.txt"
    response = requests.get(url)
    phishing_urls = response.text.strip().split("\n")
    phishing_domains = [u.split("/")[2] for u in phishing_urls[:n] if u.startswith("http")]
    df = pd.DataFrame(phishing_domains, columns=["domain"])
    df["label"] = 1
    return df

def build_dataset(output_csv="data/labeled_domains.csv", n=500):
    legit = get_legit_domains(n)
    phishing = get_phishing_domains(n)
    dataset = pd.concat([legit, phishing], ignore_index=True)
    dataset.to_csv(output_csv, index=False)
    print(f"✅ Dataset created with {len(dataset)} domains -> {output_csv}")

if __name__ == "__main__":
    build_dataset()
