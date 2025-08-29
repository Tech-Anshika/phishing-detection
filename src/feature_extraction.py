import pandas as pd
from datetime import datetime

# Trusted registrar list
TRUSTED_REGISTRARS = ["GoDaddy", "MarkMonitor", "Google", "Cloudflare", "Namecheap"]

def calculate_features(input_csv="data/domain_dataset.csv", output_csv="data/feature_dataset.csv"):
    df = pd.read_csv(input_csv)

    features = []
    for _, row in df.iterrows():
        feature_row = {}
        feature_row["domain"] = row["domain"]

        # Domain Age
        try:
            creation = datetime.fromisoformat(str(row["creation_date"]))
            expiration = datetime.fromisoformat(str(row["expiration_date"]))
            domain_age = (expiration - creation).days
        except:
            domain_age = -1
        feature_row["domain_age_days"] = domain_age

        # Registrar reputation
        registrar = str(row["registrar"]) if pd.notna(row["registrar"]) else ""
        feature_row["trusted_registrar"] = 1 if any(tr in registrar for tr in TRUSTED_REGISTRARS) else 0

        # DNS Features
        feature_row["has_mx"] = 1 if pd.notna(row["mx_records"]) else 0
        feature_row["has_ns"] = 1 if pd.notna(row["ns_records"]) else 0

        # WHOIS Completeness
        feature_row["whois_complete"] = 1 if pd.notna(row["registrar"]) and pd.notna(row["country"]) else 0

        features.append(feature_row)

    # Save to CSV
    feature_df = pd.DataFrame(features)
    feature_df.to_csv(output_csv, index=False)
    print(f"✅ Features extracted and saved to {output_csv}")


if __name__ == "__main__":
    calculate_features()
