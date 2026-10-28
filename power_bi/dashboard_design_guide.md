# Power BI Interactive Dashboard Design Guide

## Project: Customer Churn & Retention Analysis
This guide provides complete instructions to build, format, and publish the 2-page executive Power BI dashboard using the cleaned dataset.

---

## 1. Data Connection & Power Query Setup

1. Open **Power BI Desktop**.
2. Click **Get Data** -> Select **Text/CSV**.
3. Browse and select:
   `customer-churn-retention-analysis/data/processed/telco_churn_cleaned.csv`
4. In the preview dialog, click **Transform Data** to open the Power Query Editor.
5. Verify column data types:
   - `customerID`: Text
   - `tenure`: Whole Number
   - `MonthlyCharges`: Decimal Number
   - `TotalCharges`: Decimal Number
   - `ChurnNumeric`: Whole Number
   - `Contract`, `PaymentMethod`, `InternetService`: Text
6. Click **Close & Apply**.

---

## 2. Dedicated Measures Table Setup (`_Measures`)

It is a corporate standard to keep all calculations organized in a dedicated measures table:
1. On the **Home** tab, click **Enter Data**.
2. Rename the table to `_Measures` and click **Load**.
3. For each measure in [`power_bi/dax_measures.dax`](power_bi/dax_measures.dax), click **New Measure**, paste the DAX formula, and set the format string (e.g., Currency `$#,##0.00`, Percentage `0.0%`, Whole Number `#,##0`).
4. Delete the empty default `Column1` from `_Measures`.

---

## 3. Design Specifications & Canvas Theme

- **Canvas Size**: 16:9 Standard (`1280 x 720` px)
- **Background Color**: `#F8F9FA` (Clean Off-White)
- **Primary Corporate Color**: `#1B365D` (Deep Navy Blue)
- **Accent Alert / Churn**: `#E63946` (Crimson Red)
- **Accent Retained**: `#2A9D8F` (Teal Green)
- **Neutral Cards**: `#FFFFFF` (Pure White with subtle drop shadow)

---

## 4. Page 1: Churn Overview Layout

### Header Banner (Top: Y=0, H=70, W=1280)
- **Title**: `Customer Churn & Retention Analysis | Executive Overview`
- **Subtitle**: `Monitoring Attrition Patterns, Contract Commitments & Payment Channels`

### Top KPI Summary Cards (Y=80, H=90)
Place 4 Card visuals horizontally:
1. **Total Customers**: Card visual -> Field: `[Total Customers]` (Display: `7,043`)
2. **Retained Customers**: Card visual -> Field: `[Retained Customers]` (Display: `5,174 | 73.5%`) -> Accent Green
3. **Churned Customers**: Card visual -> Field: `[Churned Customers]` (Display: `1,869 | 26.5%`) -> Accent Red
4. **Overall Churn Rate**: Card visual -> Field: `[Churn Rate %]` (Display: `26.5%`)

### Interactive Slicers (Left Sidebar or Top Strip: Y=180, W=220)
- **Internet Service Slicer**: `DSL`, `Fiber optic`, `No`
- **Senior Citizen Slicer**: `Yes`, `No`
- **Partner Slicer**: `Yes`, `No`

### Main Visuals Grid
1. **Visual 1 (Donut Chart)**:
   - *Legend*: `Churn`
   - *Values*: `[Total Customers]`
   - *Colors*: Retained = `#2A9D8F`, Churned = `#E63946`
   - *Title*: `Customer Retention Distribution`
2. **Visual 2 (Clustered Column Chart)**:
   - *X-axis*: `Contract`
   - *Y-axis*: `[Churn Rate %]`
   - *Data Labels*: Enabled (`Month-to-month: 42.7%`, `One year: 11.3%`, `Two year: 2.8%`)
   - *Title*: `Churn Rate % by Contract Type`
3. **Visual 3 (Clustered Bar Chart)**:
   - *Y-axis*: `TenureCohort`
   - *X-axis*: `[Churn Rate %]`
   - *Title*: `Attrition Risk Across Customer Lifecycle`
4. **Visual 4 (Horizontal Bar Chart)**:
   - *Y-axis*: `PaymentMethod`
   - *X-axis*: `[Churn Rate %]`
   - *Title*: `Churn Rate by Payment Channel`

---

## 5. Page 2: Retention Insights & Risk Targeting Layout

### Top Financial Impact Cards
1. **Active Monthly Revenue (MRR)**: `[Retained Monthly Revenue]` -> `$316.99K`
2. **Monthly Revenue Lost to Churn**: `[Lost Monthly Revenue (Churned MRR)]` -> `$139.13K`
3. **Immediate Revenue at Risk**: `[Immediate Revenue at Risk ($/mo)]` -> `$14.77K`
4. **High Risk Cohort Churn Rate**: `[High Risk Cohort Churn Rate %]` -> `71.2%`

### Main Diagnostic Visuals
1. **Visual 1 (Line / Area / Density Chart)**:
   - *X-axis*: `MonthlyChargeTier`
   - *Y-axis*: `[Churn Rate %]`
   - *Title*: `Pricing Sensitivity: Churn Rate by Monthly Spend Bracket`
2. **Visual 2 (Matrix Visual - Service Add-on Impact)**:
   - *Rows*: `TechSupport`
   - *Columns*: `OnlineSecurity`
   - *Values*: `[Churn Rate %]`
   - *Conditional Formatting*: Background color scale (Red for high churn > 40%, Green for low churn < 15%)
3. **Visual 3 (Table Visual - At-Risk Account Priority Queue)**:
   - *Columns*: `customerID`, `tenure`, `MonthlyCharges`, `Contract`, `InternetService`, `PaymentMethod`
   - *Filter pane*: Filter on `Contract = "Month-to-month"` AND `InternetService = "Fiber optic"` AND `Churn = "No"`
   - *Title*: `High Priority Retention Outreach List`
4. **Visual 4 (Text / Callout Card - Business Retention Recommendations)**:
   - Bulleted strategic takeaways:
     - 1. Onboarding Contract Incentive (Migrate month-to-month to 1-year plans).
     - 2. Auto-Pay Discount ($5/mo off for bank transfer / credit card).
     - 3. Complimentary 90-Day Tech Support & Security Bundle.

---

## 6. Publishing to Power BI Service

1. Save the report locally as `power_bi/telco_customer_churn_dashboard.pbix`.
2. Click **Home** -> **Publish**.
3. Select your workspace (e.g., `My workspace`).
4. Click **Select**. Once published, open the report link in your browser.
5. In Power BI Service, click **File** -> **Generate QR code** or **Embed report** -> **Publish to web (public)** to embed the interactive dashboard link into your GitHub README!
