import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from components.theme import apply_global_theme
from components.sidebar import display_sidebar
from components.section_header import display_section_header
from components.kpi_card import render_kpi_row

from utils.constants import (
    PRIMARY_SKY,
    PRIMARY_SKY_DARK,
    SECONDARY_PURPLE,
    SUCCESS_GREEN,
    WARNING_AMBER,
    DANGER_RED,
    CHART_COLOR_PALETTE,
)
from utils.chart_style import apply_dashboard_style, PLOTLY_CONFIG


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
    page_title="Model Performance | Bank Churn Intelligence",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_global_theme()
display_sidebar()

# =============================================================================
# SINGLE CENTRALIZED SOURCE OF TRUTH: 5-FOLD STRATIFIED CV BENCHMARKS
# =============================================================================
cv_results = {
    "Gradient Boosting": {
        "family": "Ensemble (Boosting)",
        "accuracy": 86.31,
        "accuracy_std": 0.99,
        "precision": 77.22,
        "precision_std": 3.17,
        "recall": 46.44,
        "recall_std": 3.56,
        "f1": 57.98,
        "f1_std": 3.65,
        "roc_auc": 86.48,
        "roc_auc_std": 0.99,
        "status": "CHAMPION 🏆",
        "badge_color": "#10B981",
        "badge_bg": "#DCFCE7",
        "border_color": "#86EFAC",
        "rank": 1,
    },
    "XGBoost": {
        "family": "Ensemble (Boosting)",
        "accuracy": 86.08,
        "accuracy_std": 0.79,
        "precision": 75.55,
        "precision_std": 2.71,
        "recall": 46.75,
        "recall_std": 2.55,
        "f1": 57.75,
        "f1_std": 2.71,
        "roc_auc": 86.47,
        "roc_auc_std": 0.95,
        "status": "BENCHMARK",
        "badge_color": "#0EA5E9",
        "badge_bg": "#E0F2FE",
        "border_color": "#BAE6FD",
        "rank": 2,
    },
    "Random Forest": {
        "family": "Ensemble (Bagging)",
        "accuracy": 85.82,
        "accuracy_std": 0.84,
        "precision": 74.60,
        "precision_std": 2.81,
        "recall": 46.07,
        "recall_std": 2.75,
        "f1": 56.96,
        "f1_std": 2.90,
        "roc_auc": 85.02,
        "roc_auc_std": 1.25,
        "status": "BENCHMARK",
        "badge_color": "#0284C7",
        "badge_bg": "#E0F2FE",
        "border_color": "#BAE6FD",
        "rank": 3,
    },
    "Logistic Regression": {
        "family": "Linear Model",
        "accuracy": 81.05,
        "accuracy_std": 0.67,
        "precision": 59.67,
        "precision_std": 4.43,
        "recall": 21.41,
        "recall_std": 2.58,
        "f1": 31.48,
        "f1_std": 3.27,
        "roc_auc": 76.28,
        "roc_auc_std": 1.99,
        "status": "BASELINE",
        "badge_color": "#64748B",
        "badge_bg": "#F1F5F9",
        "border_color": "#CBD5E1",
        "rank": 4,
    },
    "Decision Tree": {
        "family": "Single Tree",
        "accuracy": 78.69,
        "accuracy_std": 0.63,
        "precision": 47.81,
        "precision_std": 1.44,
        "recall": 50.18,
        "recall_std": 3.64,
        "f1": 48.91,
        "f1_std": 2.15,
        "roc_auc": 68.08,
        "roc_auc_std": 1.50,
        "status": "EXPLORATORY",
        "badge_color": "#64748B",
        "badge_bg": "#F1F5F9",
        "border_color": "#CBD5E1",
        "rank": 5,
    },
}

