# =============================================================================
# CORRELATION HEATMAP COMPONENT
# =============================================================================

import streamlit as st
import plotly.express as px
from utils.chart_style import PLOTLY_CONFIG, apply_heatmap_style


def display_correlation_heatmap(df, key: str = None):
    """
    Display styled correlation heatmap of numerical features.
    """
    numeric_df = df.select_dtypes(include="number")
    correlation_matrix = numeric_df.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        title="Feature Correlation Matrix",
    )

    fig = apply_heatmap_style(
        fig=fig,
        title="Feature Correlation Matrix (Pearson Correlation)",
        height=540,
        zmin=-1.0,
        zmax=1.0,
    )

    st.plotly_chart(fig, use_container_width=True, config=PLOTLY_CONFIG, key=key)