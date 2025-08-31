# Phishing Detection System 🚨

**Repository:** [phishing-detection](https://github.com/Tech-Anshika/phishing-detection)  
**Stage:** 1 – Submission Ready  

---

## 1. Project Overview

The **Phishing Detection System** is an AI-powered platform designed to detect phishing domains targeting **Critical Sector Entities (CSEs)**. It provides both single-domain prediction and bulk-domain processing through a **FastAPI** interface, allowing researchers and cybersecurity teams to submit domains for automated analysis.  

This project is part of a hackathon Stage-1 submission and is focused on rapid, accurate, and reliable domain threat classification.

---

## 2. Problem Statement

CSEs face an increasing number of phishing attacks, where malicious actors create fraudulent websites to steal sensitive information. Manual detection is time-consuming and error-prone.  

**Solution Approach:**  
- Automate phishing detection using a machine learning model trained on domain features.  
- Provide bulk and single-domain prediction capabilities.  
- Generate submission-ready CSV files for Stage-1 evaluation.  

---

## 3. Features

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check: returns a simple message confirming API is running. |
| `/predict/` | GET | Predicts if a single domain is phishing or legitimate. |
| `/bulk_predict/` | POST | Accepts a CSV file with multiple domains and returns a CSV with predictions for Stage-1 submission. |

### Domain Features Used

- Domain age (`domain_age_days`)  
- Trusted registrar (`trusted_registrar`)  
- Presence of MX records (`has_mx`)  
- Presence of NS records (`has_ns`)  
- WHOIS completeness (`whois_complete`)  
- SSL validity (`has_ssl`, `ssl_valid_days`, `is_ssl_short`)  
- IP address, subnet, and IDN status  

> Note: For Stage-1 submission, only features used in model training are included in predictions.

---

## 4. Technology Stack

- **Backend:** Python, FastAPI  
- **ML Model:** scikit-learn (RandomForestClassifier)  
- **Data Processing:** pandas  
- **SSL Lookup & Networking:** `ssl`, `socket`, `ipaddress`  
- **File Handling:** CSV input/output for Stage-1 submission  

---

## 5. Usage

### Run Locally

#### 1. Clone the repository:

```bash
git clone https://github.com/Tech-Anshika/phishing-detection.git
cd phishing-detection
```
#### 2. Install dependencies:
```bash
pip install -r requirements.txt
```
#### 3. Start the API:
```bash
uvicorn src.app:app --reload
```
#### 4. Access endpoints:
-Single domain: http://127.0.0.1:8000/predict/?domain=example.com
-Bulk CSV: POST CSV file to http://127.0.0.1:8000/bulk_predict/
## 6. Project Structure
```bash
phishing-detection/
│
├─ data/                  # Input/output CSVs
├─ models/                # Trained ML model
├─ src/
│   ├─ app.py             # FastAPI application
│   ├─ feature_extraction.py  # Feature calculation logic
│   └─ ssl_lookup.py      # SSL info extraction
├─ requirements.txt       # Python dependencies
└─ README.md
```