# -----------------------------------------------------------------------------
# Compact Hero Header & Champion Model Badges
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# Compact Hero Header & Champion Model Badges
# -----------------------------------------------------------------------------
gb_cv = cv_results["Gradient Boosting"]
compact_header_html = (
    "<div class='hero-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:0.5rem;'>"
    "<div style='display:flex; align-items:center; gap:0.75rem;'>"
    "<div style='width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.2rem; font-weight:700;'>🏆</div>"
    "<div>"
    "<h1 style='margin:0; font-size:1.25rem; font-weight:800; color:#0F172A; line-height:1.2;'>Model Performance &amp; Evaluation Suite</h1>"
    "<div style='font-size:0.82rem; color:#64748B; margin-top:2px;'>Statistical validation via 5-Fold Stratified Cross-Validation on 8,000 training records, evaluated on 2,000 holdout test samples.</div>"
    "</div>"
    "</div>"
    "<div style='display:flex; align-items:center; gap:0.4rem; flex-wrap:wrap;'>"
    f"<span class='pill pill-green' style='font-size:0.74rem;'>🏆 Gradient Boosting</span>"
    f"<span class='pill pill-blue' style='font-size:0.74rem;'>🎯 {gb_cv['accuracy']:.2f}% ± {gb_cv['accuracy_std']:.2f}% CV Acc</span>"
    f"<span class='pill pill-purple' style='font-size:0.74rem;'>📈 {gb_cv['roc_auc']:.2f}% ± {gb_cv['roc_auc_std']:.2f}% CV AUC</span>"
    "<span class='pill pill-amber' style='font-size:0.74rem;'>🔬 5-Fold Stratified CV</span>"
    "</div>"
    "</div>"
    "</div>"
)
render_raw_html(compact_header_html)

# -----------------------------------------------------------------------------
# Methodology Information Banner Card
# -----------------------------------------------------------------------------
methodology_card_html = (
    "<div class='info-banner-card' style='display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:0.5rem;'>"
    "<div style='display:flex; align-items:center; gap:0.65rem;'>"
    "<span style='font-size:1.2rem;'>📐</span>"
    "<div>"
    "<span style='font-size:0.78rem; font-weight:800; color:#0F172A; text-transform:uppercase; letter-spacing:0.04em;'>Validation Methodology: </span>"
    "<span style='font-size:0.82rem; color:#475569;'>Model performance is reported using <b>5-Fold Stratified Cross-Validation</b> on the 8,000-record training set (reported as <b>Mean ± Standard Deviation</b>). The 2,000-record holdout test set remains isolated for final unbiased evaluation.</span>"
    "</div>"
    "</div>"
    "<span class='pill pill-blue'>Zero Data Leakage Protocol</span>"
    "</div>"
)
render_raw_html(methodology_card_html)

# -----------------------------------------------------------------------------
# Compact 6-Metric Horizontal Performance Ribbon (5-Fold CV Means)
# -----------------------------------------------------------------------------
metric_ribbon_html = (
    "<div class='stat-ribbon-container' style='grid-template-columns: repeat(6, 1fr);'>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>CV Accuracy</span><span>🎯</span></div>"
    f"<div style='font-size:1.15rem; font-weight:800; color:#0EA5E9; margin:2px 0;'>{gb_cv['accuracy']:.2f}%</div>"
    f"<div style='font-size:0.7rem; color:#64748B;'>± {gb_cv['accuracy_std']:.2f}% Std Dev</div>"
    "</div>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>CV ROC-AUC</span><span>📈</span></div>"
    f"<div style='font-size:1.15rem; font-weight:800; color:#8B5CF6; margin:2px 0;'>{gb_cv['roc_auc']:.2f}%</div>"
    f"<div style='font-size:0.7rem; color:#64748B;'>± {gb_cv['roc_auc_std']:.2f}% Std Dev</div>"
    "</div>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>CV Precision</span><span>🔍</span></div>"
    f"<div style='font-size:1.15rem; font-weight:800; color:#10B981; margin:2px 0;'>{gb_cv['precision']:.2f}%</div>"
    f"<div style='font-size:0.7rem; color:#64748B;'>± {gb_cv['precision_std']:.2f}% Std Dev</div>"
    "</div>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>CV Recall</span><span>⚡</span></div>"
    f"<div style='font-size:1.15rem; font-weight:800; color:#F59E0B; margin:2px 0;'>{gb_cv['recall']:.2f}%</div>"
    f"<div style='font-size:0.7rem; color:#64748B;'>± {gb_cv['recall_std']:.2f}% Std Dev</div>"
    "</div>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>CV F1 Score</span><span>⚖️</span></div>"
    f"<div style='font-size:1.15rem; font-weight:800; color:#8B5CF6; margin:2px 0;'>{gb_cv['f1']:.2f}%</div>"
    f"<div style='font-size:0.7rem; color:#64748B;'>± {gb_cv['f1_std']:.2f}% Std Dev</div>"
    "</div>"
    "<div class='stat-ribbon-card'>"
    "<div style='display:flex; justify-content:space-between; align-items:center;'><span style='font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;'>Deployment</span><span>🏆</span></div>"
    "<div style='font-size:1.1rem; font-weight:800; color:#10B981; margin:2px 0;'>CHAMPION</div>"
    "<div style='font-size:0.7rem; color:#64748B;'>Tuned GB Model</div>"
    "</div>"
    "</div>"
)
render_raw_html(metric_ribbon_html)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 5-Model Comparative Benchmark Table (5-Fold Stratified Cross-Validation)
# -----------------------------------------------------------------------------
display_section_header(
    "Algorithm Benchmark Comparison (5-Fold Stratified Cross-Validation)",
    "Comprehensive cross-validation results evaluated across 5 stratified folds on the 8,000-record training set.",
    accent_color="#A855F7",
)

