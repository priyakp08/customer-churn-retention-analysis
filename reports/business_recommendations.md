# Executive Business Recommendations: Customer Churn & Retention Strategy

**Project:** Customer Churn & Retention Analysis  
**Analyst:** Senior Data Analyst Portfolio Project  
**Target Stakeholders:** VP of Customer Experience, Chief Commercial Officer (CCO), Head of Retention  
**Dataset Basis:** IBM Telco Customer Churn (7,043 Accounts, 26.54% Baseline Churn Rate)  

---

## 1. Executive Summary & Diagnostic Findings

During our analysis across Python, MySQL, Power BI, and Excel, we analyzed 7,043 customer accounts and identified an overall customer churn rate of **26.54%** (1,869 churned accounts). This attrition represents a direct recurring revenue loss of **$139,130.85 per month** ($1.67M Annual Recurring Revenue - ARR).

Our analysis identified four primary drivers heavily associated with customer attrition:
1. **Contract Flexibility vs Commitment**: Month-to-month contracts exhibit a **42.71% churn rate**, generating **88.55% of all cancellations** across the business.
2. **The "First-Year Fragility" Window**: **55.48% of all churn** occurs in the first 12 months (`0-12 Mos` tenure churn rate is **47.44%**), plummeting to **6.61%** after year 5.
3. **Payment Channel Friction**: Customers paying via manual **Electronic Check** churn at **45.29%**, compared to only **15.24%** for automatic credit card billing.
4. **Service Add-on Deficit**: Customers without Tech Support and Online Security churn at **48.96%**, compared to just **9.01%** for customers subscribed to both services (**5.4x difference**).

---

## 2. Core Business Questions Answered

### Question 1: Which customer groups have the highest churn rate?
- **High-Risk Segment Profile**: Customers on Month-to-month contracts subscribing to Fiber Optic internet, paying via Electronic Check, with less than 12 months tenure, experience an acute **71.16% churn rate**.
- **Senior Citizens**: Churn at **41.68%** vs. **23.61%** for non-seniors.
- **Single / Independent Accounts**: Customers without partners (32.96% churn) or without dependents (31.28% churn) leave at nearly double the rate of families (14.33% churn for customers with dependents).

### Question 2: Which contract types are associated with higher churn?
- **Month-to-month**: **42.71%** churn rate (1,655 churned accounts).
- **One-year**: **11.27%** churn rate (166 churned accounts).
- **Two-year**: **2.83%** churn rate (48 churned accounts).
- *Finding*: A two-year customer is **15 times less likely to churn** than a month-to-month customer.

### Question 3: How do tenure and monthly charges relate to churn?
- **Tenure**: Inversely associated with churn. Attrition is heavily front-loaded:
  - 0–12 Mos: 47.44%
  - 13–24 Mos: 28.71%
  - 25–48 Mos: 20.39%
  - 49–60 Mos: 14.42%
  - 61–72 Mos: 6.61%
- **Monthly Charges**: Positively associated with churn. Churned customers paid an average of **$74.44/month** compared to **$61.27/month** for retained customers (+21.5% higher bills). Customers in the $70–$90 monthly tier showed the peak churn rate (**37.80%**).

### Question 4: Which customer segments should the business prioritize for retention?
The business must prioritize the **182 active customers** currently matching the high-risk cohort:
- Contract: Month-to-month
- Service: Fiber optic
- Payment: Electronic check
- Tenure: 0 to 12 months
- **Revenue at Immediate Risk**: **$14,768.95 per month** ($177,227.40 ARR).

---

## 3. Four Practical, Testable Retention Actions

> [!IMPORTANT]
> **Correlation vs. Causation Notice**:
> The observed patterns demonstrate strong statistical associations, not definitive causal proof. For example, paying by Electronic Check does not necessarily *cause* a customer to cancel; it may reflect lower commitment, transactional friction, or customers already planning to switch providers. Therefore, all recommendations are designed as **controlled A/B pilot tests** rather than blanket operational mandates.

### Initiative 1: The "First 90 Days" Onboarding Guardrail
- **Target**: New sign-ups in tenure months 0–3.
- **Action**: Implement proactive customer success check-ins at Day 14, Day 45, and Day 75 (speed test verification, equipment setup assistance, satisfaction pulse survey).
- **Business Goal**: Reduce early drop-off by catching setup friction before billing frustration occurs.
- **KPI to Measure**: 90-day retention rate (+10% target).

### Initiative 2: Auto-Pay Transition Incentive ("$5 Off Auto-Pay")
- **Target**: The 2,365 customers currently paying via manual Electronic Check.
- **Action**: Offer an ongoing $5/month billing discount for enrolling in recurring Credit Card or Bank Transfer Auto-Pay.
- **Business Rationale**: Retained automated customers churn at ~15% compared to 45% for manual checks. Even if the discount costs $5/mo, retaining a $75/mo customer yields an immediate net positive margin.
- **Test Setup**: Offer discount to a 50% test sample of e-check users; measure conversion and 6-month churn.

### Initiative 3: Complimentary Tech Support & Security Bundle Adoption
- **Target**: Fiber optic customers who opted out of value add-ons.
- **Action**: Provide a complimentary 90-day trial of **Tech Support** and **Online Security** with digital setup assistance.
- **Business Rationale**: Customers with both services churn at only **9.01%** (vs. 48.96% for neither). Value-added services increase product stickiness and perceived utility.
- **Test Setup**: Offer trial upon Fiber Optic activation; measure retention difference at Month 6.

### Initiative 4: Month-to-Month Contract Conversion Campaign
- **Target**: Active month-to-month subscribers with tenure between 6 and 12 months.
- **Action**: Offer a one-time $50 account bill credit or upgraded bandwidth tier in exchange for switching to a 1-year annual agreement.
- **Business Rationale**: Shifting a customer from month-to-month (42.7% churn) to a 1-year contract (11.3% churn) secures predictable cash flow and cuts attrition risk by nearly 75%.
