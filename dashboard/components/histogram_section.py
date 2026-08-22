from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# HISTOGRAM SECTION COMPONENT
# =============================================================================

import streamlit as st

from services.analytics_service import AnalyticsService

from utils.chart_factory import create_histogram

from components.kpi_card import display_kpi_card


def display_histogram_section(

    df,

    column,

    title,

    x_title,

    y_title,

    formatter,

    metrics,

    icon_map,

    nbins=30

):

    # ============================================================
    # Histogram
    # ============================================================

    fig = create_histogram(

        data=df,

        x=column,

        title=title,

        x_title=x_title,

        y_title=y_title,

        nbins=nbins,

        hovertemplate=
        f"<b>{column}</b>: %{{x}}<br>"
        "Customers: %{y}<extra></extra>"

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config=PLOTLY_CONFIG,
    )

    # ============================================================
    # Statistics
    # ============================================================

    stats = AnalyticsService.numeric_summary(

        df,

        column

    )

    # ============================================================
    # KPI Cards
    # ============================================================

    cols = st.columns(len(metrics))

    for col, metric in zip(cols, metrics):

        with col:

            display_kpi_card(

                title=metric["title"],

                value=formatter(

                    stats[metric["key"]]

                ),

                icon=icon_map.get(

                    metric["key"],

                    "📊"

                ),

                help_text=metric["help"]

            )