table_rows_html = ""
for model_name, m in cv_results.items():
    is_champ = (m["rank"] == 1)
    row_bg = "background:#F0FDF4;" if is_champ else ""
    badge_cls = "pill-green" if is_champ else ("pill-blue" if "XGBoost" in model_name else "pill-amber")
    
    icon_prefix = "🏆 " if is_champ else ("⚡ " if "XGBoost" in model_name else ("🌲 " if "Random" in model_name else ("📈 " if "Logistic" in model_name else "🌿 ")))
    
    table_rows_html += f"""
    <tr style='{row_bg}'>
        <td style='font-weight:700; color:#0F172A; white-space:nowrap; padding:0.55rem 0.75rem;'>{icon_prefix}{model_name}</td>
        <td style='color:#475569; font-size:0.8rem; padding:0.55rem 0.65rem; white-space:nowrap;'>{m['family']}</td>
        <td style='text-align:center; padding:0.55rem 0.45rem;'><span class='pill pill-green' style='font-size:0.75rem; padding:0.18rem 0.45rem;'>{m['accuracy']:.2f}% <span style='font-size:0.68rem; opacity:0.75;'>±{m['accuracy_std']:.2f}%</span></span></td>
        <td style='text-align:center; padding:0.55rem 0.45rem;'><span class='pill pill-green' style='font-size:0.75rem; padding:0.18rem 0.45rem;'>{m['precision']:.2f}% <span style='font-size:0.68rem; opacity:0.75;'>±{m['precision_std']:.2f}%</span></span></td>
        <td style='text-align:center; padding:0.55rem 0.45rem;'><span class='pill pill-amber' style='font-size:0.75rem; padding:0.18rem 0.45rem;'>{m['recall']:.2f}% <span style='font-size:0.68rem; opacity:0.75;'>±{m['recall_std']:.2f}%</span></span></td>
        <td style='text-align:center; padding:0.55rem 0.45rem;'><span class='pill pill-green' style='font-size:0.75rem; padding:0.18rem 0.45rem;'>{m['f1']:.2f}% <span style='font-size:0.68rem; opacity:0.75;'>±{m['f1_std']:.2f}%</span></span></td>
        <td style='text-align:center; padding:0.55rem 0.45rem;'><span class='pill pill-green' style='font-size:0.75rem; padding:0.18rem 0.45rem;'>{m['roc_auc']:.2f}% <span style='font-size:0.68rem; opacity:0.75;'>±{m['roc_auc_std']:.2f}%</span></span></td>
        <td style='text-align:center; padding:0.55rem 0.65rem;'><span class='pill {badge_cls}' style='font-size:0.72rem; padding:0.18rem 0.5rem;'>{m['status']}</span></td>
    </tr>
    """

