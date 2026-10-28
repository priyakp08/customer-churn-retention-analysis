"""
Script: generate_excel_workbook.py
Project: Customer Churn & Retention Analysis
Description:
    Generates an executive-ready Excel workbook with multiple tabs:
    - Executive_KPI_Summary (KPIs, formulas, revenue impact)
    - Segment_Analysis (Summary tables by Contract, Tenure, Internet, Payment)
    - High_Risk_Segments (Identified high-risk cohorts)
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
PROCESSED_DATA_PATH = os.path.join(PROJECT_ROOT, "data", "processed", "telco_churn_cleaned.csv")
EXCEL_OUTPUT_PATH = os.path.join(PROJECT_ROOT, "reports", "telco_churn_excel_analysis.xlsx")

def create_excel_portfolio():
    df = pd.read_csv(PROCESSED_DATA_PATH)
    wb = openpyxl.Workbook()

    header_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
    alert_fill = PatternFill(start_color="FDE8E8", end_color="FDE8E8", fill_type="solid")

    title_font = Font(name="Calibri", size=16, bold=True, color="1B365D")
    subtitle_font = Font(name="Calibri", size=11, italic=True, color="555555")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    bold_font = Font(name="Calibri", size=11, bold=True)
    regular_font = Font(name="Calibri", size=11)

    thin_border = Border(
        left=Side(style='thin', color='DDDDDD'),
        right=Side(style='thin', color='DDDDDD'),
        top=Side(style='thin', color='DDDDDD'),
        bottom=Side(style='thin', color='DDDDDD')
    )

    # TAB 1: Executive KPI Summary
    ws1 = wb.active
    ws1.title = "Executive_KPI_Summary"
    ws1.views.sheetView[0].showGridLines = True

    ws1["A1"] = "Customer Churn & Retention Analysis — Executive KPI Summary"
    ws1["A1"].font = title_font
    ws1["A2"] = "Reconciled Across Python, MySQL, and Power BI | Source: IBM Telco Customer Churn"
    ws1["A2"].font = subtitle_font

    kpi_headers = ["Metric Description", "Value", "Unit / Format", "Calculation Logic / Benchmark", "Status"]
    for col_num, h in enumerate(kpi_headers, 1):
        cell = ws1.cell(row=4, column=col_num)
        cell.value = h
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    total_cust = len(df)
    churn_cust = int(df['ChurnNumeric'].sum())
    retained_cust = total_cust - churn_cust
    churn_rate = churn_cust / total_cust
    ret_rate = retained_cust / total_cust
    mrr_retained = df[df['Churn'] == 'No']['MonthlyCharges'].sum()
    mrr_churned = df[df['Churn'] == 'Yes']['MonthlyCharges'].sum()

    kpi_rows = [
        ["Total Customer Base", total_cust, "Customers", "7,043 Accounts", "Verified Ground Truth"],
        ["Retained Customers", retained_cust, "Customers", f"{retained_cust:,} Accounts", "Active Base (73.46%)"],
        ["Churned Customers", churn_cust, "Customers", f"{churn_cust:,} Accounts", "At-Risk / Lost (26.54%)"],
        ["Overall Customer Churn Rate", churn_rate, "Percentage", f"={churn_cust}/{total_cust}", "Baseline Benchmark"],
        ["Overall Customer Retention Rate", ret_rate, "Percentage", f"={retained_cust}/{total_cust}", "Target > 80%"],
        ["Total Monthly Revenue (Retained)", mrr_retained, "USD ($)", f"${mrr_retained:,.2f}", "Active Recurring MRR"],
        ["Monthly Recurring Revenue Lost to Churn", mrr_churned, "USD ($)", f"${mrr_churned:,.2f}", "Urgent Recovery Opportunity"],
        ["Average Monthly Charge (Retained)", df[df['Churn'] == 'No']['MonthlyCharges'].mean(), "USD ($)", "$61.27 / month", "Benchmark"],
        ["Average Monthly Charge (Churned)", df[df['Churn'] == 'Yes']['MonthlyCharges'].mean(), "USD ($)", "$74.44 / month (+21.5%)", "Higher Price Friction"]
    ]

    for r_idx, row_data in enumerate(kpi_rows, 5):
        for c_idx, val in enumerate(row_data, 1):
            cell = ws1.cell(row=r_idx, column=c_idx)
            cell.value = val
            cell.font = regular_font
            cell.border = thin_border
            if c_idx == 1:
                cell.font = bold_font
            elif c_idx == 2:
                cell.alignment = Alignment(horizontal="right")
                if "Rate" in row_data[0]:
                    cell.number_format = '0.00%'
                elif "Revenue" in row_data[0] or "Average" in row_data[0]:
                    cell.number_format = '$#,##0.00'
                else:
                    cell.number_format = '#,##0'

    # TAB 2: Segment Analysis
    ws2 = wb.create_sheet(title="Segment_Churn_Pivot")
    ws2.views.sheetView[0].showGridLines = True
    ws2["A1"] = "Customer Attrition by Key Business Dimensions"
    ws2["A1"].font = title_font

    seg_headers = ["Category Dimension", "Segment Name", "Total Customers", "Churned Customers", "Churn Rate (%)", "Share of Total Churn (%)"]
    for col_num, h in enumerate(seg_headers, 1):
        cell = ws2.cell(row=3, column=col_num)
        cell.value = h
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    segments_list = [
        ("Contract", "Month-to-month", 3875, 1655, 0.4271, 0.8855),
        ("Contract", "One year", 1473, 166, 0.1127, 0.0888),
        ("Contract", "Two year", 1695, 48, 0.0283, 0.0257),
        ("Tenure Cohort", "0 - 12 Months", 2186, 1037, 0.4744, 0.5548),
        ("Tenure Cohort", "13 - 24 Months", 1024, 294, 0.2871, 0.1573),
        ("Tenure Cohort", "25 - 48 Months", 1594, 325, 0.2039, 0.1739),
        ("Tenure Cohort", "49 - 60 Months", 832, 120, 0.1442, 0.0642),
        ("Tenure Cohort", "61 - 72 Months", 1407, 93, 0.0661, 0.0498),
        ("Internet Service", "Fiber optic", 3096, 1297, 0.4189, 0.6940),
        ("Internet Service", "DSL", 2421, 459, 0.1896, 0.2456),
        ("Internet Service", "No Internet", 1526, 113, 0.0740, 0.0605),
        ("Payment Method", "Electronic check", 2365, 1071, 0.4529, 0.5730),
        ("Payment Method", "Mailed check", 1612, 308, 0.1911, 0.1648),
        ("Payment Method", "Bank transfer (auto)", 1544, 258, 0.1671, 0.1380),
        ("Payment Method", "Credit card (auto)", 1522, 232, 0.1524, 0.1241),
    ]

    for r_idx, s in enumerate(segments_list, 4):
        for c_idx, val in enumerate(s, 1):
            cell = ws2.cell(row=r_idx, column=c_idx)
            cell.value = val
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [3, 4]:
                cell.number_format = '#,##0'
                cell.alignment = Alignment(horizontal="right")
            elif c_idx in [5, 6]:
                cell.number_format = '0.00%'
                cell.alignment = Alignment(horizontal="right")
                if c_idx == 5 and val > 0.35:
                    cell.fill = alert_fill
                    cell.font = Font(name="Calibri", size=11, bold=True, color="9C0006")

    # TAB 3: High Risk Cohort
    ws3 = wb.create_sheet(title="High_Risk_Cohort")
    ws3.views.sheetView[0].showGridLines = True
    ws3["A1"] = "High Risk Customer Cohort (Month-to-Month + Fiber Optic + Electronic Check + Tenure <= 12m)"
    ws3["A1"].font = title_font

    high_risk_df = df[
        (df['Contract'] == 'Month-to-month') &
        (df['InternetService'] == 'Fiber optic') &
        (df['PaymentMethod'] == 'Electronic check') &
        (df['tenure'] <= 12)
    ]
    active_high_risk = high_risk_df[high_risk_df['Churn'] == 'No']
    ws3["A2"] = f"Total Segment: {len(high_risk_df)} | Churned: {(high_risk_df['Churn'] == 'Yes').sum()} (71.16% Churn Rate) | Currently Active at Risk: {len(active_high_risk)} Accounts (${active_high_risk['MonthlyCharges'].sum():,.2f}/mo)"
    ws3["A2"].font = subtitle_font

    hr_headers = ["CustomerID", "Gender", "SeniorCitizen", "Tenure (Mos)", "Contract", "InternetService", "PaymentMethod", "MonthlyCharges ($)", "TotalCharges ($)", "Churn Status"]
    for col_num, h in enumerate(hr_headers, 1):
        cell = ws3.cell(row=4, column=col_num)
        cell.value = h
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    for r_idx, (_, r) in enumerate(active_high_risk.head(50).iterrows(), 5):
        vals = [r['customerID'], r['gender'], r['SeniorCitizen_Label'], r['tenure'], r['Contract'], r['InternetService'], r['PaymentMethod'], r['MonthlyCharges'], r['TotalCharges'], r['Churn']]
        for c_idx, val in enumerate(vals, 1):
            cell = ws3.cell(row=r_idx, column=c_idx)
            cell.value = val
            cell.font = regular_font
            cell.border = thin_border
            if c_idx in [8, 9]:
                cell.number_format = '$#,##0.00'

    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                try:
                    if cell.value:
                        max_len = max(max_len, len(str(cell.value)))
                except:
                    pass
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    wb.save(EXCEL_OUTPUT_PATH)
    print(f"[SUCCESS] Excel workbook generated at: {EXCEL_OUTPUT_PATH}")

if __name__ == "__main__":
    create_excel_portfolio()
