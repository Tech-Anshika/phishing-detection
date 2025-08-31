from fastapi import FastAPI, UploadFile, File
import joblib
import pandas as pd
from src.feature_extraction import calculate_features
from src.ssl_lookup import get_ssl_info

app = FastAPI()

# Load trained model
model = joblib.load("models/phish_model.pkl")

@app.get("/")
def home():
    return {"message": "Phishing Detection API is running 🚀"}

@app.get("/predict/")
def predict(domain: str):
    temp_csv = "data/temp_domain.csv"
    pd.DataFrame([{"domain": domain, "label": 0}]).to_csv(temp_csv, index=False)
    calculate_features(input_csv=temp_csv, output_csv="data/temp_features.csv")
    df = pd.read_csv("data/temp_features.csv")

    # Corrected feature columns to match trained model
    feature_cols = ["domain_age_days","trusted_registrar","has_mx","has_ns","whois_complete",
                    "has_ssl","ssl_valid_days","is_ssl_short"]
    
    X = df[feature_cols].fillna(0)
    prediction = model.predict(X)[0]
    target_cse = "Unknown"
    return {
        "domain": domain,
        "prediction": "Phishing 🚨" if prediction == 1 else "Legit ✅",
        "target_cse": target_cse
    }

@app.post("/bulk_predict/")
async def bulk_predict(file: UploadFile = File(...)):
    """
    Upload a CSV with a column 'domain' and get predictions for all domains.
    Returns a CSV with prediction results ready for Stage-1 submission.
    """
    df = pd.read_csv(file.file)
    if "domain" not in df.columns:
        return {"error": "CSV must contain a 'domain' column."}

    df["label"] = 0
    temp_csv = "data/temp_bulk_domain.csv"
    df.to_csv(temp_csv, index=False)

    output_csv = "data/temp_bulk_features.csv"
    calculate_features(input_csv=temp_csv, output_csv=output_csv)

    feature_df = pd.read_csv(output_csv)
    feature_cols = ["domain_age_days","trusted_registrar","has_mx","has_ns","whois_complete",
                    "has_ssl","ssl_valid_days","is_ssl_short"]  # Corrected

    X = feature_df[feature_cols].fillna(0)

    feature_df["prediction"] = model.predict(X)
    feature_df["prediction_label"] = feature_df["prediction"].apply(lambda x: "Phishing 🚨" if x == 1 else "Legit ✅")
    feature_df["target_cse"] = "Unknown"

    submission_csv = "data/bulk_prediction_results.csv"
    feature_df.to_csv(submission_csv, index=False)

    return {"message": f"Bulk prediction completed. CSV saved at {submission_csv}", 
            "rows_processed": len(feature_df)}
