# =============================================================================
# FEATURE IMPORTANCE COMPONENT (ENHANCED PLOTLY VERSION)
# =============================================================================

"""
Displays the Feature Importance Ranking of the trained Gradient Boosting model
using Plotly for consistent enterprise styling aligned with the design system.
Supports both global feature importance and per-prediction driver ranking.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.chart_style import PLOTLY_CONFIG, apply_dashboard_style
from utils.constants import (
    PRIMARY_BLUE,
    PRIMARY_BLUE_LIGHT,
    SUCCESS_GREEN,
    WARNING_AMBER,
    DANGER_RED,
    LOW_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
    NEUTRAL_500,
    TEXT_PRIMARY,
)


def _risk_color(probability):
    if probability < LOW_RISK_THRESHOLD:
        return SUCCESS_GREEN
    if probability < MEDIUM_RISK_THRESHOLD:
        return WARNING_AMBER
    return DANGER_RED


def display_feature_importance(
    model,
    feature_names,
    customer_probability=None,
    compact=False,
):
    """
    Render styled Plotly horizontal bar chart of feature importance, matching the
    dashboard's corporate theme.

    Parameters
    ----------
    model : trained model with feature_importances_
        The Gradient Boosting model.
    feature_names : list[str]
        Column / feature names used during training.
    customer_probability : float, optional
        If provided, use as accent color for this prediction context.
    compact : bool
        If True, render a shorter chart for embedding.
    """

    importance_df = pd.DataFrame(
        {
            "Feature": feature_names,
            "Importance": model.feature_importances_,
        }
    )

    importance_df = importance_df.sort_values(by="Importance", ascending=True).reset_index(
        drop=True
    )

    total = importance_df["Importance"].sum() or 1.0
    importance_df["Share"] = importance_df["Importance"] / total * 100

    top_n = min(len(importance_df), 11)
    importance_top = importance_df.tail(top_n).copy()

    accent = _risk_color(customer_probability) if customer_probability is not None else PRIMARY_BLUE

    importance_top["Color"] = importance_top["Importance"].apply(
        lambda v: (
            SUCCESS_GREEN
            if v >= importance_top["Importance"].quantile(0.75)
            else (
                WARNING_AMBER
            if v >= importance_top["Importance"].quantile(0.4)
            else PRIMARY_BLUE_LIGHT
            )
        )
    )

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            y=importance_top["Feature"],
            x=importance_top["Importance"],
            orientation="h",
            marker=dict(
                color=importance_top["Color"],
                line=dict(color="#FFFFFF", width=1),
            ),
            hovertemplate=(
                "<b style='font-size:13px; color:#0F172A;'>%{y}</b><br>"
                "<span style='color:#475569;'>Gini Importance: <b style='color:#1E40AF;'>%{x:.4f}</b><br>"
                "Relative Share: <b style='color:#059669;'>%{customdata[0]:.1f}%</b></span>"
                "<extra></extra>"
            ),
            customdata=importance_top[["Share"]].values,
            text=[f"{s:.1f}%" for s in importance_top["Share"].values],
            textposition="outside",
            insidetextanchor="middle",
        )
    )

    height = 340 if compact else 440

    title_text = (
        "Feature Importance · Top Drivers"
        if customer_probability is None
        else f"Feature Importance · Prediction Drivers ({customer_probability:.1%} churn risk)"
    )

    fig = apply_dashboard_style(
        fig,
        title=title_text,
        x_title="Gini Importance Score",
        y_title="",
        height=height,
        showlegend=False,
    )

    fig.update_layout(
        xaxis=dict(
            title_font=dict(size=12, color=NEUTRAL_500),
            tickfont=dict(size=11, color=NEUTRAL_500),
            showgrid=True,
            gridcolor="#F1F5F9",
            zeroline=True,
            zerolinecolor="#E2E8F0",
            linecolor="#E2E8F0",
        ),
        yaxis=dict(
            tickfont=dict(size=12, color=TEXT_PRIMARY),
            showgrid=False,
            linecolor="#E2E8F0",
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    if not compact:
        st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)
        _display_importance_table(importance_df, customer_probability)


def _display_importance_table(importance_df, customer_probability):
    """Display a ranked, styled table of all features with semantic coloring."""

    importance_df = importance_df.sort_values(by="Importance", ascending=False).reset_index(
        drop=True
    )
    importance_df.index = importance_df.index + 1
    importance_df.index.name = "Rank"
    importance_df = importance_df.reset_index()

    def _tier(v):
        q75 = importance_df["Importance"].quantile(0.75)
        q40 = importance_df["Importance"].quantile(0.4)
        if v >= q75:
            return "Strong Driver"
        if v >= q40:
            return "Moderate Driver"
        return "Secondary Driver"

    importance_df["Influence Tier"] = importance_df["Importance"].apply(_tier)

    def _color_tier(t):
        if t == "Strong Driver":
            return f'<span class="pill pill-red" style="font-size:0.74rem; font-weight:700;">🔴 {t}</span>'
        if t == "Moderate Driver":
            return f'<span class="pill pill-amber" style="font-size:0.74rem; font-weight:700;">🟠 {t}</span>'
        return f'<span class="pill pill-green" style="font-size:0.74rem; font-weight:700;">🟢 {t}</span>'

    display_df = pd.DataFrame(
        {
            "Rank": importance_df["Rank"].astype(int),
            "Feature": importance_df["Feature"],
            "Importance": importance_df["Importance"].round(4),
            "Share": importance_df["Share"].round(1).astype(str) + "%",
            "Influence Tier": importance_df["Influence Tier"].apply(_color_tier),
        }
    )

    st.markdown(
        f"""
        <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:16px; padding:0.25rem 1rem 1rem 1rem; box-shadow:0 1px 3px rgba(15,23,42,0.04);">
            <div style="padding:0.9rem 0.5rem 0.5rem 0.5rem; display:flex; align-items:center; justify-content:space-between; gap:0.5rem; flex-wrap:wrap;">
                <div>
                <div style="font-weight:700; color:#0F172A; font-size:0.98rem;">Full Feature Ranking Table</div>
                <div style="font-size:0.8rem; color:#64748B;">
                    All {len(display_df)} model inputs, ranked by Gini importance.  ={'&nbsp;' if False else ''}
                    {f'<span class="pill pill-blue" style="margin-left:0.4rem; font-size:0.72rem;">Gradient Boosting Classifier</span>'}
                </div>
                </div>
                {
                    f'<span class="pill pill-green" style="font-size:0.74rem; font-weight:700;">📋 {len(display_df)} Features</span>'
                }
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Rank": st.column_config.NumberColumn(
                "Rank", format="%d", width="small"
            ),
            "Importance": st.column_config.NumberColumn(
                "Gini Importance", format="%.4f"
            ),
            "Influence Tier": st.column_config.TextColumn(
                "Influence Tier"
            ),
        },
    )
