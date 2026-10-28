-- ============================================================================
-- Script: 02_data_import_instructions.sql
-- Project: Customer Churn & Retention Analysis
-- Environment: MySQL Workbench / MySQL Server 8.0+
-- Purpose: Complete instructions for loading processed data into MySQL.
-- ============================================================================

USE telco_churn_db;

/*
==============================================================================
METHOD 1: MySQL Workbench Table Data Import Wizard (Recommended for Beginners)
==============================================================================
1. Open MySQL Workbench and connect to your local MySQL instance.
2. In the "Schemas" panel on the left, expand `telco_churn_db`.
3. Right-click on `Tables` (or right-click `customer_churn`) -> Select "Table Data Import Wizard".
4. File Path: Browse to the processed CSV:
   C:\Users\priya\.gemini\antigravity\scratch\customer-churn-retention-analysis\data\processed\telco_churn_cleaned.csv
5. Select "Use existing table" -> choose `customer_churn`.
6. Match column names from CSV headers to SQL columns:
   customerID          -> customer_id
   gender              -> gender
   SeniorCitizen       -> senior_citizen
   Partner             -> partner
   Dependents          -> dependents
   tenure              -> tenure
   PhoneService        -> phone_service
   MultipleLines       -> multiple_lines
   InternetService     -> internet_service
   OnlineSecurity      -> online_security
   OnlineBackup        -> online_backup
   DeviceProtection    -> device_protection
   TechSupport         -> tech_support
   StreamingTV         -> streaming_tv
   StreamingMovies     -> streaming_movies
   Contract            -> contract
   PaperlessBilling    -> paperless_billing
   PaymentMethod       -> payment_method
   MonthlyCharges      -> monthly_charges
   TotalCharges        -> total_charges
   Churn               -> churn
   ChurnNumeric        -> churn_numeric
   SeniorCitizen_Label -> senior_citizen_label
   TenureCohort        -> tenure_cohort
   MonthlyChargeTier   -> monthly_charge_tier
7. Click "Next" -> "Next" to execute import.
8. Verify that 7,043 records are imported.
==============================================================================
*/

/*
==============================================================================
METHOD 2: Fast Command-Line LOAD DATA INFILE (For Advanced Users)
==============================================================================
Note: Requires local_infile to be ON.
*/

-- Enable local file loading in session
SET GLOBAL local_infile = 1;

-- If using secure-file-priv directory, copy the CSV there or load directly:
LOAD DATA LOCAL INFILE 'C:/Users/priya/.gemini/antigravity/scratch/customer-churn-retention-analysis/data/processed/telco_churn_cleaned.csv'
INTO TABLE customer_churn
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(
    customer_id, gender, senior_citizen, partner, dependents, tenure,
    phone_service, multiple_lines, internet_service, online_security,
    online_backup, device_protection, tech_support, streaming_tv,
    streaming_movies, contract, paperless_billing, payment_method,
    monthly_charges, total_charges, churn, churn_numeric,
    senior_citizen_label, tenure_cohort, monthly_charge_tier
);