cv_table_html = f"""
<div class='enterprise-table-container'>
<table class='enterprise-table' style='width:100%; table-layout:auto;'>
<thead>
<tr>
<th style='padding:0.65rem 0.75rem;'>Algorithm</th>
<th style='padding:0.65rem 0.65rem;'>Model Family</th>
<th style='text-align:center; padding:0.65rem 0.45rem;'>Accuracy</th>
<th style='text-align:center; padding:0.65rem 0.45rem;'>Precision</th>
<th style='text-align:center; padding:0.65rem 0.45rem;'>Recall</th>
<th style='text-align:center; padding:0.65rem 0.45rem;'>F1-Score</th>
<th style='text-align:center; padding:0.65rem 0.45rem;'>ROC-AUC</th>
<th style='text-align:center; padding:0.65rem 0.65rem;'>Deployment Status</th>
</tr>
</thead>
<tbody>
{table_rows_html}
</tbody>
</table>
</div>
"""
render_raw_html(cv_table_html)

# -----------------------------------------------------------------------------
# Model Comparison Visual Charts (Driven from cv_results)
# -----------------------------------------------------------------------------
display_section_header(
    "Visual Performance Benchmarks (5-Fold CV Means)",
    "Direct statistical comparison across Accuracy, ROC-AUC, F1-Score, and Precision.",
    accent_color="#0EA5E9",
)

col_c1, col_c2 = st.columns(2, gap="medium")

models_list = list(cv_results.keys())
roc_auc_vals = [cv_results[m]["roc_auc"] for m in models_list]
roc_auc_errs = [cv_results[m]["roc_auc_std"] for m in models_list]
accuracy_vals = [cv_results[m]["accuracy"] for m in models_list]
accuracy_errs = [cv_results[m]["accuracy_std"] for m in models_list]
prec_vals = [cv_results[m]["precision"] for m in models_list]
prec_errs = [cv_results[m]["precision_std"] for m in models_list]
f1_vals = [cv_results[m]["f1"] for m in models_list]
f1_errs = [cv_results[m]["f1_std"] for m in models_list]

with col_c1:
    fig_bar = go.Figure()
    fig_bar.add_trace(
        go.Bar(
            name="CV ROC-AUC (%)",
            x=models_list,
            y=roc_auc_vals,
            error_y=dict(type='data', array=roc_auc_errs, visible=True, thickness=1.5, color='#334155'),
            marker_color=PRIMARY_SKY,
            text=[f"{v:.1f}%" for v in roc_auc_vals],
            textposition="auto",
        )
    )
    fig_bar.add_trace(
        go.Bar(
            name="CV Accuracy (%)",
            x=models_list,
            y=accuracy_vals,
            error_y=dict(type='data', array=accuracy_errs, visible=True, thickness=1.5, color='#334155'),
            marker_color=SECONDARY_PURPLE,
            text=[f"{v:.1f}%" for v in accuracy_vals],
            textposition="auto",
        )
    )
    fig_bar.update_layout(barmode="group")
    fig_bar = apply_dashboard_style(
        fig_bar,
        title="5-Fold CV Accuracy & ROC-AUC (Mean ± Std)",
        x_title="Candidate Algorithm",
        y_title="Metric Value (%)",
        height=360,
        showlegend=True,
    )
    st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CONFIG, key="chart_acc_roc")

with col_c2:
    fig_prec = go.Figure()
    fig_prec.add_trace(
        go.Bar(
            name="CV Precision (%)",
            x=models_list,
            y=prec_vals,
            error_y=dict(type='data', array=prec_errs, visible=True, thickness=1.5, color='#334155'),
            marker_color=SUCCESS_GREEN,
            text=[f"{v:.1f}%" for v in prec_vals],
            textposition="auto",
        )
    )
    fig_prec.add_trace(
        go.Bar(
            name="CV F1-Score (%)",
            x=models_list,
            y=f1_vals,
            error_y=dict(type='data', array=f1_errs, visible=True, thickness=1.5, color='#334155'),
            marker_color=WARNING_AMBER,
            text=[f"{v:.1f}%" for v in f1_vals],
            textposition="auto",
        )
    )
    fig_prec.update_layout(barmode="group")
    fig_prec = apply_dashboard_style(
        fig_prec,
        title="5-Fold CV Precision & F1-Score Trade-off",
        x_title="Candidate Algorithm",
        y_title="Metric Value (%)",
        height=360,
        showlegend=True,
    )
    st.plotly_chart(fig_prec, use_container_width=True, config=PLOTLY_CONFIG, key="chart_prec_f1")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Final Holdout Test Evaluation Section (2,000 Untouched Records)
