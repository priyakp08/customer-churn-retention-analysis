# Data Dictionary — IBM Telco Customer Churn

| # | Column Name | Description | Raw Data Type | Target Cleaned Type | Example Values / Value Set | Category |
|---|-------------|-------------|---------------|---------------------|----------------------------|----------|
| 1 | `customerID` | Unique identifier for each customer account | `object` (string) | `string` | `"7590-VHVEG"`, `"5575-GNVDE"` | Identity |
| 2 | `gender` | Customer gender | `object` (string) | `category` | `"Female"`, `"Male"` | Demographics |
| 3 | `SeniorCitizen` | Whether the customer is a senior citizen (65+) | `int64` | `category` (0 = No, 1 = Yes) | `0`, `1` | Demographics |
| 4 | `Partner` | Whether customer has a partner | `object` (string) | `category` | `"Yes"`, `"No"` | Demographics |
| 5 | `Dependents` | Whether customer lives with dependents | `object` (string) | `category` | `"Yes"`, `"No"` | Demographics |
| 6 | `tenure` | Number of months the customer has stayed with company | `int64` | `int64` | `0` to `72` months | Account/Usage |
| 7 | `PhoneService` | Whether customer has landline phone service | `object` (string) | `category` | `"Yes"`, `"No"` | Services |
| 8 | `MultipleLines` | Whether customer has multiple phone lines | `object` (string) | `category` | `"No"`, `"Yes"`, `"No phone service"` | Services |
| 9 | `InternetService` | Customer internet service provider technology | `object` (string) | `category` | `"DSL"`, `"Fiber optic"`, `"No"` | Services |
| 10 | `OnlineSecurity` | Whether customer has online security add-on | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 11 | `OnlineBackup` | Whether customer has online backup add-on | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 12 | `DeviceProtection` | Whether customer has device protection plan | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 13 | `TechSupport` | Whether customer has premium tech support add-on | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 14 | `StreamingTV` | Whether customer subscribes to streaming TV | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 15 | `StreamingMovies` | Whether customer subscribes to streaming movies | `object` (string) | `category` | `"Yes"`, `"No"`, `"No internet service"` | Add-ons |
| 16 | `Contract` | Customer contract billing term | `object` (string) | `category` | `"Month-to-month"`, `"One year"`, `"Two year"` | Account/Contract |
| 17 | `PaperlessBilling` | Whether customer is enrolled in paperless e-billing | `object` (string) | `category` | `"Yes"`, `"No"` | Billing |
| 18 | `PaymentMethod` | Customer payment channel | `object` (string) | `category` | `"Electronic check"`, `"Mailed check"`, `"Bank transfer (automatic)"`, `"Credit card (automatic)"` | Billing |
| 19 | `MonthlyCharges` | Current monthly billed amount (in USD) | `float64` | `float64` | `18.25` to `118.75` | Financial |
| 20 | `TotalCharges` | Cumulative charges billed across customer lifetime | `object` (string) | `float64` (11 blanks converted to 0.0) | `18.80` to `8684.80` | Financial |
| 21 | `Churn` | Target Variable: Whether customer cancelled service within past month | `object` (string) | `category` / binary | `"No"`, `"Yes"` | Target |
