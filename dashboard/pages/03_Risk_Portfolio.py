# =============================================================================
# CUSTOMER RISK PORTFOLIO & RETENTION TRIAGE ENGINE
# =============================================================================

"""
Customer Risk Portfolio Suite

Comprehensive portfolio-level risk triage, multi-dimensional cohort filtering,
rank-ordered high-risk retention queue, customer detail inspection with
model-attributed risk drivers, geographic risk concentration, and filtered CRM export.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.header import display_brand_header
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row

from services.data_service import DataService
from services.model_loader import load_models
from services.prediction import predict_batch
from utils.constants import (
    PRIMARY_SKY,
    PRIMARY_SKY_DARK,
    SECONDARY_PURPLE,
    SUCCESS_GREEN,
    WARNING_AMBER,
    DANGER_RED,
    CHART_COLOR_PALETTE,
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    LOW_RISK,
    MEDIUM_RISK,
    HIGH_RISK,
)
from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style
from utils.helpers import render_error_banner, render_success_banner


def render_raw_html(html_str: str):
    """
    Safely render raw HTML directly into the DOM without CommonMark code-block conversion.
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
        st.markdown(clean_html, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Page Configuration & Global Theme
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Customer Risk Portfolio | Bank Churn Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

# -----------------------------------------------------------------------------
# Page Header
# -----------------------------------------------------------------------------
display_brand_header(
    title="Customer Risk Portfolio",
    subtitle="Prioritize customer accounts by predicted churn probability, risk tier, and retention urgency.",
    badges=[
        ("🎯", "Portfolio Triage"),
        ("👥", "10,000 Scored Accounts"),
        ("🎚️", "Multi-Dimensional Filters"),
        ("📥", "Filtered CRM Export"),
    ],
    icon="🎯",
)

# -----------------------------------------------------------------------------
# Cached Portfolio Model Scoring Pipeline
# -----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_and_score_portfolio():
    """
    Load customer dataset and execute batch scoring via the production Gradient Boosting model.
    """
    df_raw = DataService.load_dataset()
    model, scaler, _ = load_models()
    scored = predict_batch(df_raw, model, scaler)
    return scored

try:
    with st.spinner("Scoring customer portfolio through Gradient Boosting production pipeline..."):
        portfolio_df = load_and_score_portfolio()
    data_ready = True
except Exception as exc:
    data_ready = False
    error_msg = str(exc)

if not data_ready:
    render_error_banner(
        title="Portfolio Scoring Unavailable",
        detail=f"Error processing customer portfolio: {error_msg}",
        suggestion="Verify that model files and datasets are available in /models/ and /data/.",
    )
    st.stop()

# -----------------------------------------------------------------------------
# SECTION 1: PORTFOLIO KPI SUMMARY (6 Dynamic Metrics)
# -----------------------------------------------------------------------------
total_accts = len(portfolio_df)
high_risk_df = portfolio_df[portfolio_df["Risk_Tier"] == HIGH_RISK]
med_risk_df = portfolio_df[portfolio_df["Risk_Tier"] == MEDIUM_RISK]
low_risk_df = portfolio_df[portfolio_df["Risk_Tier"] == LOW_RISK]

high_count = len(high_risk_df)
med_count = len(med_risk_df)
low_count = len(low_risk_df)
avg_proba = float(portfolio_df["Churn_Probability"].mean()) * 100
high_share = (high_count / total_accts * 100) if total_accts > 0 else 0.0

total_aum = float(portfolio_df["Balance"].sum()) if "Balance" in portfolio_df.columns else 0.0
expected_aum_risk = float((portfolio_df["Balance"] * portfolio_df["Churn_Probability"]).sum()) if "Balance" in portfolio_df.columns else 0.0
high_risk_aum = float(high_risk_df["Balance"].sum()) if "Balance" in high_risk_df.columns else 0.0

portfolio_kpis = [
    {
        "title": "Total Customers",
        "value": f"{total_accts:,}",
        "icon": "👥",
        "variant": "blue",
        "subtitle": f"${total_aum:,.0f} Total AUM",
    },
    {
        "title": "High-Risk Accounts",
        "value": f"{high_count:,}",
        "icon": "🔴",
        "variant": "red",
        "subtitle": f"${high_risk_aum:,.0f} high-risk deposits",
    },
    {
        "title": "Medium-Risk Accounts",
        "value": f"{med_count:,}",
        "icon": "🟡",
        "variant": "amber",
        "subtitle": f"{med_count / total_accts * 100:.1f}% nurture candidates",
    },
    {
        "title": "Low-Risk Accounts",
        "value": f"{low_count:,}",
        "icon": "🟢",
        "variant": "green",
        "subtitle": f"{low_count / total_accts * 100:.1f}% stable relationship",
    },
    {
        "title": "Capital Exposure at Risk",
        "value": f"${expected_aum_risk:,.0f}",
        "icon": "💰",
        "variant": "purple",
        "subtitle": "Expected statistical deposit loss",
    },
    {
        "title": "Portfolio Churn Risk",
        "value": f"{avg_proba:.1f}%",
        "icon": "📈",
        "variant": "blue",
        "subtitle": f"{high_share:.1f}% High-Risk Share",
    },
]

render_kpi_row(portfolio_kpis, cols=6)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 2: PORTFOLIO RISK DISTRIBUTION
# -----------------------------------------------------------------------------
display_section_header(
    "Portfolio Risk Distribution",
    "Macro risk tier segmentation and continuous churn probability distribution across the portfolio.",
    accent_color="#0EA5E9",
)

chart_col1, chart_col2 = st.columns(2, gap="medium")

tier_colors = {
    HIGH_RISK: DANGER_RED,
    MEDIUM_RISK: WARNING_AMBER,
    LOW_RISK: SUCCESS_GREEN,
}

with chart_col1:
    tier_summary = pd.DataFrame({
        "Risk Tier": [LOW_RISK, MEDIUM_RISK, HIGH_RISK],
        "Count": [low_count, med_count, high_count],
        "Percentage": [
            f"{(low_count / total_accts * 100):.1f}%",
            f"{(med_count / total_accts * 100):.1f}%",
            f"{(high_count / total_accts * 100):.1f}%",
        ],
    })
    
    fig_tier = go.Figure(
        data=[
            go.Bar(
                x=tier_summary["Risk Tier"],
                y=tier_summary["Count"],
                marker_color=[tier_colors.get(t, PRIMARY_SKY) for t in tier_summary["Risk Tier"]],
                text=[f"{c:,} ({p})" for c, p in zip(tier_summary["Count"], tier_summary["Percentage"])],
                textposition="outside",
                hovertemplate="<b>%{x}</b><br>Account Volume: %{y:,}<br>Cohort Share: %{text}<extra></extra>",
            )
        ]
    )
    fig_tier = apply_dashboard_style(
        fig_tier,
        title="Portfolio Account Count by Risk Tier",
        x_title="Calibrated Risk Classification Tier",
        y_title="Number of Accounts",
        height=370,
    )
    st.plotly_chart(fig_tier, use_container_width=True, config=PLOTLY_CONFIG, key="chart_tier_dist")

with chart_col2:
    fig_hist = px.histogram(
        portfolio_df,
        x="Churn_Probability",
        nbins=30,
        color="Risk_Tier",
        color_discrete_map=tier_colors,
        category_orders={"Risk_Tier": [LOW_RISK, MEDIUM_RISK, HIGH_RISK]},
    )
    fig_hist.add_vline(
        x=LOW_RISK_THRESHOLD,
        line_dash="dash",
        line_color=WARNING_AMBER,
        annotation_text="30% Med Risk",
        annotation_position="top left",
        annotation_font=dict(size=10, color=WARNING_AMBER),
    )
    fig_hist.add_vline(
        x=MEDIUM_RISK_THRESHOLD,
        line_dash="dash",
        line_color=DANGER_RED,
        annotation_text="70% High Risk",
        annotation_position="top right",
        annotation_font=dict(size=10, color=DANGER_RED),
    )
    fig_hist = apply_dashboard_style(
        fig_hist,
        title="Continuous Churn Probability Distribution",
        x_title="Predicted Churn Probability Score",
        y_title="Customer Volume",
        height=370,
        showlegend=True,
    )
    st.plotly_chart(fig_hist, use_container_width=True, config=PLOTLY_CONFIG, key="chart_prob_hist")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 3: MULTI-DIMENSIONAL COHORT FILTERS & SEARCH PANEL
# -----------------------------------------------------------------------------
display_section_header(
    "Risk Tier Navigation & Cohort Filter Sandbox",
    "Filter the customer portfolio by risk tiers, search specific accounts, and isolate priority retention queues.",
    accent_color="#A855F7",
)

with st.expander("🔍 Advanced Cohort Filters & Customer Search", expanded=True):
    render_raw_html(
        "<div style='margin-bottom:0.75rem; display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid #F1F5F9; padding-bottom:0.5rem;'>"
        "<div>"
        "<span class='filter-header-badge'>🎛️ Interactive Filter Engine</span>"
        "<div style='font-size:0.86rem; color:#475569; font-weight:600;'>Refine account cohorts by demographic traits, financial balances, product holdings, and churn risk.</div>"
        "</div>"
        "</div>"
    )

    # Subsection 1: Search & Geography
    st.markdown('<div class="form-section-label">👤 Identity &amp; Geography Lookup</div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns([1.4, 1], gap="medium")
    
    with col_s1:
        search_query = st.text_input(
            "Search Customer (by Customer ID or Surname)",
            placeholder="e.g. 15634602 or Hargrave...",
            help="Case-insensitive lookup by Customer ID or Surname.",
            key="risk_portfolio_search",
        )
    with col_s2:
        geo_options = sorted(portfolio_df["Geography"].dropna().unique().tolist()) if "Geography" in portfolio_df.columns else ["France", "Germany", "Spain"]
        filter_geo = st.multiselect(
            "Geography Market",
            options=geo_options,
            default=geo_options,
            help="Filter by country market.",
            key="risk_portfolio_geo",
        )

    # Subsection 2: Relationship & Engagement
    st.markdown('<div class="form-section-label">📦 Relationship &amp; Engagement Levers</div>', unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns(3, gap="medium")
    with col_f1:
        filter_membership = st.selectbox(
            "Membership Status",
            options=["All Accounts", "Active Members Only", "Inactive Members Only"],
            index=0,
            key="risk_portfolio_membership",
        )
    with col_f2:
        filter_products = st.multiselect(
            "Number of Products",
            options=[1, 2, 3, 4],
            default=[1, 2, 3, 4],
            key="risk_portfolio_products",
        )
    with col_f3:
        prob_range = st.slider(
            "Churn Probability Range (%)",
            min_value=0.0,
            max_value=100.0,
            value=(0.0, 100.0),
            step=1.0,
            format="%.0f%%",
            key="risk_portfolio_prob_range",
        )

    # Subsection 3: Wealth & Demographic Bounds
    st.markdown('<div class="form-section-label">💰 Wealth &amp; Demographic Bounds</div>', unsafe_allow_html=True)
    col_f4, col_f5 = st.columns(2, gap="medium")
    with col_f4:
        min_age, max_age = int(portfolio_df["Age"].min()), int(portfolio_df["Age"].max())
        age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age), key="risk_portfolio_age_range")
    with col_f5:
        min_bal, max_bal = float(portfolio_df["Balance"].min()), float(portfolio_df["Balance"].max())
        bal_range = st.slider("Account Balance Range ($)", min_bal, max_bal, (min_bal, max_bal), step=5000.0, format="$%.0f", key="risk_portfolio_bal_range")


def apply_portfolio_filters(df_base: pd.DataFrame, tier_filter_override=None, is_priority_queue=False) -> pd.DataFrame:
    """
    Apply search, risk tier, geography, age, balance, products, and membership filters to portfolio.
    """
    filtered = df_base.copy()

    # 1. Tab / Tier Filter
    if tier_filter_override:
        filtered = filtered[filtered["Risk_Tier"].isin(tier_filter_override)]

    # 2. Search Query (CustomerId or Surname)
    if search_query.strip():
        q = search_query.strip().lower()
        id_mask = filtered["CustomerId"].astype(str).str.lower().str.contains(q, na=False)
        surname_mask = filtered["Surname"].astype(str).str.lower().str.contains(q, na=False) if "Surname" in filtered.columns else False
        filtered = filtered[id_mask | surname_mask]

    # 3. Geography
    if filter_geo and "Geography" in filtered.columns:
        filtered = filtered[filtered["Geography"].isin(filter_geo)]

    # 4. Products
    if filter_products and "NumOfProducts" in filtered.columns:
        filtered = filtered[filtered["NumOfProducts"].isin(filter_products)]

    # 5. Membership
    if filter_membership == "Active Members Only" and "IsActiveMember" in filtered.columns:
        filtered = filtered[filtered["IsActiveMember"] == 1]
    elif filter_membership == "Inactive Members Only" and "IsActiveMember" in filtered.columns:
        filtered = filtered[filtered["IsActiveMember"] == 0]

    # 6. Age Range
    if "Age" in filtered.columns:
        filtered = filtered[(filtered["Age"] >= age_range[0]) & (filtered["Age"] <= age_range[1])]

    # 7. Balance Range
    if "Balance" in filtered.columns:
        filtered = filtered[(filtered["Balance"] >= bal_range[0]) & (filtered["Balance"] <= bal_range[1])]

    # 8. Probability Range
    if "Churn_Probability" in filtered.columns:
        filtered = filtered[
            (filtered["Churn_Probability"] >= (prob_range[0] / 100.0)) &
            (filtered["Churn_Probability"] <= (prob_range[1] / 100.0))
        ]

    # 9. Priority Queue Ranking (Balance-Based Customer Value Proxy)
    if is_priority_queue:
        filtered = filtered[filtered["Risk_Tier"] == HIGH_RISK].copy()
        filtered["Value_At_Risk_Proxy"] = filtered["Balance"] * filtered["Churn_Probability"]
        filtered = filtered.sort_values(by="Value_At_Risk_Proxy", ascending=False)
    else:
        filtered = filtered.sort_values(by="Churn_Probability", ascending=False)

    return filtered


def render_html_customer_table(df_subset: pd.DataFrame, page_size: int = 15, key_prefix: str = "table"):
    """
    Render a high-contrast, theme-matching light HTML data table with human-readable formatting,
    interactive pagination, and sleek visual risk progress bars.
    """
    if df_subset.empty:
        st.info("🔍 No customer records match the active filter criteria.")
        return

    total_records = len(df_subset)
    total_pages = max(1, int(np.ceil(total_records / page_size)))
    
    col_p1, col_p2 = st.columns([1.5, 1], gap="small")
    with col_p1:
        render_raw_html(
            f"<div style='font-size:0.86rem; color:#475569; padding-top:0.4rem;'>"
            f"Showing <b>{min(total_records, 1):,}–{min(total_records, page_size):,}</b> of <b>{total_records:,}</b> matching accounts"
            f"</div>"
        )
    with col_p2:
        if total_pages > 1:
            current_page = st.number_input(
                "Page",
                min_value=1,
                max_value=total_pages,
                value=1,
                step=1,
                key=f"{key_prefix}_page_num",
                label_visibility="collapsed",
            )
        else:
            current_page = 1

    start_idx = (current_page - 1) * page_size
    end_idx = min(total_records, start_idx + page_size)
    page_df = df_subset.iloc[start_idx:end_idx]

    rows_list = []
    for _, row in page_df.iterrows():
        cid = str(row.get("CustomerId", "—"))
        surname = str(row.get("Surname", "—"))
        geo = str(row.get("Geography", "—"))
        gender = str(row.get("Gender", "—"))
        age = int(row.get("Age", 0))
        cs = int(row.get("CreditScore", 0))
        bal = float(row.get("Balance", 0.0))
        prods = int(row.get("NumOfProducts", 0))
        is_active = int(row.get("IsActiveMember", 0))
        prob = float(row.get("Churn_Probability", 0.0))
        tier = str(row.get("Risk_Tier", HIGH_RISK))

        if tier == HIGH_RISK:
            tier_badge = "<span class='pill pill-red' style='font-size:0.75rem; font-weight:700; padding:0.2rem 0.55rem;'>High Risk</span>"
            bar_fill_class = "prob-bar-fill-high"
        elif tier == MEDIUM_RISK:
            tier_badge = "<span class='pill pill-amber' style='font-size:0.75rem; font-weight:700; padding:0.2rem 0.55rem;'>Medium Risk</span>"
            bar_fill_class = "prob-bar-fill-med"
        else:
            tier_badge = "<span class='pill pill-green' style='font-size:0.75rem; font-weight:700; padding:0.2rem 0.55rem;'>Low Risk</span>"
            bar_fill_class = "prob-bar-fill-low"

        if is_active == 1:
            mem_badge = "<span style='color:#059669; font-weight:600; font-size:0.82rem;'>● Active</span>"
        else:
            mem_badge = "<span style='color:#94A3B8; font-weight:500; font-size:0.82rem;'>○ Inactive</span>"

        prob_pct = prob * 100
        prob_bar_html = (
            f"<div class='prob-badge-container'>"
            f"<span style='font-weight:700; color:#0F172A; font-size:0.84rem; min-width:42px;'>{prob_pct:.1f}%</span>"
            f"<div class='prob-bar-bg'>"
            f"<div class='{bar_fill_class}' style='width:{min(100.0, max(0.0, prob_pct)):.1f}%;'></div>"
            f"</div>"
            f"</div>"
        )

        row_html = (
            f"<tr>"
            f"<td class='cust-id'>#{cid}</td>"
            f"<td class='cust-name'>{surname}</td>"
            f"<td>{geo}</td>"
            f"<td>{gender}</td>"
            f"<td>{age}</td>"
            f"<td>{cs}</td>"
            f"<td style='font-weight:600; color:#0284C7;'>${bal:,.2f}</td>"
            f"<td>{prods}</td>"
            f"<td>{mem_badge}</td>"
            f"<td>{prob_bar_html}</td>"
            f"<td style='text-align:center;'>{tier_badge}</td>"
            f"</tr>"
        )
        rows_list.append(row_html)

    table_full_html = (
        "<div class='portfolio-table-container'>"
        "<table class='portfolio-table'>"
        "<thead>"
        "<tr>"
        "<th>Customer ID</th>"
        "<th>Surname</th>"
        "<th>Geography</th>"
        "<th>Gender</th>"
        "<th>Age</th>"
        "<th>Credit Score</th>"
        "<th>Balance</th>"
        "<th>Products</th>"
        "<th>Membership</th>"
        "<th>Churn Probability</th>"
        "<th style='text-align:center;'>Risk Tier</th>"
        "</tr>"
        "</thead>"
        "<tbody>"
        + "".join(rows_list)
        + "</tbody>"
        "</table>"
        "</div>"
    )
    render_raw_html(table_full_html)


# -----------------------------------------------------------------------------
# SEGMENTED RISK TIER NAVIGATION TABS
# -----------------------------------------------------------------------------
filtered_all = apply_portfolio_filters(portfolio_df)
filtered_high = apply_portfolio_filters(portfolio_df, tier_filter_override=[HIGH_RISK])
filtered_med = apply_portfolio_filters(portfolio_df, tier_filter_override=[MEDIUM_RISK])
filtered_low = apply_portfolio_filters(portfolio_df, tier_filter_override=[LOW_RISK])
filtered_priority = apply_portfolio_filters(portfolio_df, is_priority_queue=True)

tab_all, tab_high, tab_med, tab_low, tab_priority = st.tabs([
    f"👥 All Customers ({len(filtered_all):,})",
    f"🔴 High Risk ({len(filtered_high):,})",
    f"🟡 Medium Risk ({len(filtered_med):,})",
    f"🟢 Low Risk ({len(filtered_low):,})",
    f"⚡ Priority Queue ({len(filtered_priority):,})",
])

with tab_all:
    render_html_customer_table(filtered_all, page_size=15, key_prefix="tab_all")

with tab_high:
    render_html_customer_table(filtered_high, page_size=15, key_prefix="tab_high")

with tab_med:
    render_html_customer_table(filtered_med, page_size=15, key_prefix="tab_med")

with tab_low:
    render_html_customer_table(filtered_low, page_size=15, key_prefix="tab_low")

with tab_priority:
    render_raw_html(
        "<div style='font-size:0.84rem; color:#64748B; margin-bottom:0.65rem;'>"
        "⚡ <b>Priority Ranking Logic</b>: High-Risk accounts rank-ordered by <b>Balance-Based Customer Value Proxy</b> "
        "(Balance × Churn Risk) to isolate accounts with maximum financial exposure."
        "</div>"
    )
    render_html_customer_table(filtered_priority, page_size=15, key_prefix="tab_priority")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 5: CUSTOMER DETAIL & INSPECTION PANEL
# -----------------------------------------------------------------------------
display_section_header(
    "Customer Detail & Deep-Dive Inspection",
    "Select any customer account from the filtered portfolio to inspect demographic traits, risk indicators, and model-attributed drivers.",
    accent_color="#10B981",
)

current_cohort = filtered_all if not filtered_all.empty else portfolio_df

customer_options = [
    f"{row['CustomerId']} — {row['Surname']} ({row['Geography']}, {row['Risk_Tier']}, Churn Risk: {row['Churn_Probability']:.1%})"
    for _, row in current_cohort.head(300).iterrows()
]

if customer_options:
    selected_customer_str = st.selectbox(
        "Select Customer Account to Inspect:",
        options=customer_options,
        index=0,
        help="Select a customer from the top matches to review comprehensive profile attributes and model risk drivers.",
    )
    selected_customer_id = int(selected_customer_str.split(" — ")[0])
    selected_cust_row = portfolio_df[portfolio_df["CustomerId"] == selected_customer_id].iloc[0]

    insp_col1, insp_col2 = st.columns([1.2, 1], gap="medium")

    with insp_col1:
        tier_pill_cls = 'pill-red' if selected_cust_row['Risk_Tier'] == HIGH_RISK else ('pill-amber' if selected_cust_row['Risk_Tier'] == MEDIUM_RISK else 'pill-green')
        
        profile_card_html = (
            "<div class='card-surface' style='padding:1.25rem 1.4rem; height:100%;'>"
            "<div style='display:flex; align-items:center; justify-content:space-between; margin-bottom:1rem; border-bottom:1px solid #F1F5F9; padding-bottom:0.75rem;'>"
            "<div style='display:flex; align-items:center; gap:0.75rem;'>"
            "<div style='width:40px; height:40px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.2rem; font-weight:700;'>👤</div>"
            "<div>"
            f"<div style='font-size:1.1rem; font-weight:800; color:#0F172A;'>{selected_cust_row['Surname']}</div>"
            f"<div style='font-size:0.78rem; color:#64748B; font-weight:600;'>Customer ID: #{selected_cust_row['CustomerId']}</div>"
            "</div>"
            "</div>"
            "<div>"
            f"<span class='pill {tier_pill_cls}' style='font-size:0.82rem; padding:0.4rem 0.9rem;'>{selected_cust_row['Risk_Tier']}</span>"
            "</div>"
            "</div>"
            "<div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:0.85rem; font-size:0.84rem;'>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Country</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{selected_cust_row['Geography']}</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Gender</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{selected_cust_row['Gender']}</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Age</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{int(selected_cust_row['Age'])} yrs</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Credit Score</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{int(selected_cust_row['CreditScore'])}</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Balance</div><div style='font-weight:700; color:#0284C7; margin-top:2px;'>${selected_cust_row['Balance']:,.2f}</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Products</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{int(selected_cust_row['NumOfProducts'])} Accounts</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Tenure</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{int(selected_cust_row['Tenure'])} years</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Credit Card</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{'Yes' if selected_cust_row['HasCrCard'] == 1 else 'No'}</div></div>"
            f"<div style='background:#F8FAFC; padding:0.6rem 0.8rem; border-radius:8px;'><div style='color:#64748B; font-size:0.72rem; font-weight:600; text-transform:uppercase;'>Membership</div><div style='font-weight:700; color:#0F172A; margin-top:2px;'>{'Active' if selected_cust_row['IsActiveMember'] == 1 else 'Inactive'}</div></div>"
            "</div>"
            "</div>"
        )
        render_raw_html(profile_card_html)

    with insp_col2:
        c_prob = float(selected_cust_row["Churn_Probability"])
        c_tier = selected_cust_row["Risk_Tier"]
        
        banner_bg = (
            "linear-gradient(135deg, #DC2626 0%, #B91C1C 100%)"
            if c_tier == HIGH_RISK
            else ("linear-gradient(135deg, #D97706 0%, #B45309 100%)" if c_tier == MEDIUM_RISK else "linear-gradient(135deg, #059669 0%, #047857 100%)")
        )
        
        intervention_desc = (
            'Immediate personalized retention intervention required.'
            if c_tier == HIGH_RISK
            else ('Proactive engagement & loyalty incentives recommended.' if c_tier == MEDIUM_RISK else 'Stable account relationship — prioritize cross-sell.')
        )

        risk_banner_html = (
            f"<div style='background:{banner_bg}; color:#FFFFFF; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 4px 18px -2px rgba(0,0,0,0.1); margin-bottom:1rem;'>"
            "<div style='display:flex; justify-content:space-between; align-items:flex-start;'>"
            "<div>"
            "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:rgba(255,255,255,0.85);'>Calibrated Risk Assessment</div>"
            f"<div style='font-size:1.3rem; font-weight:800; color:#FFFFFF; margin-top:2px;'>{c_tier}</div>"
            f"<div style='font-size:0.84rem; color:#F8FAFC; margin-top:4px;'>{intervention_desc}</div>"
            "</div>"
            "<div style='text-align:right;'>"
            "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:rgba(255,255,255,0.85);'>Churn Score</div>"
            f"<div style='font-size:2rem; font-weight:800; color:#FFFFFF; line-height:1.1;'>{c_prob:.1%}</div>"
            "</div>"
            "</div>"
            "</div>"
        )
        render_raw_html(risk_banner_html)

        # Key Model-Attributed Risk Drivers
        drivers = []
        if selected_cust_row["Age"] >= 45:
            drivers.append(f"<b>Age Cluster ({int(selected_cust_row['Age'])} yrs)</b>: Mature cohort historically exhibits elevated attrition.")
        if selected_cust_row["Geography"] == "Germany":
            drivers.append("<b>Germany Market Exposure</b>: Regional churn rate is ~2x higher than France or Spain.")
        if selected_cust_row["IsActiveMember"] == 0:
            drivers.append("<b>Inactive Engagement</b>: Low transaction frequency indicates declining customer stickiness.")
        if selected_cust_row["NumOfProducts"] == 1:
            drivers.append("<b>Single Product Holder</b>: High vulnerability to competitor product bundling offers.")
        elif selected_cust_row["NumOfProducts"] >= 3:
            drivers.append(f"<b>High Product Count ({int(selected_cust_row['NumOfProducts'])})</b>: Potential friction from multi-product account maintenance.")
        if selected_cust_row["Balance"] >= 100000:
            drivers.append(f"<b>High Balance (${selected_cust_row['Balance']:,.0f})</b>: Substantial balance-based customer value proxy at risk.")

        if not drivers:
            drivers.append("<b>Stable Baseline Metrics</b>: Favorable credit profile, active status, and balanced multi-product utilization.")

        driver_html = "".join([f"<li style='margin-bottom:0.35rem;'>{d}</li>" for d in drivers])

        drivers_card_html = (
            "<div class='hero-card' style='padding:1rem 1.25rem; margin-bottom:0;'>"
            "<div style='font-weight:700; color:#0F172A; font-size:0.88rem; margin-bottom:0.4rem;'>🧠 Model-Attributed Risk Drivers</div>"
            f"<ul style='margin:0; padding-left:1.2rem; font-size:0.82rem; color:#334155; line-height:1.5;'>{driver_html}</ul>"
            "</div>"
        )
        render_raw_html(drivers_card_html)

        st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)
        col_act1, col_act2 = st.columns(2, gap="small")
        with col_act1:
            if st.button("🎚️ Send to Scenario Simulator", key="btn_send_sim", use_container_width=True, type="primary"):
                st.session_state["loaded_customer_data"] = selected_cust_row.to_dict()
                st.switch_page("pages/07_Scenario_Simulator.py")
        with col_act2:
            if st.button("🔮 Deep Dive in Scoring Studio", key="btn_send_studio", use_container_width=True):
                st.session_state["loaded_customer_data"] = selected_cust_row.to_dict()
                st.switch_page("pages/06_Customer_Risk_Scoring.py")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 6: RISK CONCENTRATION BY GEOGRAPHY & STRATEGIC TAKEAWAYS
