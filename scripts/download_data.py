"""
Script: download_data.py
Project: Customer Churn & Retention Analysis
Description:
    Downloads the official IBM Telco Customer Churn dataset into data/raw/
    without modifying the original source content.
    Includes fallback URL and validation checks (row/column count).
"""

import os
import sys
import urllib.request
import pandas as pd

# Define paths relative to project root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
RAW_DATA_PATH = os.path.join(RAW_DATA_DIR, "Telco-Customer-Churn.csv")

# Public download URLs (IBM official repository and verified mirror)
PRIMARY_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
FALLBACK_URL = "https://raw.githubusercontent.com/treselle-systems/customer_churn_analysis/master/WA_Fn-UseC_-Telco-Customer-Churn.csv"

def download_dataset():
    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    if os.path.exists(RAW_DATA_PATH):
        print(f"[INFO] Raw dataset already exists at: {RAW_DATA_PATH}")
        print("[INFO] Skipping download to protect raw data integrity.")
    else:
        print("[INFO] Downloading IBM Telco Customer Churn dataset...")
        downloaded = False

        for url in [PRIMARY_URL, FALLBACK_URL]:
            try:
                print(f"[INFO] Attempting download from: {url}")
                urllib.request.urlretrieve(url, RAW_DATA_PATH)
                print("[SUCCESS] Download completed successfully.")
                downloaded = True
                break
            except Exception as e:
                print(f"[WARNING] Failed to download from {url}. Error: {e}")

        if not downloaded:
            print("[ERROR] Could not download dataset automatically.")
            print("\n--- Manual Download Instructions ---")
            print("1. Visit: https://github.com/IBM/telco-customer-churn-on-icp4d/raw/master/data/Telco-Customer-Churn.csv")
            print(f"2. Save the file as 'Telco-Customer-Churn.csv' directly into:\n   {RAW_DATA_DIR}")
            sys.exit(1)

    # Validate dataset structure
    try:
        df = pd.read_csv(RAW_DATA_PATH)
        print("\n--- Raw Data Verification ---")
        print(f"File Location : {RAW_DATA_PATH}")
        print(f"File Size     : {os.path.getsize(RAW_DATA_PATH) / 1024:.2f} KB")
        print(f"Rows Count    : {df.shape[0]} (Expected: 7043)")
        print(f"Columns Count : {df.shape[1]} (Expected: 21)")
        print(f"Target Column : 'Churn' present -> {'Churn' in df.columns}")

        if df.shape[0] == 7043 and df.shape[1] == 21:
            print("[SUCCESS] Dataset integrity verified successfully!")
        else:
            print("[WARNING] Shape differs from standard benchmark. Review data.")
    except Exception as e:
        print(f"[ERROR] Failed to read downloaded file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    download_dataset()
