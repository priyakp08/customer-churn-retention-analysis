"""
Script: clean_and_eda.py
Project: Customer Churn & Retention Analysis
Description:
    Loads raw data, performs full data cleaning, feature engineering,
    computes accurate churn metrics across segments, generates high-quality
    visualizations, and exports the clean dataset to data/processed/.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional charts
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.size'] = 11

# Define directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "raw", "Telco-Customer-Churn.csv")
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "telco_churn_cleaned.csv")
FIGURES_DIR = os.path.join(PROJECT_ROOT, "reports", "figures")
SUMMARY_METRICS_PATH = os.path.join(PROJECT_ROOT, "reports", "eda_summary_metrics.csv")

os.makedirs(os.path.join(PROJECT_ROOT, "data", "processed"), exist_ok=True)
os.makedirs(FIGURES_DIR, exist_ok=True)

def run_cleaning_and_eda():
    print("=" * 80)
    print("PHASE 2: DATA CLEANING & EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 80)

    # 1. Load Data
    print("\n[STEP 1] Loading raw dataset...")
    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Loaded {len(df):,} records and {df.shape[1]} columns.")

    # 2. Data Cleaning
    print("\n[STEP 2] Cleaning data types and handling whitespace anomalies...")
    
    # Identify whitespace in TotalCharges
    whitespace_mask = df['TotalCharges'].str.strip() == ''
    print(f"Found {whitespace_mask.sum()} rows with whitespace in 'TotalCharges'.")
    
    # For tenure == 0, TotalCharges is set to 0.0
    df.loc[whitespace_mask, 'TotalCharges'] = '0.0'
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
    print(f"'TotalCharges' successfully cast to {df['TotalCharges'].dtype}.")

    # 3. Feature Engineering for Analysis & BI
    print("\n[STEP 3] Feature Engineering...")
    
    # Binary numeric churn flag for easier aggregation (1 = Yes, 0 = No)
    df['ChurnNumeric'] = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)

    # Human-readable Senior Citizen label
    df['SeniorCitizen_Label'] = df['SeniorCitizen'].apply(lambda x: 'Yes' if x == 1 else 'No')

    # Tenure cohorts (standard telecom customer lifecycle brackets)
    tenure_bins = [-1, 12, 24, 48, 60, 72]
    tenure_labels = ['0-12 Mos', '13-24 Mos', '25-48 Mos', '49-60 Mos', '61-72 Mos']
    df['TenureCohort'] = pd.cut(df['tenure'], bins=tenure_bins, labels=tenure_labels)

    # Monthly charges spending tiers
    charge_bins = [0, 35, 70, 90, 150]
    charge_labels = ['Low (<$35)', 'Medium ($35-$70)', 'High ($70-$90)', 'Very High (>$90)']
    df['MonthlyChargeTier'] = pd.cut(df['MonthlyCharges'], bins=charge_bins, labels=charge_labels)

    print("Created features: 'ChurnNumeric', 'SeniorCitizen_Label', 'TenureCohort', 'MonthlyChargeTier'.")

    # 4. Core Baseline Metrics
    total_customers = len(df)
    churned_customers = df['ChurnNumeric'].sum()
    retained_customers = total_customers - churned_customers
    overall_churn_rate = (churned_customers / total_customers) * 100

    print("\n[STEP 4] Baseline KPIs:")
    print(f"   Total Customers     : {total_customers:,}")
    print(f"   Retained Customers  : {retained_customers:,} ({retained_customers / total_customers * 100:.2f}%)")
    print(f"   Churned Customers   : {churned_customers:,} ({overall_churn_rate:.2f}%)")
    print(f"   Overall Churn Rate  : {overall_churn_rate:.2f}%")

    # 5. Segmented Churn Analysis Function
    def calculate_segment_metrics(category_col):
        grouped = df.groupby(category_col).agg(
            Total_Customers=('customerID', 'count'),
            Churned_Customers=('ChurnNumeric', 'sum')
        ).reset_index()
        grouped['Retained_Customers'] = grouped['Total_Customers'] - grouped['Churned_Customers']
        grouped['Churn_Rate_%'] = (grouped['Churned_Customers'] / grouped['Total_Customers'] * 100).round(2)
        grouped['Customer_Share_%'] = (grouped['Total_Customers'] / total_customers * 100).round(2)
        return grouped

    categories_to_analyze = [
        'Contract',
        'TenureCohort',
        'InternetService',
        'PaymentMethod',
        'TechSupport',
        'OnlineSecurity',
        'PaperlessBilling',
        'MonthlyChargeTier',
        'SeniorCitizen_Label'
    ]

    all_summaries = []
    print("\n[STEP 5] Segmented Churn Highlights:")
    for cat in categories_to_analyze:
        summary = calculate_segment_metrics(cat)
        summary['Dimension'] = cat
        summary = summary.rename(columns={cat: 'Segment_Value'})
        all_summaries.append(summary[['Dimension', 'Segment_Value', 'Total_Customers', 'Churned_Customers', 'Churn_Rate_%', 'Customer_Share_%']])
        
        print(f"\n--- Dimension: {cat} ---")
        for _, row in summary.iterrows():
            print(f"   {str(row['Segment_Value']):25} | Customers: {row['Total_Customers']:5} | Churned: {row['Churned_Customers']:4} | Churn Rate: {row['Churn_Rate_%']:5.2f}%")

    # Export consolidated summary metrics table
    full_summary_df = pd.concat(all_summaries, ignore_index=True)
    full_summary_df.to_csv(SUMMARY_METRICS_PATH, index=False)
    print(f"\nConsolidated segment metrics exported to: {SUMMARY_METRICS_PATH}")

    # 6. Generate Readable Visualizations
    print("\n[STEP 6] Generating and saving charts...")

    # Color Palette definitions
    brand_blue = "#1f77b4"
    alert_red = "#d62728"
    retained_green = "#2ca02c"
    palette_duo = [retained_green, alert_red]

    # Chart 1: Overall Churn Distribution (Donut Chart)
    fig, ax = plt.subplots(figsize=(7, 5))
    sizes = [retained_customers, churned_customers]
    labels = [f"Retained\n({retained_customers:,} | {100 - overall_churn_rate:.1f}%)",
              f"Churned\n({churned_customers:,} | {overall_churn_rate:.1f}%)"]
    colors = [retained_green, alert_red]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
           wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2),
           textprops={'fontsize': 12, 'weight': 'bold'})
    ax.set_title("Overall Customer Churn Distribution (Total: 7,043)", fontsize=14, weight='bold', pad=15)
    plt.tight_layout()
    chart1_path = os.path.join(FIGURES_DIR, "01_overall_churn_distribution.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"Saved: {chart1_path}")

    # Chart 2: Churn by Contract Type
    contract_df = calculate_segment_metrics('Contract').sort_values('Churn_Rate_%', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(contract_df['Contract'], contract_df['Churn_Rate_%'], color=['#d95f02', '#7570b3', '#1b9e77'], width=0.55, edgecolor='black', linewidth=0.8)
    ax.axhline(overall_churn_rate, color='red', linestyle='--', linewidth=1.5, label=f'Avg Churn Rate ({overall_churn_rate:.1f}%)')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, weight='bold')
    ax.set_title("Customer Churn Rate by Contract Type", fontsize=14, weight='bold', pad=15)
    ax.set_ylabel("Churn Rate (%)", fontsize=12)
    ax.set_xlabel("Contract Type", fontsize=12)
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right')
    plt.tight_layout()
    chart2_path = os.path.join(FIGURES_DIR, "02_churn_by_contract_type.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"Saved: {chart2_path}")

    # Chart 3: Churn by Tenure Cohort
    tenure_df = calculate_segment_metrics('TenureCohort')
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(tenure_df['TenureCohort'], tenure_df['Churn_Rate_%'], color='#4575b4', width=0.6, edgecolor='black', linewidth=0.8)
    ax.axhline(overall_churn_rate, color='red', linestyle='--', linewidth=1.5, label=f'Avg Churn Rate ({overall_churn_rate:.1f}%)')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, weight='bold')
    ax.set_title("Customer Churn Rate by Tenure Cohort (Early Attrition Risk)", fontsize=14, weight='bold', pad=15)
    ax.set_ylabel("Churn Rate (%)", fontsize=12)
    ax.set_xlabel("Tenure Bracket", fontsize=12)
    ax.set_ylim(0, 55)
    ax.legend(loc='upper right')
    plt.tight_layout()
    chart3_path = os.path.join(FIGURES_DIR, "03_churn_by_tenure_cohort.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(f"Saved: {chart3_path}")

    # Chart 4: Churn by Payment Method
    pm_df = calculate_segment_metrics('PaymentMethod').sort_values('Churn_Rate_%', ascending=True)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    bars = ax.barh(pm_df['PaymentMethod'], pm_df['Churn_Rate_%'], color=['#313695', '#4575b4', '#abd9e9', '#d73027'], height=0.6, edgecolor='black', linewidth=0.8)
    ax.axvline(overall_churn_rate, color='black', linestyle='--', linewidth=1.5, label=f'Avg Churn Rate ({overall_churn_rate:.1f}%)')
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f"{width:.1f}%",
                    xy=(width, bar.get_y() + bar.get_height() / 2),
                    xytext=(5, 0), textcoords="offset points",
                    ha='left', va='center', fontsize=11, weight='bold')
    ax.set_title("Customer Churn Rate by Payment Method", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Churn Rate (%)", fontsize=12)
    ax.set_xlim(0, 55)
    ax.legend(loc='lower right')
    plt.tight_layout()
    chart4_path = os.path.join(FIGURES_DIR, "04_churn_by_payment_method.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(f"Saved: {chart4_path}")

    # Chart 5: Monthly Charges Density Distribution (Retained vs Churned)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.kdeplot(df[df['Churn'] == 'No']['MonthlyCharges'], ax=ax, label='Retained Customers', fill=True, color='forestgreen', alpha=0.35, linewidth=2)
    sns.kdeplot(df[df['Churn'] == 'Yes']['MonthlyCharges'], ax=ax, label='Churned Customers', fill=True, color='crimson', alpha=0.35, linewidth=2)
    ax.axvline(df[df['Churn'] == 'No']['MonthlyCharges'].median(), color='forestgreen', linestyle=':', label=f"Retained Median: ${df[df['Churn'] == 'No']['MonthlyCharges'].median():.1f}")
    ax.axvline(df[df['Churn'] == 'Yes']['MonthlyCharges'].median(), color='crimson', linestyle=':', label=f"Churned Median: ${df[df['Churn'] == 'Yes']['MonthlyCharges'].median():.1f}")
    ax.set_title("Distribution of Monthly Charges ($) by Churn Status", fontsize=14, weight='bold', pad=15)
    ax.set_xlabel("Monthly Charges ($)", fontsize=12)
    ax.set_ylabel("Density", fontsize=12)
    ax.legend(loc='upper right')
    plt.tight_layout()
    chart5_path = os.path.join(FIGURES_DIR, "05_monthly_charges_distribution_by_churn.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(f"Saved: {chart5_path}")

    # Chart 6: Churn by Internet Service Provider
    isp_df = calculate_segment_metrics('InternetService').sort_values('Churn_Rate_%', ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(isp_df['InternetService'], isp_df['Churn_Rate_%'], color=['#e41a1c', '#377eb8', '#4daf4a'], width=0.55, edgecolor='black', linewidth=0.8)
    ax.axhline(overall_churn_rate, color='red', linestyle='--', linewidth=1.5, label=f'Avg Churn Rate ({overall_churn_rate:.1f}%)')
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, weight='bold')
    ax.set_title("Customer Churn Rate by Internet Service Type", fontsize=14, weight='bold', pad=15)
    ax.set_ylabel("Churn Rate (%)", fontsize=12)
    ax.set_xlabel("Internet Service Provider", fontsize=12)
    ax.set_ylim(0, 50)
    ax.legend(loc='upper right')
    plt.tight_layout()
    chart6_path = os.path.join(FIGURES_DIR, "06_churn_by_internet_service.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(f"Saved: {chart6_path}")

    # 7. Export Cleaned Dataset
    print("\n[STEP 7] Exporting cleaned dataset to data/processed/...")
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"[SUCCESS] Cleaned dataset saved to: {PROCESSED_DATA_PATH}")
    print(f"Processed shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
    print(f"Nulls in processed data: {df.isnull().sum().sum()}")
    print("\n" + "=" * 80)
    print("PHASE 2 COMPLETE: Cleaned data and visualizations ready.")
    print("=" * 80)

if __name__ == "__main__":
    run_cleaning_and_eda()
