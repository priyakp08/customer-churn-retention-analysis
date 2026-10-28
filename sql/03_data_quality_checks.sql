-- ============================================================================
-- Script: 03_data_quality_checks.sql
-- Project: Customer Churn & Retention Analysis
-- Environment: MySQL Workbench
-- Purpose: Post-load data quality, constraint verification, and sanity checks.
-- ============================================================================

USE telco_churn_db;

-- 1. Verify Total Record Count (Expected: 7,043)
SELECT 
    COUNT(*) AS total_rows_loaded,
    CASE 
        WHEN COUNT(*) = 7043 THEN 'PASS: Record count matches benchmark (7,043)'
        ELSE 'FAIL: Row count mismatch'
    END AS validation_status
FROM customer_churn;

-- 2. Verify Primary Key Uniqueness (Expected: 0 duplicates)
SELECT 
    customer_id, 
    COUNT(*) AS occurrence_count
FROM customer_churn
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- 3. Check for NULL Values Across Key Analytical Fields
SELECT 
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN contract IS NULL THEN 1 ELSE 0 END) AS null_contract,
    SUM(CASE WHEN tenure IS NULL THEN 1 ELSE 0 END) AS null_tenure,
    SUM(CASE WHEN monthly_charges IS NULL THEN 1 ELSE 0 END) AS null_monthly_charges,
    SUM(CASE WHEN total_charges IS NULL THEN 1 ELSE 0 END) AS null_total_charges,
    SUM(CASE WHEN churn IS NULL THEN 1 ELSE 0 END) AS null_churn
FROM customer_churn;

-- 4. Verify TotalCharges Handling for Tenure = 0 Customers (Expected: 11 rows, TotalCharges = 0.0)
SELECT 
    customer_id, 
    tenure, 
    monthly_charges, 
    total_charges, 
    churn
FROM customer_churn
WHERE tenure = 0;

-- 5. Verify Target Variable Domain Values (Expected: 'No': 5,174 | 'Yes': 1,869)
SELECT 
    churn,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_churn), 2) AS percentage
FROM customer_churn
GROUP BY churn;