# -----------------------------------------------------------------------------
display_section_header(
    "Final Holdout Test Evaluation (2,000 Untouched Records)",
    "Unbiased evaluation of the production Gradient Boosting champion model on the isolated holdout test cohort.",
    accent_color="#10B981",
)

tab_holdout_50, tab_holdout_35 = st.tabs([
    "🎯 Default Threshold (T = 0.50) — High Precision",
    "⭐ Selected Retention Policy (T = 0.35) — Max Churn Capture"
])

with tab_holdout_50:
    t50_kpis = [
        {"title": "Holdout Accuracy", "value": "87.00%", "icon": "🎯", "variant": "green", "subtitle": "1,740 / 2,000 correct"},
        {"title": "Holdout ROC-AUC", "value": "87.08%", "icon": "📈", "variant": "purple", "subtitle": "High discrimination"},
        {"title": "Holdout Precision", "value": "79.28%", "icon": "🔍", "variant": "blue", "subtitle": "199 TP / 251 flagged"},
        {"title": "Holdout Recall", "value": "48.89%", "icon": "⚡", "variant": "amber", "subtitle": "199 / 407 churners caught"},
    ]
    render_kpi_row(t50_kpis, cols=4)
    
    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)
    
    col_m1, col_m2 = st.columns(2, gap="medium")
    with col_m1:
        cm_text_50 = [
            ["<b>1,541</b><br><span style='font-size:11px; color:#065F46;'>True Retained (96.7%)</span>",
             "<b>52</b><br><span style='font-size:11px; color:#92400E;'>False Alarm (3.3%)</span>"],
            ["<b>208</b><br><span style='font-size:11px; color:#991B1B;'>Missed Churn (51.1%)</span>",
             "<b>199</b><br><span style='font-size:11px; color:#065F46;'>Captured Churn (48.9%)</span>"]
        ]
        fig_cm_50 = go.Figure(
            data=go.Heatmap(
                z=[[10, 2], [3, 8]],
                x=["Predicted: Retained (0)", "Predicted: Churn (1)"],
                y=["Actual: Retained (0)", "Actual: Churned (1)"],
                text=cm_text_50,
                texttemplate="%{text}",
                textfont={"size": 13, "family": "Inter, Segoe UI, sans-serif"},
                colorscale=[[0.0, "#FEF2F2"], [0.25, "#FEF3C7"], [0.75, "#BAE6FD"], [1.0, "#DCFCE7"]],
                showscale=False,
                hovertemplate="<b>%{y}</b><br><b>%{x}</b><extra></extra>",
            )
        )
        fig_cm_50 = apply_dashboard_style(
            fig_cm_50,
            title="Confusion Matrix @ Threshold 0.50 (2,000 Holdout Set)",
            x_title="",
            y_title="",
            height=340,
        )
        st.plotly_chart(fig_cm_50, use_container_width=True, config=PLOTLY_CONFIG, key="chart_cm_50")

    with col_m2:
        card_html_50 = (
            "<div style='background:linear-gradient(135deg, #F0FDF4 0%, #FFFFFF 100%); border:1px solid #86EFAC; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 4px 18px -2px rgba(16,185,129,0.08); height:100%; display:flex; flex-direction:column; justify-content:space-between;'>"
            "<div>"
            "<div style='display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem; border-bottom:1px solid #DCFCE7; padding-bottom:0.6rem;'>"
            "<div style='width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #10B981 0%, #059669 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700; box-shadow:0 3px 10px rgba(16,185,129,0.25);'>🛡️</div>"
            "<div>"
            "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#059669;'>Default Baseline (T = 0.50)</div>"
            "<h3 style='margin:0; font-size:1.05rem; font-weight:800; color:#0F172A;'>High-Precision Operations</h3>"
            "</div>"
            "</div>"
            "<div style='display:flex; flex-direction:column; gap:0.65rem; font-size:0.85rem; color:#334155; line-height:1.55;'>"
            "<div style='background:#FFFFFF; border:1px solid #DCFCE7; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "🛡️ <b>Ultra-Low False Alarms (3.3%)</b>: Only 52 false alarms generated across 1,593 non-churners, minimizing wasted operational touches."
            "</div>"
            "<div style='background:#FFFFFF; border:1px solid #DCFCE7; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "🎯 <b>High-Conviction Precision (79.28%)</b>: Nearly 4 out of 5 flagged customers churn, maximizing account manager intervention credibility."
            "</div>"
            "<div style='background:#FFFFFF; border:1px solid #DCFCE7; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "⚠️ <b>Recall Tradeoff (48.89%)</b>: Leaves 208 churners unflagged; recoverable by applying the 0.35 proactive campaign threshold."
            "</div>"
            "</div>"
            "</div>"
            "<div style='margin-top:0.85rem; padding:0.75rem 1rem; background:linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%); border:1px solid #86EFAC; border-radius:10px; display:flex; justify-content:space-between; align-items:center;'>"
            "<span style='font-size:0.82rem; font-weight:700; color:#065F46;'>Overall Holdout Accuracy</span>"
            "<span style='font-size:1.15rem; font-weight:800; color:#15803D;'>87.00% (1,740 / 2,000)</span>"
            "</div>"
            "</div>"
        )
        render_raw_html(card_html_50)

