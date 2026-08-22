# =============================================================================
# CHART FACTORY
# =============================================================================

"""
Reusable Plotly Chart Factory

This module contains reusable functions to create
professional Plotly charts for the dashboard.
"""

import plotly.express as px

from utils.chart_style import apply_dashboard_style


# =============================================================================
# BAR CHART
# =============================================================================

def create_bar_chart(
    data,
    x,
    y,
    title,
    x_title,
    y_title,
    color=None,
    text=None,
    color_discrete_sequence=None,
    color_discrete_map=None,
    hovertemplate=None,
    orientation="v"
):
    """
    Create a professional Plotly Bar Chart.
    """

    fig = px.bar(

        data_frame=data,

        x=x,

        y=y,

        color=color,

        text=text,

        orientation=orientation,

        color_discrete_sequence=color_discrete_sequence,

        color_discrete_map=color_discrete_map

    )

    fig = apply_dashboard_style(

        fig=fig,

        title=title,

        x_title=x_title,

        y_title=y_title,

        hovertemplate=hovertemplate

    )

    return fig


# =============================================================================
# PIE / DONUT CHART
# =============================================================================

def create_pie_chart(
    data,
    names,
    values,
    title,
    color=None,
    color_discrete_sequence=None,
    hole=0.45
):
    """
    Create a professional Plotly Donut Chart.
    """

    fig = px.pie(

        data_frame=data,

        names=names,

        values=values,

        color=color,

        hole=hole,

        color_discrete_sequence=color_discrete_sequence

    )

    fig.update_traces(

        textinfo="percent+label",

        textposition="inside",

        textfont_size=14,

        hovertemplate=
        "<b>%{label}</b><br>" +
        "Customers: %{value}<br>" +
        "Percentage: %{percent}<extra></extra>"

    )

    fig.update_layout(

        template="plotly_dark",

        title=title,

        title_x=0.5,

        height=500,

        legend=dict(

            orientation="h",

            y=-0.15,

            x=0.5,

            xanchor="center"

        )

    )

    return fig


# =============================================================================
# HISTOGRAM
# =============================================================================

def create_histogram(
    data,
    x,
    title,
    x_title,
    y_title,
    color=None,
    nbins=30,
    hovertemplate=None
):
    """
    Create a professional Plotly Histogram.
    """

    fig = px.histogram(

        data_frame=data,

        x=x,

        color=color,

        nbins=nbins

    )

    fig = apply_dashboard_style(

        fig=fig,

        title=title,

        x_title=x_title,

        y_title=y_title,

        hovertemplate=hovertemplate

    )

    return fig