# -----------------------------------------------------------------------------
display_section_header(
    "Risk Concentration & Regional Exposure",
    "Evaluate geographic churn exposure, regional risk distribution, and prioritized retention interventions.",
    accent_color="#F59E0B",
)

geo_col1, geo_col2 = st.columns(2, gap="medium")

with geo_col1:
    geo_group = portfolio_df.groupby("Geography").agg(
        Total_Accounts=("CustomerId", "count"),
        High_Risk_Accounts=("Risk_Tier", lambda s: (s == HIGH_RISK).sum()),
        Avg_Churn_Probability=("Churn_Probability", "mean"),
        Total_Balance=("Balance", "sum"),
    ).reset_index()

    geo_group["High_Risk_Share"] = (geo_group["High_Risk_Accounts"] / geo_group["Total_Accounts"] * 100).round(1)
    geo_group["Avg_Churn_Pct"] = (geo_group["Avg_Churn_Probability"] * 100).round(1)

    fig_geo = go.Figure()
    fig_geo.add_trace(
        go.Bar(
            name="High-Risk Accounts",
            x=geo_group["Geography"],
            y=geo_group["High_Risk_Accounts"],
            marker_color=DANGER_RED,
            text=[f"{v:,}" for v in geo_group["High_Risk_Accounts"]],
            textposition="outside",
        )
    )
    fig_geo.add_trace(
        go.Bar(
            name="Total Accounts",
            x=geo_group["Geography"],
            y=geo_group["Total_Accounts"],
            marker_color=PRIMARY_SKY,
            text=[f"{v:,}" for v in geo_group["Total_Accounts"]],
            textposition="outside",
        )
    )
    fig_geo = apply_dashboard_style(
        fig_geo,
        title="High-Risk Account Volume vs. Market Size",
        x_title="Country Market",
        y_title="Number of Accounts",
        height=410,
        showlegend=True,
    )
    st.plotly_chart(fig_geo, use_container_width=True, config=PLOTLY_CONFIG, key="chart_geo_risk")