with tab_holdout_35:
    t35_kpis = [
        {"title": "Campaign Recall", "value": "59.95%", "icon": "⚡", "variant": "green", "subtitle": "+22.6% relative recall boost"},
        {"title": "Captured Churners", "value": "244 / 407", "icon": "🎯", "variant": "blue", "subtitle": "+45 additional churners caught"},
        {"title": "Campaign Precision", "value": "66.67%", "icon": "🔍", "variant": "purple", "subtitle": "244 TP / 366 flagged"},
        {"title": "Campaign F1-Score", "value": "63.13%", "icon": "⚖️", "variant": "amber", "subtitle": "Optimal campaign balance"},
    ]
    render_kpi_row(t35_kpis, cols=4)
    
    st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)
    
    col_n1, col_n2 = st.columns(2, gap="medium")
    with col_n1:
        cm_text_35 = [
            ["<b>1,471</b><br><span style='font-size:11px; color:#065F46;'>True Retained (92.3%)</span>",
             "<b>122</b><br><span style='font-size:11px; color:#92400E;'>False Alarm (7.7%)</span>"],
            ["<b>163</b><br><span style='font-size:11px; color:#991B1B;'>Missed Churn (40.0%)</span>",
             "<b>244</b><br><span style='font-size:11px; color:#065F46;'>Captured Churn (60.0%)</span>"]
        ]
        fig_cm_35 = go.Figure(
            data=go.Heatmap(
                z=[[10, 2], [3, 8]],
                x=["Predicted: Retained (0)", "Predicted: Churn (1)"],
                y=["Actual: Retained (0)", "Actual: Churned (1)"],
                text=cm_text_35,
                texttemplate="%{text}",
                textfont={"size": 13, "family": "Inter, Segoe UI, sans-serif"},
                colorscale=[[0.0, "#FEF2F2"], [0.25, "#FEF3C7"], [0.75, "#BAE6FD"], [1.0, "#DCFCE7"]],
                showscale=False,
                hovertemplate="<b>%{y}</b><br><b>%{x}</b><extra></extra>",
            )
        )
        fig_cm_35 = apply_dashboard_style(
            fig_cm_35,
            title="Confusion Matrix @ Retention Threshold 0.35 (2,000 Holdout Set)",
            x_title="",
            y_title="",
            height=340,
        )
        st.plotly_chart(fig_cm_35, use_container_width=True, config=PLOTLY_CONFIG, key="chart_cm_35")

    with col_n2:
        card_html_35 = (
            "<div style='background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.08); height:100%; display:flex; flex-direction:column; justify-content:space-between;'>"
            "<div>"
            "<div style='display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem; border-bottom:1px solid #E0F2FE; padding-bottom:0.6rem;'>"
            "<div style='width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700; box-shadow:0 3px 10px rgba(14,165,233,0.25);'>⭐</div>"
            "<div>"
            "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#0284C7;'>Selected Retention Policy (T = 0.35)</div>"
            "<h3 style='margin:0; font-size:1.05rem; font-weight:800; color:#0F172A;'>Proactive Outreach Impact</h3>"
            "</div>"
            "</div>"
            "<div style='display:flex; flex-direction:column; gap:0.65rem; font-size:0.85rem; color:#334155; line-height:1.55;'>"
            "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "🎯 <b>+45 Additional Churners Saved</b>: Recovers 244 of 407 churners (60.0% capture rate), significantly reducing missed churn exposure."
            "</div>"
            "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "🔍 <b>Robust Campaign Precision (66.67%)</b>: Two-thirds of all 366 outreach touches are genuine flight risks, keeping outreach cost effective."
            "</div>"
            "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
            "💰 <b>Illustrative Scenario Simulation</b>: In an illustrative scenario ($2.5K CLV, 25% save rate, $50 contact cost), protects an estimated <b>+$22,375 net added value</b>."
            "</div>"
            "</div>"
            "</div>"
            "<div style='margin-top:0.85rem; padding:0.75rem 1rem; background:linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%); border:1px solid #7DD3FC; border-radius:10px; display:flex; justify-content:space-between; align-items:center;'>"
            "<span style='font-size:0.82rem; font-weight:700; color:#0369A1;'>Selected Policy Accuracy</span>"
            "<span style='font-size:1.15rem; font-weight:800; color:#0284C7;'>85.75% (1,715 / 2,000)</span>"
            "</div>"
            "</div>"
        )
        render_raw_html(card_html_35)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Decision Boundary Curve & Policy Tuning Playbook (OOF 5-Fold Evaluation)
