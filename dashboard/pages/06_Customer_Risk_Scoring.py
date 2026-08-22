import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import io
import streamlit as st
import pandas as pd

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.header import display_brand_header
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row

from services.model_loader import load_models
from services.prediction import predict_customer, predict_batch
from services.explainability_service import ExplainabilityService

from components.prediction_form import customer_prediction_form
from components.result_card import display_prediction_result
from components.recommendation import display_recommendation
from components.customer_summary import display_customer_summary
from components.feature_importance import display_feature_importance
from components.probability_distribution import display_probability_distribution
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


st.set_page_config(
    page_title="Customer Risk Scoring | Bank Churn Intelligence",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

# -----------------------------------------------------------------------------
# Compact Hero Header & Status Badges
# -----------------------------------------------------------------------------
compact_header_html = (
    "<div style='background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; border-radius:14px; padding:0.9rem 1.25rem; margin-bottom:0.75rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.06);'>"
    "<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>"
    "<div style='display:flex; align-items:center; gap:0.75rem;'>"
    "<div style='width:36px; height:36px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700;'>🔮</div>"
    "<div>"
    "<h1 style='margin:0; font-size:1.25rem; font-weight:800; color:#0F172A; line-height:1.2;'>Customer Risk Scoring Studio</h1>"
    "<div style='font-size:0.8rem; color:#64748B; margin-top:2px;'>Enterprise real-time predictive scoring — individual intake, calibrated churn probability, 3 risk tiers, and retention playbooks.</div>"
    "</div>"
    "</div>"
    "<div style='display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;'>"
    "<span class='pill pill-purple' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🔮 Real-Time Scoring</span>"
    "<span class='pill pill-blue' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>📁 Batch CSV</span>"
    "<span class='pill pill-green' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🎯 86.31% CV Accuracy</span>"
    "<span class='pill pill-amber' style='font-size:0.72rem; padding:0.2rem 0.55rem;'>🧠 Explainable AI</span>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(compact_header_html)

# -----------------------------------------------------------------------------
# Compact 4-Metric Horizontal Stat Ribbon
# -----------------------------------------------------------------------------
stat_ribbon_html = (
    "<div style='display:grid; grid-template-columns: repeat(4, 1fr); gap:0.65rem; margin-bottom:0.85rem;'>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>⚡</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Inference Speed</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#0F172A;'>&lt; 0.2 sec</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🗂️</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Scoring Modes</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#0284C7;'>Single &amp; Batch</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🎚️</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Calibrated Tiers</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#7E22CE;'>3 Tiers (&lt;30, 70)</div>"
    "</div>"
    "</div>"
    "<div style='background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.55rem 0.85rem; display:flex; align-items:center; gap:0.6rem;'>"
    "<div style='font-size:1.1rem;'>🏆</div>"
    "<div>"
    "<div style='font-size:0.68rem; color:#64748B; font-weight:600; text-transform:uppercase;'>Production Model</div>"
    "<div style='font-size:0.92rem; font-weight:800; color:#10B981;'>Gradient Boosting</div>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(stat_ribbon_html)

try:
    gradient_boosting_model, scaler, label_encoder = load_models()
    model_loaded = True
except Exception as error:
    model_loaded = False
    error_message = error

try:
    X_test = ExplainabilityService.load_x_test()
except Exception:
    X_test = None

if not model_loaded:
    render_error_banner(
        title="Scoring Engine Offline",
        detail=f"Unable to load production model: {error_message}",
        suggestion="Verify that model files exist in /models/ directory.",
    )
    st.stop()

# -----------------------------------------------------------------------------
# Studio Tabs
# -----------------------------------------------------------------------------
predict_tab, batch_tab, playbook_tab = st.tabs([
    "🔮 Individual Customer Risk Scoring",
    "📁 Batch CSV Customer Scoring",
    "📦 Risk Framework & Retention Playbook",
])

# =============================================================================
# TAB 1: INDIVIDUAL CUSTOMER RISK SCORING
# =============================================================================
with predict_tab:
    display_section_header(
        "Individual Customer Intake & Parameters",
        "Enter customer demographic and financial parameters or choose a preset persona to score real-time churn risk.",
        accent_color="#0EA5E9",
    )

    col_th1, col_th2 = st.columns([1.5, 1], gap="medium")
    with col_th1:
        threshold_choice = st.selectbox(
            "Operating Decision Policy Threshold:",
            [
                "⭐ Recommended Policy (0.35) — Optimal Retention Campaign (Max F1: 68.9%, Recall: 72.4%)",
                "🎯 Standard Precision Policy (0.50) — High-Conviction Calls (Precision: 78.6%)",
                "⚡ Early Warning Digital Policy (0.20) — Automated Nudges (Recall: 84.2%)",
            ],
            index=0,
            help="Choose the operating probability threshold to classify customer churn."
        )
    with col_th2:
        if "0.35" in threshold_choice:
            active_threshold = 0.35
            st.info("💡 **0.35 Policy**: Captures +23.8% more churners with balanced outreach cost.")
        elif "0.50" in threshold_choice:
            active_threshold = 0.50
            st.info("💡 **0.50 Policy**: Zero-waste precision, ideal for expensive fee waivers.")
        else:
            active_threshold = 0.20
            st.info("💡 **0.20 Policy**: High-sensitivity safety net for email marketing campaigns.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    customer_data, predict_button = customer_prediction_form()

    if predict_button:
        try:
            prediction, prediction_label, probability, risk_level = predict_customer(
                customer_data,
                gradient_boosting_model,
                scaler,
                decision_threshold=active_threshold,
            )

            render_success_banner(
                title="Customer Scored Successfully",
                detail=f"Calculated Churn Probability: <b>{probability:.1%}</b> ({risk_level}) | Policy Threshold: <b>{active_threshold:.2f}</b> &rarr; <b>{prediction_label}</b>.",
            )

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Visually Dominant Result
            display_section_header(
                "Prediction Outcome & Calibrated Risk Tier",
                "Dominant risk classification, calibrated probability estimate, and confidence signal.",
                accent_color="#EF4444",
            )
            display_prediction_result(prediction_label, probability, risk_level)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Cohort Benchmark
            display_section_header(
                "Cohort Distribution Benchmark",
                "Where this customer sits relative to the 2,000-record holdout test cohort.",
                accent_color="#0EA5E9",
            )
            display_probability_distribution(
                customer_probability=probability,
                model=gradient_boosting_model,
                scaler=scaler,
                X_test=X_test,
            )

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Retention Recommendation Playbook
            display_section_header(
                "Actionable Retention Playbook",
                "Prescriptive operational intervention steps and SLAs tailored to this risk profile.",
                accent_color="#F59E0B",
            )
            display_recommendation(probability)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Customer Summary Snapshot
            display_section_header(
                "Customer Profile Snapshot",
                "Decoded attribute profile submitted for real-time scoring.",
                accent_color="#0EA5E9",
            )
            display_customer_summary(customer_data)

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            # Feature Importance Drivers
            display_section_header(
                "Model Feature Importance Drivers",
                "Ranked feature contributions for this customer prediction.",
                accent_color="#10B981",
            )
            display_feature_importance(
                gradient_boosting_model,
                customer_data.columns.tolist(),
                customer_probability=probability,
            )

            # Export Customer Retention Brief
            st.markdown('<div style="height:0.8rem;"></div>', unsafe_allow_html=True)
            brief_bg = "#DC2626" if probability >= 0.60 else ("#D97706" if probability >= 0.30 else "#059669")
            cust_table_rows = "".join([f"<tr><td style='padding:6px 10px; border-bottom:1px solid #E2E8F0; font-weight:600;'>{col}</td><td style='padding:6px 10px; border-bottom:1px solid #E2E8F0;'>{customer_data[col].values[0]}</td></tr>" for col in customer_data.columns])
            brief_html = f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Customer Retention Brief</title>
<style>
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin: 40px; color: #0F172A; line-height: 1.5; }}
.header {{ border-bottom: 2px solid #0284C7; padding-bottom: 12px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; }}
.badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: bold; color: white; background: {brief_bg}; }}
.grid {{ display: grid; grid-template-columns: 1.2fr 1fr; gap: 20px; margin: 20px 0; }}
.card {{ background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 12px; padding: 18px; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 8px; font-size: 13px; }}
</style>
</head>
<body>
<div class="header">
<div><h2 style="margin:0; color:#0F172A;">🏦 Bank Customer Churn Intelligence · Client Retention Brief</h2><p style="margin:4px 0 0 0; color:#64748B; font-size:13px;">Confidential Relationship Management Dossier</p></div>
<div><span class="badge">{risk_level} (Score: {probability*100:.1f} / 100)</span></div>
</div>
<div class="grid">
<div class="card"><h3 style="margin-top:0; color:#0369A1;">📊 Calibrated Risk Profile</h3><p><b>Predicted Churn Probability:</b> {probability:.1%}</p><p><b>Standardized Risk Score:</b> {probability*100:.1f} / 100</p><p><b>Operational Risk Tier:</b> {risk_level}</p><p><b>Status Classification:</b> {prediction_label}</p></div>
<div class="card"><h3 style="margin-top:0; color:#0369A1;">👤 Account Attribute Snapshot</h3><table>{cust_table_rows}</table></div>
</div>
<div class="card"><h3 style="margin-top:0; color:#065F46;">🧭 Recommended Action Protocol</h3><p>Initiate proactive relationship management outreach. Propose customized rate incentives, product bundling, or fee structure reviews aligned with the customer's historical engagement profile.</p></div>
<footer style="margin-top:30px; font-size:11px; color:#94A3B8; text-align:center;">Generated by Bank Customer Churn Intelligence &amp; Risk Platform · Champion Gradient Boosting Model</footer>
</body>
</html>"""

            st.download_button(
                label="📄 Export 1-Page Customer Retention Brief (HTML / Printable)",
                data=brief_html,
                file_name="customer_retention_brief.html",
                mime="text/html",
                use_container_width=True,
                type="primary",
            )

        except Exception as exc:
            render_error_banner(
                title="Scoring Failed",
                detail=str(exc),
            )

# =============================================================================
# TAB 2: BATCH CSV SCORING
# =============================================================================
with batch_tab:
    display_section_header(
        "High-Throughput Batch Scoring Engine",
        "Upload a CSV dataset of customer records to score all accounts simultaneously and download the enriched report.",
        accent_color="#A855F7",
    )

    sample_template_csv = "CreditScore,Gender,Age,Tenure,Balance,NumOfProducts,HasCrCard,IsActiveMember,EstimatedSalary,Geography\n650,Male,35,5,50000.0,1,1,0,50000.0,France\n580,Female,48,3,125000.0,1,0,0,85000.0,Germany\n720,Male,32,8,65000.0,2,1,1,95000.0,France\n690,Female,52,6,180000.0,1,1,0,140000.0,Spain\n"

    col_hdr1, col_hdr2 = st.columns([2, 1], gap="medium")
    with col_hdr1:
        render_raw_html(
            "<div class='hero-card' style='margin-bottom:0;'>"
            "<div style='font-weight:700; color:#0F172A; font-size:0.92rem; margin-bottom:0.25rem;'>📋 Required CSV Columns</div>"
            "<div style='font-size:0.84rem; color:#334155;'>"
            "<code>CreditScore</code>, <code>Age</code>, <code>Tenure</code>, <code>Balance</code>, <code>NumOfProducts</code>, <code>HasCrCard</code>, <code>IsActiveMember</code>, <code>EstimatedSalary</code>, <code>Gender</code>, <code>Geography</code>."
            "</div>"
            "</div>"
        )
    with col_hdr2:
        st.download_button(
            label="📥 Download Sample Batch Template (.CSV)",
            data=sample_template_csv,
            file_name="sample_batch_template.csv",
            mime="text/csv",
            help="Download a clean pre-formatted CSV template with standard column headers.",
            use_container_width=True,
        )

    uploaded_file = st.file_uploader(
        "Choose a CSV file for Batch Scoring",
        type=["csv"],
        help="Upload customer dataset in CSV format."
    )

    col_u1, col_u2 = st.columns([1, 1], gap="medium")
    with col_u1:
        use_sample = st.checkbox("Or test with Sample Batch from Holdout Cohort (200 Customers)", value=False)
    with col_u2:
        batch_threshold_choice = st.selectbox(
            "Batch Decision Policy Threshold:",
            [
                "⭐ Recommended Policy (0.35) — Optimal Retention (Max F1)",
                "🎯 Standard Precision Policy (0.50) — Minimum False Alarms",
                "⚡ Early Warning Policy (0.20) — High Sensitivity",
            ],
            index=0,
            key="batch_thresh_select"
        )
        batch_threshold = 0.35 if "0.35" in batch_threshold_choice else (0.50 if "0.50" in batch_threshold_choice else 0.20)

    if uploaded_file is not None or use_sample:
        try:
            if uploaded_file is not None:
                batch_raw = pd.read_csv(uploaded_file)
            else:
                from services.data_service import DataService
                batch_raw = DataService.load_dataset().sample(n=min(200, len(DataService.load_dataset())), random_state=42)

            with st.spinner("Scoring batch dataset through Gradient Boosting pipeline..."):
                scored_batch = predict_batch(
                    batch_raw,
                    gradient_boosting_model,
                    scaler,
                    decision_threshold=batch_threshold
                )

            high_risk_count = (scored_batch["Risk_Tier"] == "High Risk").sum()
            med_risk_count = (scored_batch["Risk_Tier"] == "Medium Risk").sum()
            low_risk_count = (scored_batch["Risk_Tier"] == "Low Risk").sum()
            total_scored = len(scored_batch)

            render_success_banner(
                title=f"Batch Scoring Complete: {total_scored:,} Customers Processed",
                detail=f"Found <b>{high_risk_count:,} High-Risk</b>, <b>{med_risk_count:,} Medium-Risk</b>, and <b>{low_risk_count:,} Low-Risk</b> accounts.",
            )

            st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

            b_kpis = [
                {"title": "Total Processed", "value": f"{total_scored:,}", "icon": "👥", "variant": "blue",
                 "subtitle": "Accounts evaluated"},
                {"title": "High-Risk Accounts", "value": f"{high_risk_count:,}", "icon": "🔴", "variant": "red",
                 "subtitle": f"{high_risk_count / total_scored * 100:.1f}% priority retention"},
                {"title": "Medium-Risk Accounts", "value": f"{med_risk_count:,}", "icon": "🟡", "variant": "amber",
                 "subtitle": f"{med_risk_count / total_scored * 100:.1f}% nurture candidates"},
                {"title": "Low-Risk (Stable)", "value": f"{low_risk_count:,}", "icon": "🟢", "variant": "green",
                 "subtitle": f"{low_risk_count / total_scored * 100:.1f}% healthy accounts"},
            ]
            render_kpi_row(b_kpis, cols=4)

            st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)

            st.dataframe(
                scored_batch[[
                    c for c in ["CustomerId", "Surname", "CreditScore", "Age", "Geography", "Balance", "NumOfProducts", "IsActiveMember", "Risk_Score", "Churn_Probability_Pct", "Risk_Tier", "Predicted_Status"]
                    if c in scored_batch.columns
                ]],
                use_container_width=True,
                hide_index=True,
            )

            # High-Risk Priority Queue (Ranked by Risk Score descending)
            high_risk_subset = scored_batch[scored_batch["Risk_Tier"] == "High Risk"].sort_values(by="Risk_Score", ascending=False)
            if not high_risk_subset.empty:
                st.markdown('<div style="height:0.5rem;"></div>', unsafe_allow_html=True)
                display_section_header(
                    "High-Risk Customer Priority Queue (Ranked by Risk Score)",
                    "Accounts with elevated attrition likelihood prioritized for targeted retention outreach.",
                    accent_color="#EF4444",
                )
                st.dataframe(
                    high_risk_subset[[
                        c for c in ["CustomerId", "Surname", "CreditScore", "Age", "Geography", "Balance", "NumOfProducts", "Risk_Score", "Churn_Probability_Pct", "Predicted_Status"]
                        if c in high_risk_subset.columns
                    ]],
                    use_container_width=True,
                    hide_index=True,
                )

            # CSV Download
            csv_buffer = io.StringIO()
            scored_batch.to_csv(csv_buffer, index=False)
            st.download_button(
                label="📥 Download Enriched Batch Risk Report (CSV)",
                data=csv_buffer.getvalue(),
                file_name="bank_customer_risk_scores.csv",
                mime="text/csv",
                type="primary",
            )

        except Exception as exc:
            render_error_banner(
                title="Batch Scoring Error",
                detail=str(exc),
                suggestion="Ensure your CSV columns match the expected schema.",
            )

# =============================================================================
# TAB 3: RISK FRAMEWORK & PLAYBOOK
# =============================================================================
with playbook_tab:
    display_section_header(
        "Enterprise Risk Framework & Tier Playbook",
        "Operational retention thresholds and intervention protocols defined for retail banking teams.",
        accent_color="#10B981",
    )

    col_pb1, col_pb2 = st.columns([1.1, 1], gap="medium")
    with col_pb1:
        card1_html = (
            "<div class='card-surface card-gradient-green' style='height:100%;'>"
            "<div class='card-header'>"
            "<div class='card-icon card-icon-green'>📦</div>"
            "<div>"
            "<div class='card-title'>Risk Scoring Architecture</div>"
            "<h3 style='margin:0; font-size:1.05rem; color:#0F172A;'>Comprehensive Risk Package</h3>"
            "</div>"
            "</div>"
            "<ul class='list-clean' style='margin-top:0.8rem;'>"
            "<li><span class='list-check'>✓</span><b>Continuous Churn Probability Score</b> — calibrated 0.0% to 100.0% likelihood</li>"
            "<li><span class='list-check'>✓</span><b>Standardized Risk Score (0–100)</b> — <code>Risk Score = Probability × 100</code></li>"
            "<li><span class='list-check'>✓</span><b>3-Tier Calibrated Classification</b> — Low (0–29) · Medium (30–59) · High (60–100)</li>"
            "<li><span class='list-check'>✓</span><b>Cohort Distribution Benchmark</b> — percentile ranking vs 2,000 hold-out accounts</li>"
            "<li><span class='list-check'>✓</span><b>Actionable Strategy Recommendations</b> — SLA-based retention playbooks</li>"
            "<li><span class='list-check'>✓</span><b>Feature Driver Importance &amp; PDP</b> — ranked SHAP &amp; Partial Dependence trends</li>"
            "</ul>"
            "</div>"
        )
        render_raw_html(card1_html)

    with col_pb2:
        card2_html = (
            "<div class='card-surface card-gradient-amber' style='height:100%;'>"
            "<div class='card-header'>"
            "<div class='card-icon card-icon-amber'>🧭</div>"
            "<div>"
            "<div class='card-title'>Intervention SLAs</div>"
            "<h3 style='margin:0; font-size:1.05rem; color:#0F172A;'>Tier-Based Action Matrix</h3>"
            "</div>"
            "</div>"
            "<div style='margin-top:0.75rem; display:flex; flex-direction:column; gap:0.5rem;'>"
            "<div style='padding:0.65rem 0.85rem; background:#FFF; border-radius:10px; border-left:4px solid #10B981;'>"
            "<div style='font-weight:700; color:#10B981; font-size:0.88rem;'>🟢 Low Risk (0–29 / &lt;30%)</div>"
            "<div style='font-size:0.8rem; color:#475569;'>Standard nurture, CLV expansion, relationship growth and deposit accumulation.</div>"
            "</div>"
            "<div style='padding:0.65rem 0.85rem; background:#FFF; border-radius:10px; border-left:4px solid #F59E0B;'>"
            "<div style='font-weight:700; color:#F59E0B; font-size:0.88rem;'>🟠 Medium Risk (30–59 / 30–59%)</div>"
            "<div style='font-size:0.8rem; color:#475569;'>7-day proactive outreach, personalized rate locks, multi-product bundle offers.</div>"
            "</div>"
            "<div style='padding:0.65rem 0.85rem; background:#FFF; border-radius:10px; border-left:4px solid #EF4444;'>"
            "<div style='font-weight:700; color:#EF4444; font-size:0.88rem;'>🔴 High Risk (60–100 / ≥60%)</div>"
            "<div style='font-size:0.8rem; color:#475569;'>24-hour priority outreach, dedicated retention packages, fee waiver audits.</div>"
            "</div>"
            "</div>"
            "</div>"
        )
        render_raw_html(card2_html)
