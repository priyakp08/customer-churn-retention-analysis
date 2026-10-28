-- ============================================================================
-- Script: 01_database_and_table_setup.sql
-- Project: Customer Churn & Retention Analysis
-- Environment: MySQL 8.0+ / MySQL Workbench
-- Purpose: Creates the database schema and table for Telco Customer Churn data.
-- ============================================================================

-- Step 1: Create Database
CREATE DATABASE IF NOT EXISTS telco_churn_db;
USE telco_churn_db;

-- Step 2: Drop existing table if recreating
DROP TABLE IF EXISTS customer_churn;

-- Step 3: Create Table with Appropriate Data Types and Constraints
CREATE TABLE customer_churn (
    customer_id          VARCHAR(20)    PRIMARY KEY,
    gender               VARCHAR(10)    NOT NULL,
    senior_citizen       TINYINT        NOT NULL,
    partner              VARCHAR(5)     NOT NULL,
    dependents           VARCHAR(5)     NOT NULL,
    tenure               INT            NOT NULL,
    phone_service        VARCHAR(5)     NOT NULL,
    multiple_lines       VARCHAR(25)    NOT NULL,
    internet_service     VARCHAR(25)    NOT NULL,
    online_security      VARCHAR(25)    NOT NULL,
    online_backup        VARCHAR(25)    NOT NULL,
    device_protection    VARCHAR(25)    NOT NULL,
    tech_support         VARCHAR(25)    NOT NULL,
    streaming_tv         VARCHAR(25)    NOT NULL,
    streaming_movies     VARCHAR(25)    NOT NULL,
    contract             VARCHAR(25)    NOT NULL,
    paperless_billing    VARCHAR(5)     NOT NULL,
    payment_method       VARCHAR(35)    NOT NULL,
    monthly_charges      DECIMAL(10,2)  NOT NULL,
    total_charges        DECIMAL(10,2)  NOT NULL,
    churn                VARCHAR(5)     NOT NULL,
    churn_numeric        TINYINT        NOT NULL,
    senior_citizen_label VARCHAR(5)     NOT NULL,
    tenure_cohort        VARCHAR(20)    NOT NULL,
    monthly_charge_tier  VARCHAR(25)    NOT NULL
);

-- Show structure to verify
DESCRIBE customer_churn;
