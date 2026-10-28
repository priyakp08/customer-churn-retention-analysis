-- ============================================================================
-- Script: 04_business_churn_analysis.sql
-- Project: Customer Churn & Retention Analysis
-- Environment: MySQL Workbench
-- Purpose: Complete business analysis answering core retention questions
--          using Aggregations, CASE statements, CTEs, and Window Functions.
-- ============================================================================

USE telco_churn_db;

-- ----------------------------------------------------------------------------
-- QUERY 1: Overall Executive KPI Summary
-- Business Goal: Baseline health check on total volume and attrition rate.
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS retention_rate_pct
FROM customer_churn;


-- ----------------------------------------------------------------------------
-- QUERY 2: Churn by Contract Type
-- Business Goal: Measure contract commitment impact and identify largest churn source.
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 3: Churn by Payment Method
-- Business Goal: Compare friction and churn rates across payment channels.
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 4: Churn by Tenure Cohorts (Using CASE WHEN)
-- Business Goal: Pinpoint at what lifecycle stage customers drop off.
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 5: Monthly and Total Charges Analysis
-- Business Goal: Quantify financial sensitivity and lost revenue.
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 6: Customer Retention by Service Add-ons (Tech Support & Online Security)
-- Business Goal: Evaluate whether support and security services enhance stickiness.
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 7: High-Risk Customer Segmentation (Using CTE)
-- Business Goal: Identify and quantify customers matching the highest-risk profile:
--                (Month-to-month + Fiber Optic + Electronic Check + Tenure <= 12 Mos).
-- ----------------------------------------------------------------------------
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


-- ----------------------------------------------------------------------------
-- QUERY 8: Window Functions — Segment Ranking and Cumulative Churn Impact
-- Business Goal: Rank customer segments by volume of churn and calculate
--                running cumulative contribution to total churn.
-- ----------------------------------------------------------------------------
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
    DENSE_RANK() OVER (ORDER BY churned_customers DESC) AS churn_volume_rank,
    SUM(churned_customers) OVER (ORDER BY churned_customers DESC) AS cumulative_churned_customers,
    ROUND(SUM(churned_customers) OVER (ORDER BY churned_customers DESC) * 100.0 / (SELECT SUM(churn_numeric) FROM customer_churn), 2) AS cumulative_pct_of_all_churn
FROM segment_churn_summary
ORDER BY churn_volume_rank ASC
LIMIT 10;