# -----------------------------------------------------------------------------
display_section_header(
    "Decision Boundary & Threshold Policy Playbook (via 5-Fold OOF Predictions)",
    "Classification probability threshold sensitivity analysis calibrated strictly on 8,000 Out-Of-Fold (OOF) training predictions.",
    accent_color="#F59E0B",
)

col_d1, col_d2 = st.columns(2, gap="medium")

with col_d1:
    oof_thresholds = [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.70, 0.80, 0.90]
    oof_prec = [34.91, 43.78, 50.80, 56.66, 62.01, 66.23, 69.99, 74.59, 77.32, 80.18, 83.48, 86.69, 92.92, 94.47]
    oof_rec = [89.26, 82.33, 74.11, 68.90, 63.50, 58.96, 54.66, 50.61, 46.44, 42.94, 39.69, 31.96, 25.77, 14.66]
    oof_f1 = [50.19, 57.17, 60.28, 62.18, 62.75, 62.38, 61.38, 60.31, 58.03, 55.93, 53.80, 46.71, 40.35, 25.39]

    fig_thresh = go.Figure()

    fig_thresh.add_trace(
        go.Scatter(
            x=oof_thresholds,
            y=oof_prec,
            mode="lines+markers",
            name="OOF Precision (%)",
            line=dict(color=PRIMARY_SKY, width=2.5),
            marker=dict(size=5),
            hovertemplate="Threshold: <b>%{x:.2f}</b><br>OOF Precision: <b>%{y:.1f}%</b><extra></extra>",
        )
    )

    fig_thresh.add_trace(
        go.Scatter(
            x=oof_thresholds,
            y=oof_rec,
            mode="lines+markers",
            name="OOF Recall (%)",
            line=dict(color=DANGER_RED, width=2.5),
            marker=dict(size=5),
            hovertemplate="Threshold: <b>%{x:.2f}</b><br>OOF Recall: <b>%{y:.1f}%</b><extra></extra>",
        )
    )

    fig_thresh.add_trace(
        go.Scatter(
            x=oof_thresholds,
            y=oof_f1,
            mode="lines+markers",
            name="OOF F1-Score (%)",
            line=dict(color=WARNING_AMBER, width=2.5, dash="dot"),
            marker=dict(size=4),
            hovertemplate="Threshold: <b>%{x:.2f}</b><br>OOF F1-Score: <b>%{y:.1f}%</b><extra></extra>",
        )
    )

    fig_thresh.add_vline(
        x=0.50,
        line_width=1.5,
        line_dash="dash",
        line_color="#64748B",
        annotation_text="Default (0.50)",
        annotation_position="top left",
        annotation_font_size=10,
    )

    fig_thresh.add_vline(
        x=0.35,
        line_width=2,
        line_dash="solid",
        line_color=SUCCESS_GREEN,
        annotation_text="Selected Policy (0.35)",
        annotation_position="top right",
        annotation_font_size=10,
        annotation_font_color=SUCCESS_GREEN,
    )

    fig_thresh = apply_dashboard_style(
        fig_thresh,
        title="Threshold Optimization on 5-Fold OOF Predictions",
        x_title="Probability Decision Threshold",
        y_title="Metric Score (%)",
        height=360,
        showlegend=True,
    )
    st.plotly_chart(fig_thresh, use_container_width=True, config=PLOTLY_CONFIG, key="chart_threshold_curve")

