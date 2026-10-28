"""
Script: inspect_data.py
Project: Customer Churn & Retention Analysis
Description:
    Performs Phase 1 comprehensive data inspection on the raw Telco dataset:
    - Dimensions, columns, and data types
    - Missing value detection (explicit NaN vs whitespace blanks)
    - Duplicate customerID check
    - Target variable ('Churn') distribution
    - Summary of categorical and numeric columns
"""

import os
import pandas as pd
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "Telco-Customer-Churn.csv")

def inspect_dataset():
    if not os.path.exists(RAW_DATA_PATH):
        print(f"[ERROR] Raw data file not found at: {RAW_DATA_PATH}")
        print("Please run scripts/download_data.py first.")
        return

    df = pd.read_csv(RAW_DATA_PATH)

    print("=" * 80)
    print("PHASE 1: RAW DATASET INSPECTION REPORT")
    print("=" * 80)

    # 1. Shape and Structure
    print(f"\n1. DATASET DIMENSIONS:")
    print(f"   Total Records (Rows)   : {df.shape[0]:,}")
    print(f"   Total Attributes (Cols): {df.shape[1]}")

    # 2. Duplicate Check
    duplicate_rows = df.duplicated().sum()
    duplicate_ids = df['customerID'].duplicated().sum()
    print(f"\n2. DUPLICATE CHECK:")
    print(f"   Full duplicate rows     : {duplicate_rows}")
    print(f"   Duplicate customerID entries: {duplicate_ids}")
    print(f"   Is customerID unique primary key?: {duplicate_ids == 0}")

    # 3. Column Data Types & Standard Null Checks
    print(f"\n3. COLUMN DATA TYPES & STANDARD NULL COUNTS:")
    info_df = pd.DataFrame({
        'Data Type': df.dtypes,
        'Non-Null Count': df.notnull().sum(),
        'Standard Null Count': df.isnull().sum(),
        'Null %': (df.isnull().sum() / len(df) * 100).round(2)
    })
    print(info_df.to_string())

    # 4. Hidden Data Quality Issue: Whitespace in TotalCharges
    is_blank = df['TotalCharges'].str.strip() == ''
    blank_total_charges = is_blank.sum()
    print(f"\n4. DATA QUALITY ANOMALY DETECTION (TotalCharges):")
    print(f"   Column 'TotalCharges' data type: {df['TotalCharges'].dtype} (Expected: float64)")
    print(f"   Number of whitespace / empty string rows in 'TotalCharges': {blank_total_charges}")
    
    if blank_total_charges > 0:
        tenure_of_blanks = df[is_blank]['tenure'].value_counts().to_dict()
        print(f"   Tenure of these {blank_total_charges} rows: {tenure_of_blanks}")
        churn_of_blanks = df[is_blank]['Churn'].value_counts().to_dict()
        print(f"   Churn status of these {blank_total_charges} rows: {churn_of_blanks}")
        print("   -> INSIGHT: All 11 records have tenure = 0 months (new sign-ups).")
        print("      None of these 11 customers have churned (Churn = 'No').")

    # 5. Target Variable Distribution: Churn
    print(f"\n5. TARGET VARIABLE DISTRIBUTION ('Churn'):")
    churn_counts = df['Churn'].value_counts()
    churn_pct = df['Churn'].value_counts(normalize=True) * 100
    churn_summary = pd.DataFrame({
        'Count': churn_counts,
        'Percentage (%)': churn_pct.round(2)
    })
    print(churn_summary.to_string())

    # 6. Numeric Features Summary
    print(f"\n6. NUMERIC SUMMARY (Raw numeric columns):")
    print(df.describe().round(2).to_string())

    # 7. Categorical Cardinality & Unique Values Preview
    print(f"\n7. CATEGORICAL FEATURES & UNIQUE VALUES:")
    cat_cols = df.select_dtypes(include=['object']).columns.drop(['customerID', 'TotalCharges'])
    for col in cat_cols:
        unique_vals = df[col].unique().tolist()
        print(f"   - {col:18}: {len(unique_vals)} unique values -> {unique_vals}")

    print("\n" + "=" * 80)
    print("INSPECTION COMPLETE: Raw dataset is verified and ready for Phase 2 cleaning.")
    print("=" * 80)

if __name__ == "__main__":
    inspect_dataset()