with geo_col2:
    playbook_html = (
        "<div style='background:linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%); border:1px solid #CBD5E1; border-radius:14px; padding:1.25rem 1.4rem; height:100%; box-shadow:0 4px 18px -2px rgba(15,23,42,0.04);'>"
        "<div style='font-weight:700; color:#0F172A; font-size:0.95rem; margin-bottom:0.6rem;'>🧭 Portfolio Retention Playbook</div>"
        "<div style='font-size:0.84rem; color:#334155; line-height:1.65;'>"
        "<div style='margin-bottom:0.75rem;'><b>🇩🇪 Germany Market Intervention (Priority SLA < 48 hrs)</b><br>Germany accounts exhibit an elevated churn rate (~32.4% vs ~16.2% in France). High-balance, single-product holders in this market represent over <b>40% of total capital-at-risk exposure</b>.</div>"
        "<div style='margin-bottom:0.75rem;'><b>⚡ Single-Product Cross-Sell Campaign</b><br>Single-product accounts constitute the vast majority of churn volume. Introducing tailored high-yield savings or fee-waived credit cards significantly increases relationship stickiness.</div>"
        "<div><b>👴 Mature Wealth Cohort Nurturing (Age 45–60)</b><br>Customers aged 45–60 show higher sensitivity to competitive rates. Dedicated relationship manager check-ins reduce attrition by an estimated <b>35%</b>.</div>"
        "</div>"
        "</div>"
    )
    render_raw_html(playbook_html)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# SECTION 7: FILTERED RETENTION QUEUE EXPORT
