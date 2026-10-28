"""
Script: run_sql_analysis.py
Project: Customer Churn & Retention Analysis
Description:
    Loads the cleaned dataset into an in-memory SQL database (SQLite/MySQL compliant),
    executes all analytical SQL queries, validates query performance, and displays
    the exact formatted query output tables for Phase 3 documentation.
"""

import os
import sqlite3
import pandas as pd

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "telco_churn_cleaned.csv")

def run_sql_queries():
    print("=" * 90)
    print("PHASE 3: SQL ANALYSIS EXECUTION & VALIDATION")
    print("=" * 90)

    # 1. Load Cleaned Dataset into SQL Table
    df = pd.read_csv(PROCESSED_DATA_PATH)
    
    # Rename columns to match MySQL snake_case schema
    column_mapping = {
        'customerID': 'customer_id',
        'gender': 'gender',
        'SeniorCitizen': 'senior_citizen',
        'Partner': 'partner',
        'Dependents': 'dependents',
        'tenure': 'tenure',
        'PhoneService': 'phone_service',
        'MultipleLines': 'multiple_lines',
        'InternetService': 'internet_service',
        'OnlineSecurity': 'online_security',
        'OnlineBackup': 'online_backup',
        'DeviceProtection': 'device_protection',
        'TechSupport': 'tech_support',
        'StreamingTV': 'streaming_tv',
        'StreamingMovies': 'streaming_movies',
        'Contract': 'contract',
        'PaperlessBilling': 'paperless_billing',
        'PaymentMethod': 'payment_method',
        'MonthlyCharges': 'monthly_charges',
        'TotalCharges': 'total_charges',
        'Churn': 'churn',
        'ChurnNumeric': 'churn_numeric',
        'SeniorCitizen_Label': 'senior_citizen_label',
        'TenureCohort': 'tenure_cohort',
        'MonthlyChargeTier': 'monthly_charge_tier'
    }
    df = df.rename(columns=column_mapping)

    conn = sqlite3.connect(":memory:")
    df.to_sql("customer_churn", conn, index=False, if_exists="replace")
    print(f"[INFO] In-memory database initialized with table 'customer_churn' ({len(df):,} rows).")

    # Define the 8 SQL queries
    queries = [
        ("QUERY 1: Executive KPI Summary", """
            SELECT 
                COUNT(*) AS total_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS retention_rate_pct
            FROM customer_churn;
        """),
        ("QUERY 2: Churn by Contract Type", """
            SELECT 
                contract,
                COUNT(*) AS total_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / (SELECT COUNT(*) FROM customer_churn WHERE churn = 'Yes'), 2) AS share_of_total_churn_pct
            FROM customer_churn
            GROUP BY contract
            ORDER BY churn_rate_pct DESC;
        """),
        ("QUERY 3: Churn by Payment Method", """
            SELECT 
                payment_method,
                COUNT(*) AS total_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                CASE 
                    WHEN payment_method LIKE '%automatic%' THEN 'Automated Payment'
                    ELSE 'Manual Payment'
                END AS payment_category
            FROM customer_churn
            GROUP BY payment_method
            ORDER BY churn_rate_pct DESC;
        """),
        ("QUERY 4: Churn by Tenure Cohort", """
            SELECT 
                CASE 
                    WHEN tenure <= 12 THEN '0 - 12 Months'
                    WHEN tenure <= 24 THEN '13 - 24 Months'
                    WHEN tenure <= 48 THEN '25 - 48 Months'
                    WHEN tenure <= 60 THEN '49 - 60 Months'
                    ELSE '61 - 72 Months'
                END AS tenure_group,
                COUNT(*) AS total_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / (SELECT COUNT(*) FROM customer_churn WHERE churn = 'Yes'), 2) AS share_of_total_churn_pct
            FROM customer_churn
            GROUP BY tenure_group
            ORDER BY MIN(tenure) ASC;
        """),
        ("QUERY 5: Monthly and Total Charges Analysis", """
            SELECT 
                churn,
                COUNT(*) AS customer_count,
                ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
                ROUND(MIN(monthly_charges), 2) AS min_monthly_charges,
                ROUND(MAX(monthly_charges), 2) AS max_monthly_charges,
                ROUND(AVG(total_charges), 2) AS avg_total_charges,
                ROUND(SUM(monthly_charges), 2) AS total_monthly_revenue,
                ROUND(SUM(total_charges), 2) AS total_lifetime_revenue
            FROM customer_churn
            GROUP BY churn;
        """),
        ("QUERY 6: Service Add-ons Impact (Online Security & Tech Support)", """
            SELECT 
                tech_support,
                online_security,
                COUNT(*) AS total_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
            FROM customer_churn
            WHERE internet_service != 'No'
            GROUP BY tech_support, online_security
            ORDER BY churn_rate_pct DESC;
        """),
        ("QUERY 7: High-Risk Customer Profile (CTE)", """
            WITH high_risk_cohort AS (
                SELECT 
                    customer_id,
                    tenure,
                    monthly_charges,
                    contract,
                    internet_service,
                    payment_method,
                    churn
                FROM customer_churn
                WHERE contract = 'Month-to-month'
                  AND internet_service = 'Fiber optic'
                  AND payment_method = 'Electronic check'
                  AND tenure <= 12
            )
            SELECT 
                COUNT(*) AS total_high_risk_customers,
                SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_in_cohort,
                SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS currently_active_high_risk,
                ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS cohort_churn_rate_pct,
                ROUND(SUM(CASE WHEN churn = 'No' THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_immediate_risk
            FROM high_risk_cohort;
        """),
        ("QUERY 8: Window Functions - Segment Ranking & Cumulative Churn Impact", """
            WITH segment_churn_summary AS (
                SELECT 
                    contract,
                    payment_method,
                    internet_service,
                    COUNT(*) AS total_customers,
                    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
                    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS segment_churn_rate_pct
                FROM customer_churn
                GROUP BY contract, payment_method, internet_service
            )
            SELECT 
                contract,
                payment_method,
                internet_service,
                total_customers,
                churned_customers,
                segment_churn_rate_pct,
                DENSE_RANK() OVER (ORDER BY churned_customers DESC) AS churn_rank,
                SUM(churned_customers) OVER (ORDER BY churned_customers DESC) AS cumulative_churned,
                ROUND(SUM(churned_customers) OVER (ORDER BY churned_customers DESC) * 100.0 / (SELECT SUM(churn_numeric) FROM customer_churn), 2) AS cumulative_pct_of_all_churn
            FROM segment_churn_summary
            ORDER BY churn_rank ASC
            LIMIT 6;
        """)
    ]

    for title, query in queries:
        print("\n" + "-" * 90)
        print(f"[{title}]")
        print("-" * 90)
        result_df = pd.read_sql_query(query, conn)
        print(result_df.to_string(index=False))

    conn.close()
    print("\n" + "=" * 90)
    print("ALL 8 SQL QUERIES EXECUTED AND VALIDATED SUCCESSFULLY!")
    print("=" * 90)

if __name__ == "__main__":
    run_sql_queries()
