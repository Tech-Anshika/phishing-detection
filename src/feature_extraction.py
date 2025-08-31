import pandas as pd
from datetime import datetime
import socket, ssl
import ipaddress
from .ssl_lookup import get_ssl_info  # keep your existing ssl_lookup

TRUSTED_REGISTRARS = ["GoDaddy", "MarkMonitor", "Google", "Cloudflare", "Namecheap"]

def calculate_features(input_csv="data/labeled_domains.csv", output_csv="data/final_feature_dataset.csv"):
    df = pd.read_csv(input_csv)
    features = []

    for _, row in df.iterrows():
        feature_row = {}
        domain = row["domain"]
        feature_row["domain"] = domain
        feature_row["label"] = row.get("label", 0)

        # Domain Age
        try:
            creation = datetime.fromisoformat(str(row.get("creation_date", "")))
            expiration = datetime.fromisoformat(str(row.get("expiration_date", "")))
            feature_row["domain_age_days"] = (expiration - creation).days
        except:
            feature_row["domain_age_days"] = -1

        # Registrar reputation
        registrar = str(row.get("registrar", "")) if pd.notna(row.get("registrar", "")) else ""
        feature_row["trusted_registrar"] = 1 if any(tr in registrar for tr in TRUSTED_REGISTRARS) else 0

        # DNS Features
        feature_row["has_mx"] = 1 if pd.notna(row.get("mx_records")) else 0
        feature_row["has_ns"] = 1 if pd.notna(row.get("ns_records")) else 0

        # WHOIS Completeness
        feature_row["whois_complete"] = 1 if pd.notna(row.get("registrar")) and pd.notna(row.get("country")) else 0

        # SSL Features
        ssl_info = get_ssl_info(domain)
        feature_row.update(ssl_info)

        features.append(feature_row)

    # Save features
    feature_df = pd.DataFrame(features)

    # Keep only model-trained features
    ordered_cols = ["domain_age_days","trusted_registrar","has_mx","has_ns","whois_complete",
                    "has_ssl","ssl_valid_days","is_ssl_short"]
    
    for c in ordered_cols:
        if c not in feature_df.columns:
            feature_df[c] = 0  # fill missing columns

    feature_df = feature_df[["domain","label"] + ordered_cols]  # preserve order
    feature_df.to_csv(output_csv, index=False)
    print(f"\n✅ Feature dataset saved to {output_csv}")