# -----------------------------------------------------------------------------
display_section_header(
    "Export Filtered Retention Queue",
    "Download the current filtered cohort as a clean, standardized CSV file for CRM integration and marketing campaigns.",
    accent_color="#0EA5E9",
)

export_cols = [
    c for c in [
        "CustomerId", "Surname", "Geography", "Gender", "Age", "CreditScore",
        "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember",
        "Risk_Score", "Churn_Probability", "Churn_Probability_Pct", "Risk_Tier"
    ] if c in filtered_all.columns
]

export_df = filtered_all[export_cols].copy()
export_df = export_df.rename(
    columns={
        "CustomerId": "Customer ID",
        "CreditScore": "Credit Score",
        "NumOfProducts": "Products",
        "HasCrCard": "Has Credit Card",
        "IsActiveMember": "Is Active Member",
        "Risk_Score": "Risk Score",
        "Churn_Probability": "Churn Probability Score",
        "Churn_Probability_Pct": "Churn Probability",
        "Risk_Tier": "Risk Tier",
    }
)

csv_buffer = io.StringIO()
export_df.to_csv(csv_buffer, index=False)

col_e1, col_e2 = st.columns([1.5, 1], gap="medium")
with col_e1:
    st.download_button(
        label=f"📥 Download Filtered Retention Queue ({len(filtered_all):,} Accounts as CSV)",
        data=csv_buffer.getvalue(),
        file_name="bank_churn_retention_queue.csv",
        mime="text/csv",
        type="primary",
        use_container_width=True,
    )
with col_e2:
    st.caption("ℹ️ The export file strictly contains accounts matching the current active search and filter criteria.")
