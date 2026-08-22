# =============================================================================
# SCENARIO SIMULATOR SUITE - ENTERPRISE GUIDED 3-STEP SANDBOX
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row

from services.model_loader import load_models
from services.prediction import predict_customer
from services.preprocessing import PreprocessingError
try:
    from services.prediction import PredictionError
except Exception:
    PredictionError = Exception

from utils.constants import (
    PRIMARY_SKY,
    PRIMARY_SKY_DARK,
    SECONDARY_PURPLE,
    SUCCESS_GREEN,
    WARNING_AMBER,
    DANGER_RED,
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    LOW_RISK,
    MEDIUM_RISK,
    HIGH_RISK,
    CHURN,
    NO_CHURN,
)
from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style
from utils.helpers import (
    init_session_state_defaults,
    safe_execute,
    compute_safe_delta,
    render_error_banner,
    render_toast,
)
from utils.validation import validate_customer_params, sanitize_probability
from utils.formatters import format_currency


def render_raw_html(html_str: str):
    """
    Safely render raw HTML directly into the DOM without CommonMark code-block conversion.
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
        st.markdown(clean_html, unsafe_allow_html=True)


st.set_page_config(
    page_title="Scenario Simulator | Bank Churn Intelligence",
    page_icon="🎚️",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
init_session_state_defaults()
display_sidebar()

# -----------------------------------------------------------------------------
# Compact Hero Header & Status Badges
# -----------------------------------------------------------------------------
compact_header_html = (
    "<div style='background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; border-radius:14px; padding:0.9rem 1.25rem; margin-bottom:0.75rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.06);'>"
    "<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>"
    "<div style='display:flex; align-items:center; gap:0.75rem;'>"
    "<div style='width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700;'>🎚️</div>"
    "<div>"
    "<h1 style='margin:0; font-size:1.25rem; font-weight:800; color:#0F172A; line-height:1.2;'>Retention Scenario Simulator</h1>"
    "<div style='font-size:0.8rem; color:#64748B; margin-top:2px;'>Interactive retention sandbox — adjust engagement, product holdings, and balances to observe live probability deltas.</div>"
    "</div>"
    "</div>"
    "<div style='display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;'>"
    "<span class='pill pill-purple' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🎚️ Scenario Tuning</span>"
    "<span class='pill pill-blue' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>📊 Live Delta Analysis</span>"
    "<span class='pill pill-green' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🧪 A/B Retention Testing</span>"
    "<span class='pill pill-amber' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>💡 Actionable Guidance</span>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(compact_header_html)

# -----------------------------------------------------------------------------
# Compact 4-Metric Horizontal Stat Ribbon
# -----------------------------------------------------------------------------
stat_ribbon_html = (
    "<div class='stat-ribbon-container' style='grid-template-columns: repeat(4, 1fr);'>"
    "<div class='stat-ribbon-card' style='display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.15rem;'>🧪</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Scenarios Supported</div>"
    "<div style='font-size:0.95rem; font-weight:800; color:#0F172A;'>Unlimited</div>"
    "</div>"
    "</div>"
    "<div class='stat-ribbon-card' style='display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.15rem;'>🎛️</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Tunable Levers</div>"
    "<div style='font-size:0.95rem; font-weight:800; color:#0284C7;'>11 Parameters</div>"
    "</div>"
    "</div>"
    "<div class='stat-ribbon-card' style='display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.15rem;'>🏆</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Champion Model</div>"
    "<div style='font-size:0.95rem; font-weight:800; color:#10B981;'>Gradient Boosting</div>"
    "</div>"
    "</div>"
    "<div class='stat-ribbon-card' style='display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.15rem;'>⚡</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Inference Latency</div>"
    "<div style='font-size:0.95rem; font-weight:800; color:#D97706;'>&lt; 0.2 sec</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(stat_ribbon_html)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

gradient_boosting_model, scaler, label_encoder = None, None, None
model_ready = False

try:
    gradient_boosting_model, scaler, label_encoder = load_models()
    model_ready = True
    st.session_state["model_health"] = "OK"
except Exception as exc:
    st.session_state["model_health"] = "FAIL"
    render_error_banner(
        title="Scoring Engine Unavailable",
        detail=str(exc),
        suggestion="Check that /models contains gradient_boosting_model.pkl and scaler.pkl.",
    )
    st.stop()


def _build_customer_df(params):
    gender_num = 1 if str(params.get("Gender", "Male")).lower() in ("male", "1") else 0
    geo = str(params.get("Geography", "France"))
    return pd.DataFrame({
        "CreditScore": [float(params.get("CreditScore", 650))],
        "Gender": [gender_num],
        "Age": [float(params.get("Age", 35))],
        "Tenure": [float(params.get("Tenure", 5))],
        "Balance": [float(params.get("Balance", 50000.0))],
        "NumOfProducts": [float(params.get("NumOfProducts", 1))],
        "HasCrCard": [float(params.get("HasCrCard", 1))],
        "IsActiveMember": [float(params.get("IsActiveMember", 1))],
        "EstimatedSalary": [float(params.get("EstimatedSalary", 50000.0))],
        "Geography_Germany": [1.0 if geo == "Germany" else 0.0],
        "Geography_Spain": [1.0 if geo == "Spain" else 0.0],
    })


def _score(params):
    df = _build_customer_df(params)
    pred, pred_label, proba, risk = predict_customer(df, gradient_boosting_model, scaler)
    proba = sanitize_probability(proba)
    return df, pred, pred_label, proba, risk


def _risk_meta(p):
    if p < LOW_RISK_THRESHOLD:
        return {
            "class": "risk-low",
            "icon": "🟢",
            "label": LOW_RISK,
            "variant": "green",
            "bg_start": "#047857",
            "bg_mid": "#10B981",
            "bar_class": "probability-bar-low",
            "ribbon": "risk-ribbon-low",
        }
    if p < MEDIUM_RISK_THRESHOLD:
        return {
            "class": "risk-medium",
            "icon": "🟡",
            "label": MEDIUM_RISK,
            "variant": "amber",
            "bg_start": "#B45309",
            "bg_mid": "#F59E0B",
            "bar_class": "probability-bar-medium",
            "ribbon": "risk-ribbon-medium",
        }
    return {
        "class": "risk-high",
        "icon": "🔴",
        "label": HIGH_RISK,
        "variant": "red",
        "bg_start": "#991B1B",
        "bg_mid": "#EF4444",
        "bar_class": "probability-bar-high",
        "ribbon": "risk-ribbon-high",
    }


# -----------------------------------------------------------------------------
# Visually Impressive Guided 3-Step Process Banner
# -----------------------------------------------------------------------------
display_section_header(
    "Scenario Setup · Guided 3-Step Sandbox",
    "Follow the structured retention workflow: Define Baseline Customer → Apply Retention Levers → Inspect Real-Time Delta & Financial ROI.",
    accent_color="#0EA5E9",
)

stepper_html = (
    "<div style='background:linear-gradient(135deg, #F8FAFC 0%, #FFFFFF 100%); border:1.5px solid #BAE6FD; border-radius:14px; padding:1rem 1.25rem; margin-bottom:1.15rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.07);'>"
    "<div style='display:grid; grid-template-columns: repeat(3, 1fr); gap:0.85rem;'>"
    "<div style='background:#FFFFFF; border:1.5px solid #BAE6FD; border-radius:12px; padding:0.75rem 0.95rem; display:flex; align-items:center; gap:0.75rem; box-shadow:0 2px 6px rgba(14,165,233,0.08);'>"
    "<div style='width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.95rem; flex-shrink:0; box-shadow:0 2px 6px rgba(14,165,233,0.3);'>1</div>"
    "<div>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>🏁 Step 1: Baseline Profile</div>"
    "<div style='font-size:0.76rem; color:#64748B; margin-top:1px;'>Configure starting attributes &amp; risk score</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1.5px solid #DDD6FE; border-radius:12px; padding:0.75rem 0.95rem; display:flex; align-items:center; gap:0.75rem; box-shadow:0 2px 6px rgba(168,85,247,0.08);'>"
    "<div style='width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg, #A855F7 0%, #7E22CE 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.95rem; flex-shrink:0; box-shadow:0 2px 6px rgba(168,85,247,0.3);'>2</div>"
    "<div>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>🎚️ Step 2: Scenario Levers</div>"
    "<div style='font-size:0.76rem; color:#64748B; margin-top:1px;'>Toggle product bundling &amp; engagement</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1.5px solid #A7F3D0; border-radius:12px; padding:0.75rem 0.95rem; display:flex; align-items:center; gap:0.75rem; box-shadow:0 2px 6px rgba(16,185,129,0.08);'>"
    "<div style='width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:0.95rem; flex-shrink:0; box-shadow:0 2px 6px rgba(16,185,129,0.3);'>3</div>"
    "<div>"
    "<div style='font-weight:700; font-size:0.88rem; color:#0F172A;'>📈 Step 3: Impact Analysis</div>"
    "<div style='font-size:0.76rem; color:#64748B; margin-top:1px;'>Inspect score reduction &amp; net ROI</div>"
    "</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(stepper_html)

baseline_tab, scenario_tab, insight_tab = st.tabs([
    "🏁 Step 1: Baseline Profile",
    "🎚️ Step 2: Scenario Tuning",
    "📈 Step 3: Impact Analysis",
])

# =============================================================================
# STEP 1: BASELINE PROFILE (With Quick Archetype Presets)
# =============================================================================
with baseline_tab:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #BAE6FD; border-radius:12px; padding:0.75rem 1rem; margin-bottom:0.85rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
            <div style="font-size:0.84rem; font-weight:700; color:#0369A1;">⚡ Quick-Load Banking Archetype Preset:</div>
            <div style="font-size:0.78rem; color:#64748B;">Instantly populate realistic baseline parameters to test common retention scenarios.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    presets_list = [
        "🔴 High Risk: Middle-Aged German Inactive Client (Single Product)",
        "🟡 Medium Risk: Mature Dual-Product Deposit Holder",
        "🟢 Low Risk: Premier Young Active Multi-Product Member",
        "Custom Configuration",
    ]
    
    loaded_customer = st.session_state.get("loaded_customer_data")
    loaded_label = None
    if loaded_customer:
        cid = loaded_customer.get("CustomerId", "Profile")
        sname = loaded_customer.get("Surname", "Account")
        loaded_label = f"👤 Selected Account #{cid} ({sname})"
        presets_list = [loaded_label] + presets_list

    preset_choice = st.selectbox(
        "Select Archetype",
        presets_list,
        index=0 if loaded_label else 0,
        label_visibility="collapsed",
        key="baseline_preset_selector",
    )

    # Archetype default mappings
    if loaded_label and preset_choice == loaded_label:
        d_credit = int(loaded_customer.get("CreditScore", 650))
        d_age = int(loaded_customer.get("Age", 42))
        d_tenure = int(loaded_customer.get("Tenure", 5))
        d_balance = float(loaded_customer.get("Balance", 75000.0))
        d_salary = float(loaded_customer.get("EstimatedSalary", 60000.0))
        d_gender = str(loaded_customer.get("Gender", "Male"))
        d_geo = str(loaded_customer.get("Geography", "France"))
        d_prod = int(loaded_customer.get("NumOfProducts", 1))
        d_card = int(loaded_customer.get("HasCrCard", 1))
        d_active = int(loaded_customer.get("IsActiveMember", 0))
    elif "High Risk" in preset_choice:
        d_credit, d_age, d_tenure, d_balance, d_salary = 580, 48, 3, 125000.0, 85000.0
        d_gender, d_geo, d_prod, d_card, d_active = "Female", "Germany", 1, 0, 0
    elif "Medium Risk" in preset_choice:
        d_credit, d_age, d_tenure, d_balance, d_salary = 640, 41, 5, 80000.0, 65000.0
        d_gender, d_geo, d_prod, d_card, d_active = "Male", "France", 1, 1, 0
    elif "Low Risk" in preset_choice:
        d_credit, d_age, d_tenure, d_balance, d_salary = 750, 32, 7, 55000.0, 95000.0
        d_gender, d_geo, d_prod, d_card, d_active = "Male", "France", 2, 1, 1
    else:
        d_credit, d_age, d_tenure, d_balance, d_salary = 650, 42, 5, 75000.0, 60000.0
        d_gender, d_geo, d_prod, d_card, d_active = "Male", "France", 1, 1, 0

    col_b1, col_b2 = st.columns(2, gap="medium")

    with col_b1:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD;'>📊 Demographic &amp; Financial Baseline</span>"
            "</div>"
        )
        b_credit = st.slider("Credit Score", 300, 900, d_credit, 5, key="b_credit")
        b_age = st.slider("Age (Years)", 18, 100, d_age, 1, key="b_age")
        b_tenure = st.slider("Tenure (Years)", 0, 10, d_tenure, 1, key="b_tenure")
        b_balance = st.slider("Account Balance ($)", 0.0, 250000.0, d_balance, 1000.0, format="$%.0f", key="b_balance")
        b_salary = st.slider("Estimated Salary ($)", 0.0, 200000.0, d_salary, 1000.0, format="$%.0f", key="b_salary")

    with col_b2:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#FAF5FF; color:#7E22CE; border:1px solid #DDD6FE;'>🏦 Starting Products &amp; Branch</span>"
            "</div>"
        )
        b_gender = st.selectbox("Gender", ["Male", "Female"], index=0 if d_gender == "Male" else 1, key="b_gender")
        b_geo = st.selectbox("Geography", ["France", "Germany", "Spain"], index=["France", "Germany", "Spain"].index(d_geo), key="b_geo")
        b_products = st.selectbox("Number of Products", [1, 2, 3, 4], index=d_prod - 1, key="b_products")
        b_card = st.selectbox("Has Credit Card", [1, 0], index=0 if d_card == 1 else 1, format_func=lambda x: "Yes — Cardholder" if x == 1 else "No — No Card", key="b_card")
        b_active = st.selectbox("Active Member Status", [1, 0], index=0 if d_active == 1 else 1, format_func=lambda x: "Active — Engaged" if x == 1 else "Inactive — Low Engagement", key="b_active")

    baseline_params = {
        "CreditScore": b_credit, "Gender": b_gender, "Age": b_age, "Tenure": b_tenure,
        "Balance": b_balance, "NumOfProducts": b_products, "HasCrCard": b_card,
        "IsActiveMember": b_active, "EstimatedSalary": b_salary, "Geography": b_geo,
    }

    _, baseline_pred, baseline_pred_label, baseline_proba, baseline_risk = _score(baseline_params)
    baseline_meta = _risk_meta(baseline_proba)

    baseline_border_color = "#EF4444" if baseline_proba >= 0.70 else ("#F59E0B" if baseline_proba >= 0.30 else "#10B981")
    baseline_bg_tint = "#FEF2F2" if baseline_proba >= 0.70 else ("#FFFBEB" if baseline_proba >= 0.30 else "#F0FDF4")
    baseline_text_color = "#DC2626" if baseline_proba >= 0.70 else ("#D97706" if baseline_proba >= 0.30 else "#059669")

    baseline_banner_html = (
        f"<div style='margin-top:1.25rem; background:#FFFFFF; border:1.5px solid #E2E8F0; border-left:6px solid {baseline_border_color}; border-radius:14px; padding:1.15rem 1.35rem; box-shadow:0 4px 18px -2px rgba(15,23,42,0.06);'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;'>"
        f"<div style='display:flex; align-items:flex-start; gap:0.9rem; flex:1; min-width:280px;'>"
        f"<div style='width:44px; height:44px; border-radius:12px; background:{baseline_bg_tint}; border:1px solid {baseline_border_color}; display:flex; align-items:center; justify-content:center; font-size:1.35rem; flex-shrink:0;'>{baseline_meta['icon']}</div>"
        f"<div>"
        f"<div style='display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;'>"
        f"<span class='filter-header-badge' style='background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD;'>🏁 Baseline · Starting Customer Profile</span>"
        f"</div>"
        f"<h3 style='margin:0; font-size:1.15rem; font-weight:800; color:#0F172A;'>{baseline_risk} · {baseline_pred_label}</h3>"
        f"<div style='font-size:0.84rem; color:#475569; margin-top:0.3rem; line-height:1.5;'>"
        f"Starting predicted churn probability before scenario intervention. "
        f"Switch to <b>Step 2 (Scenario Tuning)</b> to toggle retention levers and observe live probability deltas."
        f"</div>"
        f"</div>"
        f"</div>"
        f"<div style='flex-shrink:0; background:{baseline_bg_tint}; border:1.5px solid {baseline_border_color}; border-radius:12px; padding:0.75rem 1.25rem; text-align:center; min-width:180px; box-shadow:0 2px 8px rgba(0,0,0,0.04);'>"
        f"<div style='font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#64748B; margin-bottom:0.2rem;'>Baseline Churn Score</div>"
        f"<div style='font-size:2.1rem; font-weight:900; color:{baseline_text_color}; line-height:1.1;'>{baseline_proba:.1%}</div>"
        f"<div style='font-size:0.75rem; font-weight:700; color:{baseline_text_color}; margin-top:0.25rem;'>{baseline_risk}</div>"
        f"</div>"
        f"</div>"
        f"</div>"
    )
    render_raw_html(baseline_banner_html)

# =============================================================================
# STEP 2: SCENARIO TUNING (With Retention Strategy Packages)
# =============================================================================
with scenario_tab:
    st.markdown(
        """
        <div style="background:#FFFFFF; border:1px solid #DDD6FE; border-radius:12px; padding:0.75rem 1rem; margin-bottom:0.85rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;">
            <div style="font-size:0.84rem; font-weight:700; color:#6D28D9;">🎯 1-Click Retention Playbook Strategy:</div>
            <div style="font-size:0.78rem; color:#64748B;">Select an institutional intervention campaign to automatically apply proven retention levers.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    strategy_preset = st.selectbox(
        "Playbook Strategy",
        [
            "Custom Manual Lever Configuration",
            "🚀 Strategy A: Digital Engagement & App Onboarding (Activate Membership)",
            "🎁 Strategy B: Multi-Product Cross-Sell Campaign (+1 Secondary Product)",
            "💎 Strategy C: Comprehensive VIP Relationship Package (Activate + Product 2 + Credit Card)",
        ],
        index=3 if baseline_proba > 0.50 else 2,
        label_visibility="collapsed",
        key="strategy_preset_selector",
    )

    # Strategy mappings
    auto_active = True if "Strategy A" in strategy_preset or "Strategy C" in strategy_preset else False
    auto_prod = True if "Strategy B" in strategy_preset or "Strategy C" in strategy_preset else False
    auto_card = True if "Strategy C" in strategy_preset else False

    col_s1, col_s2 = st.columns(2, gap="medium")

    with col_s1:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD;'>📊 Financial &amp; Demographic Modifiers</span>"
            "</div>"
        )
        mod_credit = st.checkbox(f"Override Credit Score (baseline: {b_credit:,})", value=False, key="mod_credit_toggle")
        s_credit = st.slider("Scenario Credit Score", 300, 900, b_credit, 5, key="s_credit", disabled=not mod_credit)

        mod_age = st.checkbox(f"Override Age (baseline: {b_age} yrs)", value=False, key="mod_age_toggle")
        s_age = st.slider("Scenario Age", 18, 100, b_age, 1, key="s_age", disabled=not mod_age)

        mod_tenure = st.checkbox(f"Override Tenure (baseline: {b_tenure} yrs)", value=False, key="mod_tenure_toggle")
        s_tenure = st.slider("Scenario Tenure (yrs)", 0, 10, b_tenure, 1, key="s_tenure", disabled=not mod_tenure)

        mod_balance = st.checkbox(f"Override Balance (baseline: ${b_balance:,.0f})", value=False, key="mod_balance_toggle")
        s_balance = st.slider("Scenario Balance ($)", 0.0, 250000.0, b_balance, 1000.0, format="$%.0f", key="s_balance", disabled=not mod_balance)

        mod_salary = st.checkbox(f"Override Salary (baseline: ${b_salary:,.0f})", value=False, key="mod_salary_toggle")
        s_salary = st.slider("Scenario Salary ($)", 0.0, 200000.0, b_salary, 1000.0, format="$%.0f", key="s_salary", disabled=not mod_salary)

    with col_s2:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#FAF5FF; color:#7E22CE; border:1px solid #DDD6FE;'>🏦 High-Impact Retention Levers</span>"
            "</div>"
        )
        mod_active = st.checkbox(f"Lever 1: Toggle Active Membership (baseline: {'Active' if b_active == 1 else 'Inactive'})", value=auto_active or (b_active == 0), key="mod_active_toggle")
        s_active = st.selectbox("Scenario Active Status", [1, 0], index=0, format_func=lambda x: "Active — Engaged" if x == 1 else "Inactive", key="s_active", disabled=not mod_active)

        mod_products = st.checkbox(f"Lever 2: Bundle Secondary Product (baseline: {b_products})", value=auto_prod or (b_products == 1), key="mod_products_toggle")
        s_products = st.selectbox("Scenario Product Count", [1, 2, 3, 4], index=1, key="s_products", disabled=not mod_products)

        mod_card = st.checkbox(f"Lever 3: Issue Credit Card (baseline: {'Yes' if b_card == 1 else 'No'})", value=auto_card, key="mod_card_toggle")
        s_card = st.selectbox("Scenario Credit Card", [1, 0], index=0, format_func=lambda x: "Yes" if x == 1 else "No", key="s_card", disabled=not mod_card)

        mod_geo = st.checkbox(f"Override Country (baseline: {b_geo})", value=False, key="mod_geo_toggle")
        s_geo = st.selectbox("Scenario Country", ["France", "Germany", "Spain"], index=["France", "Germany", "Spain"].index(b_geo), key="s_geo", disabled=not mod_geo)

    scenario_params = {
        "CreditScore": s_credit if mod_credit else b_credit,
        "Gender": b_gender,
        "Age": s_age if mod_age else b_age,
        "Tenure": s_tenure if mod_tenure else b_tenure,
        "Balance": s_balance if mod_balance else b_balance,
        "NumOfProducts": s_products if mod_products else b_products,
        "HasCrCard": s_card if mod_card else b_card,
        "IsActiveMember": s_active if mod_active else b_active,
        "EstimatedSalary": s_salary if mod_salary else b_salary,
        "Geography": s_geo if mod_geo else b_geo,
    }

    _, scenario_pred, scenario_pred_label, scenario_proba, scenario_risk = _score(scenario_params)
    scenario_meta = _risk_meta(scenario_proba)

    delta_abs, delta_pct = compute_safe_delta(baseline_proba, scenario_proba)

    scenario_border_color = "#EF4444" if scenario_proba >= 0.70 else ("#F59E0B" if scenario_proba >= 0.30 else "#10B981")
    scenario_bg_tint = "#FEF2F2" if scenario_proba >= 0.70 else ("#FFFBEB" if scenario_proba >= 0.30 else "#F0FDF4")
    scenario_text_color = "#DC2626" if scenario_proba >= 0.70 else ("#D97706" if scenario_proba >= 0.30 else "#059669")
    delta_badge_class = "pill-green" if delta_abs < -0.005 else ("pill-red" if delta_abs > 0.005 else "pill-amber")

    scenario_banner_html = (
        f"<div style='margin-top:1.25rem; background:#FFFFFF; border:1.5px solid #E2E8F0; border-left:6px solid {scenario_border_color}; border-radius:14px; padding:1.15rem 1.35rem; box-shadow:0 4px 18px -2px rgba(15,23,42,0.06);'>"
        f"<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:1rem;'>"
        f"<div style='display:flex; align-items:flex-start; gap:0.9rem; flex:1; min-width:280px;'>"
        f"<div style='width:44px; height:44px; border-radius:12px; background:{scenario_bg_tint}; border:1px solid {scenario_border_color}; display:flex; align-items:center; justify-content:center; font-size:1.35rem; flex-shrink:0;'>{scenario_meta['icon']}</div>"
        f"<div>"
        f"<div style='display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;'>"
        f"<span class='filter-header-badge' style='background:#FAF5FF; color:#7E22CE; border:1px solid #DDD6FE;'>🎚️ Scenario · Modified Customer Profile</span>"
        f"</div>"
        f"<h3 style='margin:0; font-size:1.15rem; font-weight:800; color:#0F172A;'>{scenario_risk} · {scenario_pred_label}</h3>"
        f"<div style='font-size:0.84rem; color:#475569; margin-top:0.3rem; line-height:1.5;'>"
        f"Churn probability changed by <b style='color:#0F172A;'>{delta_abs:+.1%}</b> ({delta_pct:+.1f}% relative change). "
        f"Switch to <b>Step 3 (Impact Analysis)</b> to inspect the full comparison scorecards, charts, and estimated financial ROI."
        f"</div>"
        f"</div>"
        f"</div>"
        f"<div style='flex-shrink:0; background:{scenario_bg_tint}; border:1.5px solid {scenario_border_color}; border-radius:12px; padding:0.75rem 1.25rem; text-align:center; min-width:180px; box-shadow:0 2px 8px rgba(0,0,0,0.04);'>"
        f"<div style='font-size:0.7rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#64748B; margin-bottom:0.2rem;'>Scenario Churn Score</div>"
        f"<div style='font-size:2.1rem; font-weight:900; color:{scenario_text_color}; line-height:1.1;'>{scenario_proba:.1%}</div>"
        f"<div style='margin-top:0.25rem;'><span class='pill {delta_badge_class}' style='font-size:0.75rem;'><b>{delta_abs:+.1%}</b> vs baseline</span></div>"
        f"</div>"
        f"</div>"
        f"</div>"
    )
    render_raw_html(scenario_banner_html)

# =============================================================================
# STEP 3: IMPACT ANALYSIS & FINANCIAL ROI SANDBOX
# =============================================================================
with insight_tab:
    display_section_header(
        "Impact Analysis · Baseline vs Scenario",
        "Side-by-side comparison: probability score deltas, risk-tier migration, and recommended playbook.",
        accent_color="#10B981",
    )

    improved = delta_abs < -0.005
    worsened = delta_abs > 0.005
    d_variant = "green" if improved else ("red" if worsened else "amber")
    d_icon = "📉" if improved else ("📈" if worsened else "➖")
    d_header = "Retention Win" if improved else ("Risk Elevated" if worsened else "Neutral Impact")

    # Estimated CLV Value Protected: Baseline Balance * Delta Absolute
    est_balance = float(scenario_params["Balance"])
    clv_protected = max(0.0, -delta_abs * est_balance)

    col_w1, col_w2, col_w3 = st.columns([1, 1, 1.2], gap="medium")

    with col_w1:
        c1_html = (
            f"<div class='card-surface card-gradient-{baseline_meta['variant']}'>"
            f"<div class='card-header'><div class='card-icon card-icon-blue'>🏁</div><div><div class='card-title'>Baseline Profile</div><h3 style='margin:0; font-size:1rem;'>Starting Risk</h3></div></div>"
            f"<div class='card-value' style='font-size:2.2rem; margin:0.4rem 0;'>{baseline_proba:.1%}</div>"
            f"<span class='pill pill-{baseline_meta['variant']}'>{baseline_risk}</span>"
            f"</div>"
        )
        render_raw_html(c1_html)

    with col_w2:
        c2_html = (
            f"<div class='card-surface card-gradient-{scenario_meta['variant']}'>"
            f"<div class='card-header'><div class='card-icon card-icon-purple'>🎚️</div><div><div class='card-title'>Modified Scenario</div><h3 style='margin:0; font-size:1rem;'>Post-Lever Risk</h3></div></div>"
            f"<div class='card-value' style='font-size:2.2rem; margin:0.4rem 0;'>{scenario_proba:.1%}</div>"
            f"<span class='pill pill-{scenario_meta['variant']}'>{scenario_risk}</span>"
            f"</div>"
        )
        render_raw_html(c2_html)

    with col_w3:
        status_msg = '✅ Retention levers successfully lowered churn probability.' if improved else ('⚠️ Changes increased attrition risk.' if worsened else 'ℹ️ Minimal move.')
        c3_html = (
            f"<div class='card-surface card-gradient-{d_variant}'>"
            f"<div class='card-header'><div class='card-icon card-icon-{d_variant}'>{d_icon}</div><div><div class='card-title'>Net Impact</div><h3 style='margin:0; font-size:1rem;'>{d_header}</h3></div></div>"
            f"<div style='display:grid; grid-template-columns:1fr 1fr; gap:0.5rem; margin:0.4rem 0;'>"
            f"<div style='background:#FFF; padding:0.5rem 0.7rem; border-radius:10px; border:1px solid #E2E8F0;'><div class='card-title' style='font-size:0.68rem;'>Absolute Δ</div><div style='font-size:1.25rem; font-weight:800; color:#0F172A;'>{delta_abs:+.2%}</div></div>"
            f"<div style='background:#FFF; padding:0.5rem 0.7rem; border-radius:10px; border:1px solid #E2E8F0;'><div class='card-title' style='font-size:0.68rem;'>Relative Δ</div><div style='font-size:1.25rem; font-weight:800; color:#0F172A;'>{delta_pct:+.1f}%</div></div>"
            f"</div>"
            f"<div style='font-size:0.82rem; color:#475569;'>{status_msg}</div>"
            f"</div>"
        )
        render_raw_html(c3_html)

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    # Side-by-Side: Plotly Bar Chart & Financial ROI Card
    col_c1, col_c2 = st.columns([1.3, 1], gap="medium")

    with col_c1:
        fig_comp = go.Figure()
        fig_comp.add_trace(
            go.Bar(
                x=["Baseline Starting Profile", "Modified Retention Scenario"],
                y=[baseline_proba * 100, scenario_proba * 100],
                marker_color=[baseline_meta["bg_mid"], scenario_meta["bg_mid"]],
                text=[f"{baseline_proba:.1%}", f"{scenario_proba:.1%}"],
                textposition="outside",
                textfont=dict(size=14, family="Inter, Segoe UI", color="#0F172A", weight="bold"),
                width=0.42,
            )
        )
        fig_comp = apply_dashboard_style(
            fig_comp,
            title="Baseline vs Scenario Churn Probability Delta",
            x_title="",
            y_title="Predicted Churn Probability (%)",
            height=370,
        )
        fig_comp.update_yaxes(range=[0, 105], dtick=20)
        st.plotly_chart(fig_comp, use_container_width=True, config=PLOTLY_CONFIG, key="chart_scenario_comp")

    with col_c2:
        roi_card_html = (
            "<div style='background:linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%); border:1.5px solid #BBF7D0; border-radius:14px; padding:1.15rem 1.35rem; box-shadow:0 4px 18px -2px rgba(16,185,129,0.08); height:100%; box-sizing:border-box;'>"
            "<div style='display:flex; align-items:center; gap:0.5rem; margin-bottom:0.4rem;'>"
            "<div style='width:32px; height:32px; border-radius:8px; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1rem; font-weight:700;'>💰</div>"
            "<div style='font-weight:800; color:#065F46; font-size:0.96rem;'>Simulated Retention ROI &amp; Value Saved</div>"
            "</div>"
            f"<div style='margin:0.75rem 0; padding:0.75rem 0.95rem; background:#FFFFFF; border:1px solid #A7F3D0; border-radius:10px;'>"
            f"<div style='font-size:0.72rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Estimated Deposit Value Protected</div>"
            f"<div style='font-size:1.8rem; font-weight:800; color:#047857; line-height:1.2; margin:0.2rem 0;'>{format_currency(clv_protected)}</div>"
            f"<div style='font-size:0.76rem; color:#64748B;'>Based on ${est_balance:,.0f} balance exposure × {abs(delta_abs):.1%} risk mitigation.</div>"
            f"</div>"
            "<div style='font-size:0.8rem; color:#334155; line-height:1.5;'>"
            "• <b>Intervention Recommendation</b>: Enroll client in digital engagement onboarding &amp; issue secondary product bundle offer.<br>"
            "• <b>Executive Budget</b>: Allocate up to <b>$250</b> retention incentive against the estimated <b>"
            + format_currency(clv_protected) + "</b> deposit protection."
            "</div>"
            "</div>"
        )
        render_raw_html(roi_card_html)
