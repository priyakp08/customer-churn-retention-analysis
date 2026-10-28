# Interview Preparation Guide: Customer Churn & Retention Analysis

This guide prepares you to speak confidently about this project in Data Analyst, Business Analyst, and Reporting Analyst interviews.

---

## 1. Project Walkthrough & Storytelling

### Q1: Can you walk me through your Customer Churn & Retention Analysis project?
**Answer (STAR Method):**
- **Situation**: Telecommunications companies face recurring subscription churn, which erodes Monthly Recurring Revenue (MRR) and increases customer acquisition costs. I wanted to analyze an authentic telecom customer dataset (IBM Telco Churn, 7,043 customers) to diagnose attrition drivers and provide data-backed retention strategies.
- **Task**: Clean the raw dataset, perform exploratory data analysis in Python, build robust analytical queries in MySQL using CTEs and Window Functions, construct a 2-page interactive executive dashboard in Power BI, and formulate testable business recommendations.
- **Action**: 
  - In **Python**, I uncovered a hidden whitespace issue in `TotalCharges` (11 rows with `tenure = 0`), imputed `0.0`, engineered tenure cohorts and spending tiers, and calculated a baseline churn rate of **26.54%**.
  - In **MySQL**, I created the schema and wrote queries using CTEs and Window Functions to segment high-risk customers and quantify cumulative churn.
  - In **Power BI**, I created a dedicated `_Measures` table with 12 DAX calculations (such as `Lost Monthly Revenue` and `High-Risk Cohort Churn Rate`) and built an executive overview and diagnostic retention page.
  - In **Excel**, I reconciled all metrics into a multi-tab summary workbook.
- **Result**: I isolated a high-risk customer profile (Month-to-month + Fiber Optic + Electronic Check + First-year tenure) suffering from an acute **71.16% churn rate**, representing **$14,768.95 in monthly revenue at immediate risk**, and designed 4 testable retention interventions to mitigate this attrition.

---

## 2. Technical Python & Data Wrangling

### Q2: Did you encounter any data quality issues during ingestion, and how did you resolve them?
**Answer:**
Yes. When inspecting `TotalCharges`, it was typed as an `object` (string) despite containing monetary values. A standard `df.isnull().sum()` showed 0 nulls. By running a whitespace detection script (`df['TotalCharges'].str.strip() == ''`), I identified **11 records** containing empty string values (`" "`).
Upon investigating these 11 rows, I found that **all 11 had `tenure = 0` months** and `Churn = 'No'`. They were brand new subscribers who had not yet completed a billing cycle. Dropping them or imputing with mean/median would distort the data. Therefore, I imputed them with `0.0` and cast `TotalCharges` to `float64`, preserving all 7,043 customer accounts.

---

## 3. Technical SQL & Database Architecture

### Q3: How did you use a Common Table Expression (CTE) in your SQL analysis?
**Answer:**
I used a CTE to isolate and analyze multi-condition customer cohorts. In Query 7, I created a CTE called `high_risk_cohort` filtering customers on `contract = 'Month-to-month'`, `internet_service = 'Fiber optic'`, `payment_method = 'Electronic check'`, and `tenure <= 12`.
From this CTE, I aggregated both historical attrition (449 churned out of 631 = **71.16% churn**) and active accounts currently in jeopardy (182 active customers), calculating the exact monthly recurring revenue at risk:
```sql
ROUND(SUM(CASE WHEN churn = 'No' THEN monthly_charges ELSE 0 END), 2) AS monthly_revenue_at_immediate_risk
```
Using a CTE kept the logic modular, readable, and reusable for executive reporting.

### Q4: Why did you use Window Functions like `DENSE_RANK()` and `SUM() OVER ()` instead of standard `GROUP BY`?
**Answer:**
A standard `GROUP BY` collapses rows into grouped aggregates, but cannot calculate running totals across groups without self-joins. By utilizing `DENSE_RANK() OVER (ORDER BY churned_customers DESC)` and `SUM(churned_customers) OVER (ORDER BY churned_customers DESC)`, I was able to rank segments by churn volume and simultaneously compute their cumulative contribution to company-wide churn.
This revealed that the top segment (`Month-to-month` + `Electronic check` + `Fiber optic`) accounted for **42.22% of all customer cancellations** by itself, and the top 6 segments accounted for **78.49% of all churn**.

---

## 4. Power BI & DAX Proficiency

### Q5: Explain the difference between Row Context and Filter Context using one of your DAX measures.
**Answer:**
- **Row Context** exists when iterating row-by-row (e.g., in a calculated column or inside iterator functions like `SUMX`).
- **Filter Context** is the set of active filters applied to the data model via visual fields, slicers, or page-level filters.
- In my measure:
  ```dax
  Lost Monthly Revenue = 
  CALCULATE(
      SUM(customer_churn[MonthlyCharges]),
      customer_churn[Churn] = "Yes"
  )
  ```
  `CALCULATE` modifies the existing Filter Context by overriding or adding the filter `Churn = "Yes"`. If an executive slices the dashboard by `Contract = "Month-to-month"`, the measure evaluates within the combined filter context of `Contract = "Month-to-month"` AND `Churn = "Yes"`.

---

## 5. Business Acumen & Analytical Judgment

### Q6: Customers paying by Electronic Check have a 45.3% churn rate compared to 15.2% for Credit Card auto-pay. Does this prove that electronic checks cause customers to leave?
**Answer:**
No. This is a crucial distinction between **correlation and causation**. Customers choosing electronic checks might have lower commitment, lower financial stability, or might have intentionally avoided auto-pay because they planned to cancel in the near future.
Rather than assuming causality, I proposed a controlled **A/B pilot campaign**: offer a $5/month discount to a random sample of electronic check users to enroll in automated billing. If the test group demonstrates a statistically significant decline in churn relative to the control group, we validate whether the payment friction itself was causal.

### Q7: What was the single most impactful finding regarding service add-ons?
**Answer:**
Customers with **neither** Tech Support nor Online Security had a **48.96% churn rate**. However, customers subscribing to **both** services churned at only **9.01%** — a **5.4x difference**. This suggests that value-add services create customer stickiness and digital switching barriers, making bundled offerings an effective retention mechanism.

### Q8: If leadership gave you a budget of $50,000 for retention, where would you allocate it?
**Answer:**
I would allocate the budget to the **182 active customers** in the high-risk cohort (Month-to-month, Fiber Optic, Electronic Check, Tenure < 12m), who represent **$14,769/month in revenue at risk** ($177K ARR):
1. Allocate **$10,000** toward a $50 contract-lock bill credit to migrate them from month-to-month to a 1-year agreement.
2. Allocate **$15,000** for a $5/mo auto-pay discount incentive.
3. Allocate **$25,000** to fund dedicated Customer Success onboarding specialists for new subscribers during their first 90 days, where over 55% of all cancellations occur.