with col_d2:
    thresh_card_html = (
        "<div style='background:linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%); border:1px solid #BAE6FD; border-radius:14px; padding:1.25rem 1.4rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.08); height:100%; display:flex; flex-direction:column; justify-content:space-between;'>"
        "<div>"
        "<div style='display:flex; align-items:center; gap:0.75rem; margin-bottom:0.75rem; border-bottom:1px solid #E0F2FE; padding-bottom:0.6rem;'>"
        "<div style='width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.15rem; font-weight:700; box-shadow:0 3px 10px rgba(14,165,233,0.25);'>⚖️</div>"
        "<div>"
        "<div style='font-size:0.72rem; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#0284C7;'>OOF Threshold Calibration</div>"
        "<h3 style='margin:0; font-size:1.05rem; font-weight:800; color:#0F172A;'>Operating Policy Playbook</h3>"
        "</div>"
        "</div>"
        "<div style='display:flex; flex-direction:column; gap:0.65rem; font-size:0.85rem; color:#334155; line-height:1.55;'>"
        "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
        "🎯 <b>Default Threshold (0.50) — High Precision</b>: Prioritizes accuracy and avoids false alarms (77.32% OOF precision). Best suited for high-cost retention interventions (fee waivers, executive relationship calls)."
        "</div>"
        "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
        "⭐ <b>Selected Policy (0.35) — Optimal Retention</b>: Selected as the operational retention threshold based on the OOF precision-recall trade-off and campaign capacity considerations (near-peak OOF F1 of 62.38%, stronger precision 66.23% than 0.30, and improved recall 58.96% vs 46.44% at 0.50)."
        "</div>"
        "<div style='background:#FFFFFF; border:1px solid #BAE6FD; border-radius:10px; padding:0.65rem 0.85rem;'>"
        "⚡ <b>Early Warning Policy (0.20) — High Sensitivity</b>: Captures 74.11% of training churners; ideal for zero-marginal-cost digital channels (in-app feature guides, automated educational emails)."
        "</div>"
        "</div>"
        "</div>"
        "<div style='margin-top:0.85rem; padding:0.75rem 1rem; background:linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%); border:1px solid #7DD3FC; border-radius:10px; display:flex; justify-content:space-between; align-items:center;'>"
        "<span style='font-size:0.82rem; font-weight:700; color:#0369A1;'>Calibrated via 5-Fold OOF CV</span>"
        "<span style='font-size:1.05rem; font-weight:800; color:#0284C7;'>Selected Threshold = 0.35</span>"
        "</div>"
        "</div>"
    )
    render_raw_html(thresh_card_html)
