# Data Validation, Assumptions & Analytical Limitations

**Project:** Customer Churn & Retention Analysis  
**Benchmark Dataset:** IBM Telco Customer Churn (7,043 Records)  

---

## 1. Cross-Tool Metric Reconciliation Table

To ensure analytical integrity across the data pipeline, all core metrics were independently calculated and reconciled across **Python (Pandas)**, **SQL (MySQL)**, **Power BI (DAX)**, and **Excel (Pivot Tables & Formulas)**.

| Analytical Metric | Python (Pandas) | SQL (MySQL) | Power BI (DAX) | Excel Workbook | Reconciliation Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Customers** | `7,043` | `7,043` | `7,043` | `7,043` | **100% Match** |
| **Retained Customers** | `5,174` | `5,174` | `5,174` | `5,174` | **100% Match** |
| **Churned Customers** | `1,869` | `1,869` | `1,869` | `1,869` | **100% Match** |
| **Overall Churn Rate** | `26.54%` | `26.54%` | `26.54%` | `26.54%` | **100% Match** |
| **Overall Retention Rate** | `73.46%` | `73.46%` | `73.46%` | `73.46%` | **100% Match** |
| **Month-to-Month Churn Rate** | `42.71%` | `42.71%` | `42.71%` | `42.71%` | **100% Match** |
| **One-Year Contract Churn Rate**| `11.27%` | `11.27%` | `11.27%` | `11.27%` | **100% Match** |
| **Two-Year Contract Churn Rate**| `2.83%` | `2.83%` | `2.83%` | `2.83%` | **100% Match** |
| **0–12 Mos Tenure Churn Rate** | `47.44%` | `47.44%` | `47.44%` | `47.44%` | **100% Match** |
| **Electronic Check Churn Rate** | `45.29%` | `45.29%` | `45.29%` | `45.29%` | **100% Match** |
| **Active Monthly Revenue (MRR)**| `$316,985.75` | `$316,985.75` | `$316.99K` | `$316,985.75` | **100% Match** |
| **Lost Monthly Revenue (Churn)**| `$139,130.85` | `$139,130.85` | `$139.13K` | `$139,130.85` | **100% Match** |
| **High-Risk Segment Churn Rate**| `71.16%` | `71.16%` | `71.16%` | `71.16%` | **100% Match** |
| **Immediate MRR at Risk** | `$14,768.95` | `$14,768.95` | `$14.77K` | `$14,768.95` | **100% Match** |

---

## 2. Analytical Assumptions

1. **`TotalCharges` for `tenure = 0`**:
   - The 11 records with whitespace strings (`" "`) were imputed with `0.0` rather than dropped or filled with mean/median.
   - *Rationale*: A customer who has completed 0 months has received 0 monthly billing cycles. Imputing with zero accurately represents cumulative historical payments and avoids artificially biasing tenure or lifetime revenue metrics.
2. **Snapshot Nature of Data**:
   - The dataset represents a historical cross-sectional snapshot of an active telecom subscriber base over a single observation window (last month churn).
   - Inactive/churned accounts are treated as mutually exclusive with retained accounts during the snapshot period.
3. **Revenue Interpretation**:
   - `MonthlyCharges` reflects the current contractual monthly fee. `TotalCharges` reflects cumulative historical billings. Lost MRR is defined as the sum of `MonthlyCharges` for customers where `Churn = 'Yes'`.

---

## 3. Analytical Limitations

1. **Observational vs Causal Data**:
   - The dataset does not originate from a randomized controlled trial (A/B experiment). Observed patterns (e.g., electronic check churn vs credit card churn) are statistical correlations, not deterministic proof that the payment channel itself induces churn.
2. **Absence of Customer Service Interaction Data**:
   - The dataset does not record inbound customer support call logs, ticket resolution times, or network outage telemetry, which are known real-world drivers of telecom customer dissatisfaction.
3. **Static Pricing Information**:
   - The dataset records current monthly charges but does not track price increases, promotions expiring, or historical bill shocks that may have preceded cancellation.
