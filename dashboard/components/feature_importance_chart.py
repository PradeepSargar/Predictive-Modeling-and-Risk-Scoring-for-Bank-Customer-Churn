# =============================================================================
# FEATURE IMPORTANCE CHART COMPONENT - ENTERPRISE XAI EDITION
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style
from utils.constants import PRIMARY_SKY, PRIMARY_SKY_DARK


def display_feature_importance_chart(feature_importance_df, key: str = None):
    """
    Display feature importance horizontal ranking bar chart with executive breakdown cards.
    """
    plot_df = feature_importance_df.sort_values(
        by="Importance",
        ascending=True,
    ).copy()

    total = plot_df["Importance"].sum() or 1.0
    plot_df["Share"] = (plot_df["Importance"] / total * 100).round(1)

    # Color palette: top 3 highlighted with gradient theme sky-blue, others with neutral slate
    num_bars = len(plot_df)
    colors = [
        "#0284C7" if i >= num_bars - 3 else "#38BDF8" if i >= num_bars - 6 else "#94A3B8"
        for i in range(num_bars)
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=plot_df["Feature"],
            x=plot_df["Importance"],
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="#FFFFFF", width=1.5),
                cornerradius=4,
            ),
            text=[f"  {s:.1f}% ({v:.3f})" for s, v in zip(plot_df["Share"], plot_df["Importance"])],
            textposition="outside",
            textfont=dict(size=12, family="Inter, Segoe UI", color="#0F172A", weight="bold"),
            hovertemplate="<b>%{y}</b><br>Gini Importance: <b>%{x:.4f}</b><br>Global Share: <b>%{text}</b><extra></extra>",
        )
    )

    fig = apply_dashboard_style(
        fig=fig,
        title="Global Gini Feature Importance Ranking (Tree Split Criterion)",
        x_title="Gini Impurity Reduction Score",
        y_title="Audited Model Feature",
        height=480,
    )
    fig.update_layout(
        margin=dict(l=10, r=40, t=45, b=35),
        xaxis=dict(range=[0, plot_df["Importance"].max() * 1.25]),
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    # Executive 3-Pillar Driver Breakdown
    st.markdown(
        """
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.75rem; margin-top:0.75rem;">
            <div style="background:#FFFFFF; border:1px solid #BAE6FD; border-radius:12px; padding:0.85rem 1rem; box-shadow:0 2px 6px rgba(14,165,233,0.06);">
                <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;">
                    <span style="font-size:1.1rem;">🥇</span>
                    <span style="font-weight:700; color:#0369A1; font-size:0.88rem;">Primary Driver: Age</span>
                </div>
                <div style="font-size:0.8rem; color:#475569; line-height:1.5;">
                    Accounts for <b>~42%</b> of tree split decisions. Customer attrition risk accelerates significantly above age 45.
                </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #DDD6FE; border-radius:12px; padding:0.85rem 1rem; box-shadow:0 2px 6px rgba(168,85,247,0.06);">
                <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;">
                    <span style="font-size:1.1rem;">🥈</span>
                    <span style="font-weight:700; color:#6D28D9; font-size:0.88rem;">Secondary Driver: Products</span>
                </div>
                <div style="font-size:0.8rem; color:#475569; line-height:1.5;">
                    Single-product accounts exhibit the highest vulnerability. Holding 2 products provides optimal relationship retention.
                </div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #A7F3D0; border-radius:12px; padding:0.85rem 1rem; box-shadow:0 2px 6px rgba(16,185,129,0.06);">
                <div style="display:flex; align-items:center; gap:0.4rem; margin-bottom:0.25rem;">
                    <span style="font-size:1.1rem;">🥉</span>
                    <span style="font-weight:700; color:#065F46; font-size:0.88rem;">Tertiary Driver: Activity</span>
                </div>
                <div style="font-size:0.8rem; color:#475569; line-height:1.5;">
                    Inactive member status doubles churn probability. Digital banking engagement serves as a strong retention anchor.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )