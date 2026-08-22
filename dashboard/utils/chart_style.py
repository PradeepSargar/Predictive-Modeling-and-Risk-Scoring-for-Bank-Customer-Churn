# =============================================================================
# ENTERPRISE CHART STYLING UTILITIES
# =============================================================================

"""
Standardized Plotly styling adhering to the Enterprise Design System:
Sky Blue primary (#0EA5E9), clean white background, minimal gridlines,
Inter typography, clean non-overlapping top-right modebar controls (Auto Scale, Zoom, Pan, Reset, Download).
"""

from utils.constants import (
    PLOTLY_TEMPLATE,
    CHART_HEIGHT,
    FONT_FAMILY,
    FONT_SIZE,
    PRIMARY_SKY,
    PRIMARY_DARK,
    SECONDARY_PURPLE,
    SUCCESS_GREEN,
    WARNING_AMBER,
    DANGER_RED,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_MUTED,
    BORDER_DEFAULT,
    CHART_COLOR_PALETTE,
)

CHART_COLOR_SEQUENCE = CHART_COLOR_PALETTE

CHART_DIVERGING_PALETTE = [
    DANGER_RED,
    "#F97316",
    WARNING_AMBER,
    "#84CC16",
    SUCCESS_GREEN,
    "#0EA5E9",
]

CHURN_PAIR_COLORS = [
    PRIMARY_SKY,
    DANGER_RED,
]

# Clean, streamlined 5-button modebar with responsive autoscale
PLOTLY_CONFIG = {
    "displayModeBar": True,
    "displaylogo": False,
    "responsive": True,
    "scrollZoom": False,
    "doubleClick": "reset+autosize",
    "modeBarButtons": [
        [
            "zoom2d",
            "pan2d",
            "autoScale2d",
            "resetScale2d",
            "toImage",
        ]
    ],
    "toImageButtonOptions": {
        "format": "png",
        "filename": "bank_churn_chart",
        "height": 650,
        "width": 1100,
        "scale": 2,
    },
}


def apply_dashboard_style(
    fig,
    title,
    x_title,
    y_title,
    height=400,
    showlegend=False,
    hovertemplate=None,
    textposition="auto",
    marker_colors=None,
):
    """
    Apply enterprise minimalist theme with responsive autoscale,
    clear title padding, and anti-collision text margins.
    """
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        autosize=True,
        title=dict(
            text=title,
            font=dict(
                family=FONT_FAMILY,
                size=13.5,
                color=TEXT_PRIMARY,
            ),
            x=0.01,
            xanchor="left",
            y=0.97,
            yanchor="top",
            pad=dict(l=0, r=100, t=0, b=0),
        ),
        xaxis_title=x_title,
        yaxis_title=y_title,
        xaxis=dict(
            title_font=dict(family=FONT_FAMILY, size=11.5, color=TEXT_SECONDARY),
            tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
            gridcolor="#F1F5F9",
            gridwidth=1,
            linecolor=BORDER_DEFAULT,
            linewidth=1,
            showline=False,
            zeroline=False,
            showgrid=True,
            ticks="outside",
            ticklen=4,
            tickcolor=BORDER_DEFAULT,
            autorange=True,
            fixedrange=False,
            automargin=True,
        ),
        yaxis=dict(
            title_font=dict(family=FONT_FAMILY, size=11.5, color=TEXT_SECONDARY),
            tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
            gridcolor="#F1F5F9",
            gridwidth=1,
            linecolor=BORDER_DEFAULT,
            linewidth=1,
            showline=False,
            zeroline=True,
            zerolinecolor="#E2E8F0",
            zerolinewidth=1,
            showgrid=True,
            ticks="outside",
            ticklen=4,
            tickcolor=BORDER_DEFAULT,
            autorange=True,
            fixedrange=False,
            automargin=True,
        ),
        font=dict(family=FONT_FAMILY, size=FONT_SIZE, color=TEXT_SECONDARY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=52, r=20, t=48, b=45 if not showlegend else 72),
        height=height,
        showlegend=showlegend,
        legend=dict(
            font=dict(family=FONT_FAMILY, size=10, color=TEXT_SECONDARY),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=BORDER_DEFAULT,
            borderwidth=1,
            orientation="h",
            yanchor="top",
            y=-0.18,
            xanchor="center",
            x=0.5,
        ),
        hoverlabel=dict(
            bgcolor="#0F172A",
            font_size=11.5,
            font_family=FONT_FAMILY,
            font_color="#FFFFFF",
            bordercolor="#1E293B",
        ),
        modebar=dict(
            orientation="h",
            bgcolor="rgba(255, 255, 255, 0.94)",
            color="#475569",
            activecolor="#0284C7",
        ),
        uniformtext=dict(mode="hide", minsize=8),
        colorway=CHART_COLOR_PALETTE,
    )

    if marker_colors is not None:
        fig.update_traces(marker_color=marker_colors)

    if hovertemplate is not None:
        fig.update_traces(hovertemplate=hovertemplate)

    if textposition:
        try:
            fig.update_traces(textposition=textposition, cliponaxis=False)
        except Exception:
            pass

    return fig


def apply_pie_style(fig, title, height=380, showlegend=True):
    """
    Apply enterprise donut/pie chart styling with non-overlapping modebar and legend.
    """
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        autosize=True,
        title=dict(
            text=title,
            font=dict(family=FONT_FAMILY, size=13.5, color=TEXT_PRIMARY),
            x=0.01,
            xanchor="left",
            y=0.97,
            pad=dict(l=0, r=100, t=0, b=0),
        ),
        font=dict(family=FONT_FAMILY, size=11, color=TEXT_SECONDARY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=48, b=55 if showlegend else 25),
        height=height,
        showlegend=showlegend,
        legend=dict(
            font=dict(family=FONT_FAMILY, size=10, color=TEXT_SECONDARY),
            bgcolor="rgba(255,255,255,0.92)",
            bordercolor=BORDER_DEFAULT,
            borderwidth=1,
            orientation="h",
            yanchor="top",
            y=-0.10,
            xanchor="center",
            x=0.5,
        ),
        modebar=dict(
            orientation="h",
            bgcolor="rgba(255, 255, 255, 0.94)",
            color="#475569",
            activecolor="#0284C7",
        ),
        uniformtext=dict(mode="hide", minsize=9),
        colorway=CHART_COLOR_PALETTE,
    )
    return fig


def apply_heatmap_style(fig, title, height=460, zmin=None, zmax=None):
    """
    Apply enterprise correlation heatmap styling with responsive autoscale and clean top toolbar.
    """
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        autosize=True,
        title=dict(
            text=title,
            font=dict(family=FONT_FAMILY, size=13.5, color=TEXT_PRIMARY),
            x=0.01,
            xanchor="left",
            y=0.97,
            pad=dict(l=0, r=100, t=0, b=0),
        ),
        xaxis=dict(
            autorange=True,
            fixedrange=False,
            automargin=True,
            tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        ),
        yaxis=dict(
            autorange=True,
            fixedrange=False,
            automargin=True,
            tickfont=dict(family=FONT_FAMILY, size=10, color=TEXT_MUTED),
        ),
        font=dict(family=FONT_FAMILY, size=11, color=TEXT_SECONDARY),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=70, r=35, t=48, b=60),
        height=height,
        modebar=dict(
            orientation="h",
            bgcolor="rgba(255, 255, 255, 0.94)",
            color="#475569",
            activecolor="#0284C7",
        ),
    )
    fig.update_coloraxes(
        colorscale=[
            [0.0, DANGER_RED],
            [0.5, "#FFFFFF"],
            [1.0, PRIMARY_SKY],
        ],
        colorbar_title=dict(text="Correlation", font=dict(family=FONT_FAMILY, size=11)),
    )
    return fig
