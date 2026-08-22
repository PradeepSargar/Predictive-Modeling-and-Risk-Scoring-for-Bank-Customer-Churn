# =============================================================================
# PROBABILITY DISTRIBUTION VISUALIZATION COMPONENT
# =============================================================================

"""
Displays the cohort-level churn probability distribution with an overlay
marker showing where the scored customer sits relative to the test-set
population. Uses Plotly for interactive, enterprise-grade visuals.
"""

import numpy as np
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
)


def _cohort_probabilities(model, scaler, X_test):
    """Generate churn probabilities for the hold-out cohort on demand using unscaled features for Gradient Boosting."""
    if X_test is None or model is None:
        return None
    proba = model.predict_proba(X_test)[:, 1]
    return pd.Series(proba, name="Churn Probability")


def display_probability_distribution(
    customer_probability=None,
    model=None,
    scaler=None,
    X_test=None,
    cohort_proba_series=None,
):
    """
    Render the cohort probability distribution chart with optional customer marker.

    Parameters
    ----------
    customer_probability : float or None
        Individual customer's churn probability (0.0 - 1.0) to highlight.
    model : trained classifier
        Gradient boosting model used to score cohort (if cohort not precomputed).
    scaler : StandardScaler
        Scaler used during training.
    X_test : pd.DataFrame
        Hold-out test features for cohort scoring.
    cohort_proba_series : pd.Series, optional
        Precomputed cohort probabilities to bypass recomputation.
    """

    st.markdown(
        """
        <div class="insight-card insight-card-blue" style="margin:0 0 1rem 0;">
            <div class="insight-card-icon">📊</div>
            <div>
                <div class="insight-card-title">Cohort Probability Distribution</div>
                <div class="insight-card-body">
                    Histogram + KDE of predicted churn probabilities across the 2,000-row
                    hold-out cohort scored by Gradient Boosting. The annotated marker shows <b>where this customer ranks</b>
                    relative to the population — critical for prioritising retention resources.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if cohort_proba_series is None and model is not None and X_test is not None:
        cohort_proba_series = _cohort_probabilities(model, scaler, X_test)

    if cohort_proba_series is None:
        st.info(
            "ℹ️ Cohort distribution will appear as soon as a customer is scored "
            "and the hold-out dataset is available."
        )
        return

    proba_df = pd.DataFrame({"Churn Probability": cohort_proba_series.values})

    bins = np.linspace(0, 1, 41)
    counts, edges = np.histogram(proba_df["Churn Probability"], bins=bins)
    bin_centers = (edges[:-1] + edges[1:]) / 2.0

    def _band(c):
        if c < LOW_RISK_THRESHOLD:
            return "Low Risk (<30%)"
        if c < MEDIUM_RISK_THRESHOLD:
            return "Medium Risk (30–59%)"
        return "High Risk (60–100%)"

    hist_df = pd.DataFrame(
        {
            "Bin Center": bin_centers,
            "Customers": counts,
            "Risk Band": [_band(c) for c in bin_centers],
        }
    )

    color_map = {
        "Low Risk (<30%)": SUCCESS_GREEN,
        "Medium Risk (30–59%)": WARNING_AMBER,
        "High Risk (60–100%)": DANGER_RED,
    }

    fig = px.bar(
        hist_df,
        x="Bin Center",
        y="Customers",
        color="Risk Band",
        color_discrete_map=color_map,
        hover_data={
            "Bin Center": ":,.1%",
            "Customers": ":,",
            "Risk Band": True,
        },
    )

    from scipy.stats import gaussian_kde

    kde_x = np.linspace(0, 1, 300)
    kde = gaussian_kde(proba_df["Churn Probability"].values)
    kde_y = kde(kde_x)
    max_count = float(counts.max()) if counts.max() > 0 else 1.0
    kde_scaled = kde_y / kde_y.max() * max_count * 0.9

    fig.add_trace(
        go.Scatter(
            x=kde_x,
            y=kde_scaled,
            mode="lines",
            name="Density (KDE)",
            line=dict(color=PRIMARY_BLUE, width=3, shape="spline"),
            hovertemplate=(
                "<b style='font-size:13px; color:#0F172A;'>Probability: %{x:.1%}</b><br>"
                "<span style='color:#475569; font-size:12px;'>Density: <b style='color:#1E40AF;'>relative</b></span>"
                "<extra></extra>"
            ),
        )
    )

    if customer_probability is not None:
        pct = float(customer_probability)
        fig.add_vline(
            x=pct,
            line_width=0,
        )
        fig.add_trace(
            go.Scatter(
                x=[pct, pct],
                y=[0, max_count * 1.02],
                mode="lines",
                name="This Customer",
                line=dict(color="#0F172A", width=3, dash="dot"),
                hoverinfo="skip",
                showlegend=False,
            )
        )
        fig.add_annotation(
            x=pct,
            y=max_count * 0.98,
            text=f"👤 This Customer<br><b>{pct:.1%}</b>",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.4,
            arrowwidth=2,
            arrowcolor="#0F172A",
            ax=-60,
            ay=-40,
            font=dict(family="Inter, Segoe UI, sans-serif", size=12, color="#FFFFFF"),
            bgcolor=PRIMARY_BLUE,
            bordercolor="#1E3A8A",
            borderwidth=1.5,
            borderpad=6,
            opacity=0.96,
        )

    fig.add_vrect(
        x0=0,
        x1=LOW_RISK_THRESHOLD,
        fillcolor=SUCCESS_GREEN,
        opacity=0.05,
        line_width=0,
        annotation_text="LOW",
        annotation_position="bottom left",
        annotation_font_size=10,
        annotation_font_color=SUCCESS_GREEN,
    )
    fig.add_vrect(
        x0=LOW_RISK_THRESHOLD,
        x1=MEDIUM_RISK_THRESHOLD,
        fillcolor=WARNING_AMBER,
        opacity=0.05,
        line_width=0,
        annotation_text="MEDIUM",
        annotation_position="bottom left",
        annotation_font_size=10,
        annotation_font_color=WARNING_AMBER,
    )
    fig.add_vrect(
        x0=MEDIUM_RISK_THRESHOLD,
        x1=1.0,
        fillcolor=DANGER_RED,
        opacity=0.05,
        line_width=0,
        annotation_text="HIGH",
        annotation_position="bottom left",
        annotation_font_size=10,
        annotation_font_color=DANGER_RED,
    )

    fig = apply_dashboard_style(
        fig,
        title="Cohort Churn Probability Distribution · Hold-Out Set",
        x_title="Predicted Churn Probability",
        y_title="Customers (Count)",
        height=440,
        showlegend=True,
    )

    fig.update_layout(bargap=0.04)
    fig.update_xaxes(range=[-0.02, 1.02], tickformat=".0%", dtick=0.1)

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG)

    _display_distribution_stats(proba_df["Churn Probability"].values, customer_probability)


def _display_distribution_stats(cohort_proba, customer_probability):
    """Render a small KPI-style summary comparing the customer vs the cohort."""

    p25 = float(np.percentile(cohort_proba, 25))
    p50 = float(np.percentile(cohort_proba, 50))
    p75 = float(np.percentile(cohort_proba, 75))
    p90 = float(np.percentile(cohort_proba, 90))
    mean = float(np.mean(cohort_proba))

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card-surface card-gradient-green">
                <div class="card-header">
                    <div class="card-icon card-icon-green">📉</div>
                    <div class="card-title">Cohort Median</div>
                </div>
                <div class="card-value" style="font-size:1.5rem;">{p50:.1%}</div>
                <div class="card-subtitle">50th-percentile churn score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="card-surface card-gradient-blue">
                <div class="card-header">
                    <div class="card-icon card-icon-blue">📊</div>
                    <div class="card-title">Cohort Mean</div>
                </div>
                <div class="card-value" style="font-size:1.5rem;">{mean:.1%}</div>
                <div class="card-subtitle">Average churn probability</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="card-surface card-gradient-amber">
                <div class="card-header">
                    <div class="card-icon card-icon-amber">⚠️</div>
                    <div class="card-title">High-Risk Threshold</div>
                </div>
                <div class="card-value" style="font-size:1.5rem;">{p90:.1%}</div>
                <div class="card-subtitle">Top 10% at-risk cohort</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        if customer_probability is not None:
            rank = float(np.mean(cohort_proba <= customer_probability)) * 100
            delta_color = "red" if rank >= 70 else ("amber" if rank >= 40 else "green")
            delta_icon = "📈" if rank >= 70 else ("➖" if rank >= 40 else "✅")
            st.markdown(
                f"""
                <div class="card-surface card-gradient-{delta_color}">
                    <div class="card-header">
                        <div class="card-icon card-icon-{delta_color}">{delta_icon}</div>
                        <div class="card-title">Customer Percentile</div>
                    </div>
                    <div class="card-value" style="font-size:1.5rem;">{rank:.1f}ᵗʰ</div>
                    <div class="card-subtitle">
                        {100 - rank:.1f}% of the cohort has a <i>lower</i> churn score
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="card-surface card-gradient-purple">
                    <div class="card-header">
                        <div class="card-icon card-icon-purple">🎯</div>
                        <div class="card-title">IQR Spread</div>
                    </div>
                    <div class="card-value" style="font-size:1.3rem;">
                        {p25:.0%} – {p75:.0%}
                    </div>
                    <div class="card-subtitle">Middle 50% of cohort range</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
