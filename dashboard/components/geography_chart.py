from utils.chart_style import PLOTLY_CONFIG
# =============================================================================
# GEOGRAPHY DISTRIBUTION CHART
# =============================================================================

import streamlit as st
import plotly.express as px
from utils.chart_factory import create_bar_chart
from utils.constants import PRIMARY_BLUE, SUCCESS_GREEN, WARNING_AMBER


def display_geography_chart(df, key: str = None):
    """
    Display customer distribution across European countries with summary metrics.
    """
    geography_counts = (
        df["Geography"]
        .value_counts()
        .reset_index()
    )
    geography_counts.columns = ["Country", "Customers"]
    total = len(df)

    fig = create_bar_chart(
        data=geography_counts,
        x="Country",
        y="Customers",
        color="Country",
        text="Customers",
        title="Customer Distribution Across Geographies",
        x_title="Country",
        y_title="Number of Customers",
        color_discrete_sequence=[PRIMARY_BLUE, SUCCESS_GREEN, WARNING_AMBER],
        hovertemplate="<b>%{x}</b><br>Customers: <b>%{y:,}</b><extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)

    fr_cnt = int(geography_counts[geography_counts["Country"] == "France"]["Customers"].values[0]) if len(geography_counts[geography_counts["Country"] == "France"]) > 0 else 0
    de_cnt = int(geography_counts[geography_counts["Country"] == "Germany"]["Customers"].values[0]) if len(geography_counts[geography_counts["Country"] == "Germany"]) > 0 else 0
    es_cnt = int(geography_counts[geography_counts["Country"] == "Spain"]["Customers"].values[0]) if len(geography_counts[geography_counts["Country"] == "Spain"]) > 0 else 0

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns: repeat(3, 1fr); gap:0.45rem; margin-top:0.4rem; margin-bottom:0.85rem;">
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">🇫🇷 France</div>
                <div style="font-size:0.96rem; font-weight:800; color:#0284C7; margin-top:0.1rem;">{fr_cnt:,} <span style="font-size:0.75rem; color:#64748B; font-weight:600;">({fr_cnt/total*100:.1f}%)</span></div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">🇩🇪 Germany</div>
                <div style="font-size:0.96rem; font-weight:800; color:#059669; margin-top:0.1rem;">{de_cnt:,} <span style="font-size:0.75rem; color:#64748B; font-weight:600;">({de_cnt/total*100:.1f}%)</span></div>
            </div>
            <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:10px; padding:0.5rem 0.6rem; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.02);">
                <div style="font-size:0.68rem; color:#64748B; font-weight:700; text-transform:uppercase;">🇪🇸 Spain</div>
                <div style="font-size:0.96rem; font-weight:800; color:#D97706; margin-top:0.1rem;">{es_cnt:,} <span style="font-size:0.75rem; color:#64748B; font-weight:600;">({es_cnt/total*100:.1f}%)</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )