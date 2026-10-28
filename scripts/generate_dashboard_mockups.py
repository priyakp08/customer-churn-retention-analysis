"""
Script: generate_dashboard_mockups.py
Project: Customer Churn & Retention Analysis
Description:
    Renders pixel-perfect, executive-grade 16:9 visual mockups representing:
    - Page 1: Churn Overview
    - Page 2: Retention Insights & Risk Targeting
    Saves outputs directly to screenshots/ for inclusion in documentation and GitHub.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Corporate Color Palette
navy = "#1B365D"
crimson = "#E63946"
teal = "#2A9D8F"
bg_gray = "#F4F6F9"
card_white = "#FFFFFF"
border_gray = "#CBD5E1"
dark_text = "#0F172A"
sub_text = "#64748B"

def draw_top_kpis(ax, kpis):
    card_w = 0.222
    spacing = 0.017
    start_x = 0.03
    for i, (title, val, subtitle, color) in enumerate(kpis):
        x = start_x + i * (card_w + spacing)
        ax.add_patch(patches.FancyBboxPatch((x, 0.785), card_w, 0.105, boxstyle="round,pad=0.008", 
                                            facecolor=card_white, edgecolor=border_gray, linewidth=1.2))
        ax.add_patch(patches.Rectangle((x, 0.88), card_w, 0.01, facecolor=color))
        ax.text(x + 0.012, 0.852, title, fontsize=9.5, weight='bold', color=sub_text)
        ax.text(x + 0.012, 0.812, val, fontsize=20, weight='bold', color=color)
        ax.text(x + 0.012, 0.793, subtitle, fontsize=8.5, color=sub_text)

# ----------------------------------------------------------------------------
# PAGE 1: CHURN OVERVIEW
# ----------------------------------------------------------------------------
def generate_page_1():
    fig = plt.figure(figsize=(16, 9), facecolor=bg_gray, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Header
    ax.add_patch(patches.Rectangle((0, 0.91), 1, 0.09, facecolor=navy))
    ax.text(0.03, 0.962, "Customer Churn & Retention Analysis | Executive Dashboard", 
            fontsize=20, weight='bold', color='white', va='center')
    ax.text(0.03, 0.932, "Page 1: Churn Overview — High-Level Attrition KPIs, Contracts, Lifecycle & Payment Friction", 
            fontsize=11.5, color='#CBD5E1', va='center')

    # Top KPI Cards
    kpis = [
        ("TOTAL CUSTOMERS", "7,043", "Active & Churned Accounts", navy),
        ("RETAINED CUSTOMERS", "5,174", "73.5% Overall Retention", teal),
        ("CHURNED CUSTOMERS", "1,869", "26.5% Overall Churn", crimson),
        ("CHURN RATE", "26.54%", "Baseline Churn Benchmark", crimson)
    ]
    draw_top_kpis(ax, kpis)

    # Panel 1: Retention Donut
    ax1 = fig.add_axes([0.03, 0.44, 0.455, 0.30], facecolor=card_white)
    ax1.set_title("Customer Retention Distribution", fontsize=12, weight='bold', color=dark_text, pad=10)
    sizes = [5174, 1869]
    labels = ['Retained\n5,174 (73.5%)', 'Churned\n1,869 (26.5%)']
    ax1.pie(sizes, labels=labels, colors=[teal, crimson], autopct='%1.1f%%', startangle=90,
            wedgeprops=dict(width=0.40, edgecolor='white', linewidth=2),
            textprops={'fontsize': 10, 'weight': 'bold', 'color': dark_text})

    # Panel 2: Contract Type
    ax2 = fig.add_axes([0.515, 0.44, 0.455, 0.30], facecolor=card_white)
    contracts = ['Month-to-month', 'One year', 'Two year']
    c_rates = [42.71, 11.27, 2.83]
    bars = ax2.bar(contracts, c_rates, color=[crimson, '#3B82F6', teal], width=0.48, edgecolor=border_gray)
    ax2.axhline(26.54, color='red', linestyle='--', linewidth=1.2, label='Avg Churn (26.5%)')
    for b in bars:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3), 
                     textcoords="offset points", ha='center', fontsize=9.5, weight='bold')
    ax2.set_title("Churn Rate % by Contract Type (Month-to-month drives 88.6% of churn)", fontsize=12, weight='bold', color=dark_text, pad=10)
    ax2.set_ylabel("Churn Rate (%)", fontsize=9.5, color=sub_text)
    ax2.set_ylim(0, 52)
    ax2.legend(loc='upper right', fontsize=8.5)
    ax2.tick_params(axis='both', labelsize=9.5)

    # Panel 3: Tenure Cohort
    ax3 = fig.add_axes([0.03, 0.065, 0.455, 0.31], facecolor=card_white)
    tenure_groups = ['0-12 Mos', '13-24 Mos', '25-48 Mos', '49-60 Mos', '61-72 Mos']
    t_rates = [47.44, 28.71, 20.39, 14.42, 6.61]
    bars = ax3.bar(tenure_groups, t_rates, color='#2563EB', width=0.52, edgecolor=border_gray)
    ax3.axhline(26.54, color='red', linestyle='--', linewidth=1.2)
    for b in bars:
        h = b.get_height()
        ax3.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3), 
                     textcoords="offset points", ha='center', fontsize=9, weight='bold')
    ax3.set_title("Customer Lifecycle Attrition (Early 0-12 Mos Tenure Risk)", fontsize=12, weight='bold', color=dark_text, pad=10)
    ax3.set_ylabel("Churn Rate (%)", fontsize=9.5, color=sub_text)
    ax3.set_ylim(0, 58)
    ax3.tick_params(axis='both', labelsize=9)

    # Panel 4: Payment Method
    ax4 = fig.add_axes([0.515, 0.065, 0.455, 0.31], facecolor=card_white)
    pms = ['Electronic check', 'Mailed check', 'Bank transfer (auto)', 'Credit card (auto)']
    p_rates = [45.29, 19.11, 16.71, 15.24]
    y_pos = np.arange(len(pms))
    bars = ax4.barh(y_pos, p_rates, color=[crimson, '#93C5FD', '#60A5FA', '#2563EB'], height=0.52, edgecolor=border_gray)
    ax4.axvline(26.54, color='red', linestyle='--', linewidth=1.2)
    ax4.set_yticks(y_pos)
    ax4.set_yticklabels(pms, fontsize=9, weight='bold')
    ax4.invert_yaxis()
    for b in bars:
        w = b.get_width()
        ax4.annotate(f"{w:.1f}%", xy=(w, b.get_y() + b.get_height()/2), xytext=(4, 0), 
                     textcoords="offset points", va='center', fontsize=9, weight='bold')
    ax4.set_title("Churn Rate by Payment Channel (Manual Check vs Auto-Pay)", fontsize=12, weight='bold', color=dark_text, pad=10)
    ax4.set_xlabel("Churn Rate (%)", fontsize=9.5, color=sub_text)
    ax4.set_xlim(0, 55)
    ax4.tick_params(axis='both', labelsize=9)

    out1 = os.path.join(SCREENSHOTS_DIR, "power_bi_page1_churn_overview.png")
    plt.savefig(out1, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Saved Page 1 mockup: {out1}")

# ----------------------------------------------------------------------------
# PAGE 2: RETENTION INSIGHTS & RISK TARGETING
# ----------------------------------------------------------------------------
def generate_page_2():
    fig = plt.figure(figsize=(16, 9), facecolor=bg_gray, dpi=200)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')

    # Header
    ax.add_patch(patches.Rectangle((0, 0.91), 1, 0.09, facecolor=navy))
    ax.text(0.03, 0.962, "Customer Churn & Retention Analysis | Executive Dashboard", 
            fontsize=20, weight='bold', color='white', va='center')
    ax.text(0.03, 0.932, "Page 2: Retention Insights — Financial Sensitivity, Add-on Stickiness & Actionable Outreach", 
            fontsize=11.5, color='#CBD5E1', va='center')

    # Top KPI Cards
    kpis = [
        ("ACTIVE MONTHLY REVENUE", "$316.99K", "Active Recurring MRR", teal),
        ("LOST MRR (CHURNED)", "$139.13K", "$139.1K / Month Attrition", crimson),
        ("IMMEDIATE REVENUE AT RISK", "$14.77K", "182 High-Risk Active Accounts", '#D97706'),
        ("HIGH RISK CHURN RATE", "71.16%", "M2M + Fiber + E-Check + <12m", crimson)
    ]
    draw_top_kpis(ax, kpis)

    # Visual 1: Price Sensitivity (Monthly Charge Tiers)
    ax1 = fig.add_axes([0.03, 0.44, 0.455, 0.30], facecolor=card_white)
    tiers = ['Low (<$35)', 'Medium ($35-$70)', 'High ($70-$90)', 'Very High (>$90)']
    t_rates = [10.89, 23.94, 37.80, 32.78]
    bars = ax1.bar(tiers, t_rates, color=['#10B981', '#F59E0B', '#EF4444', '#DC2626'], width=0.52, edgecolor=border_gray)
    ax1.axhline(26.54, color='black', linestyle='--', linewidth=1.2, label='Avg Churn (26.5%)')
    for b in bars:
        h = b.get_height()
        ax1.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3), 
                     textcoords="offset points", ha='center', fontsize=9, weight='bold')
    ax1.set_title("Pricing Sensitivity: Churn Rate % by Monthly Spend Bracket", fontsize=12, weight='bold', color=dark_text, pad=10)
    ax1.set_ylabel("Churn Rate (%)", fontsize=9.5, color=sub_text)
    ax1.set_ylim(0, 48)
    ax1.legend(loc='upper left', fontsize=8.5)
    ax1.tick_params(axis='both', labelsize=8.5)

    # Visual 2: Support & Security Add-on Impact
    ax2 = fig.add_axes([0.515, 0.44, 0.455, 0.30], facecolor=card_white)
    combos = ['Neither Support\nnor Security', 'Tech Support\nOnly', 'Online Security\nOnly', 'Both Support\n& Security']
    c_rates = [48.96, 22.33, 21.30, 9.01]
    bars = ax2.bar(combos, c_rates, color=[crimson, '#F59E0B', '#EAB308', teal], width=0.52, edgecolor=border_gray)
    for b in bars:
        h = b.get_height()
        ax2.annotate(f"{h:.1f}%", xy=(b.get_x() + b.get_width()/2, h), xytext=(0, 3), 
                     textcoords="offset points", ha='center', fontsize=9.5, weight='bold')
    ax2.set_title("Service Add-on Stickiness: 5.4x Churn Reduction with Bundled Services", fontsize=12, weight='bold', color=dark_text, pad=10)
    ax2.set_ylabel("Churn Rate (%)", fontsize=9.5, color=sub_text)
    ax2.set_ylim(0, 58)
    ax2.tick_params(axis='both', labelsize=8.5)

    # Visual 3: High-Risk Cohort Callout Card
    ax.add_patch(patches.FancyBboxPatch((0.03, 0.065), 0.455, 0.31, boxstyle="round,pad=0.01", 
                                        facecolor=card_white, edgecolor=border_gray, linewidth=1.2))
    ax.text(0.045, 0.335, "High-Risk Segment Profile (Outreach Target Queue)", fontsize=12, weight='bold', color=dark_text)
    ax.text(0.045, 0.295, "- Target Criteria: Month-to-month + Fiber Optic + Electronic Check + Tenure <= 12 Mos", fontsize=9, color=dark_text)
    ax.text(0.045, 0.260, "- Historical Cohort Size: 631 Total Customers | 449 Churned (71.16% Churn Rate)", fontsize=9, weight='bold', color=crimson)
    ax.text(0.045, 0.225, "- Active High-Risk Customers: 182 Accounts Currently Active", fontsize=9, weight='bold', color=teal)
    ax.text(0.045, 0.190, "- Immediate Monthly Revenue at Risk: $14,768.95 / Month ($177.2K ARR)", fontsize=9, weight='bold', color=crimson)
    ax.text(0.045, 0.155, "- Priority Action: Assign dedicated onboarding success specialist within first 90 days.", fontsize=8.5, color=sub_text)
    ax.text(0.045, 0.120, "- Strategic Offer: 1-Year contract lock ($10/mo discount) + Free Tech Support add-on.", fontsize=8.5, color=sub_text)

    # Visual 4: Actionable Retention Playbook
    ax.add_patch(patches.FancyBboxPatch((0.515, 0.065), 0.455, 0.31, boxstyle="round,pad=0.01", 
                                        facecolor=card_white, edgecolor=border_gray, linewidth=1.2))
    ax.text(0.53, 0.335, "Executive Retention Playbook & Testable Interventions", fontsize=12, weight='bold', color=dark_text)
    strategies = [
        ("1. Early Onboarding Guardrail (Days 0-90):", "55.5% of churn happens in Year 1. Implement onboarding check-ins and satisfaction surveys."),
        ("2. Auto-Pay Discount Campaign ($5/mo):", "Incentivize electronic check users (45.3% churn) to switch to automated billing (15.2% churn)."),
        ("3. Security & Support Bundle Adoption:", "Promote Tech Support & Online Security to reduce churn from 49.0% down to 9.0%."),
        ("4. Contract Migration Incentive:", "Offer one-time bill credit ($50) to convert month-to-month users to 1-year agreements.")
    ]
    y_step = 0.28
    for title, desc in strategies:
        ax.text(0.53, y_step, title, fontsize=9, weight='bold', color=navy)
        ax.text(0.53, y_step - 0.024, desc, fontsize=8.5, color=sub_text)
        y_step -= 0.052

    out2 = os.path.join(SCREENSHOTS_DIR, "power_bi_page2_retention_insights.png")
    plt.savefig(out2, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Saved Page 2 mockup: {out2}")

if __name__ == "__main__":
    generate_page_1()
    generate_page_2()
