# =============================================================================
# REUSABLE METRICS & KPI COMPONENT
# =============================================================================

"""
Reusable metric cards, stat badges, and KPI grid utilities
for the Bank Churn Intelligence Dashboard.
"""

from typing import List, Dict, Any, Optional
import streamlit as st


def render_metric_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    icon: str = "📊",
    variant: str = "blue",
    delta: Optional[str] = None,
    delta_positive: bool = True,
    help_text: Optional[str] = None,
):
    """
    Render a single enterprise styled KPI card with subtle gradient accents.
    """
    gradient_class = f"card-gradient-{variant}" if variant in ("blue", "green", "amber", "red", "purple") else "card-gradient-blue"
    icon_class = f"card-icon-{variant}" if variant in ("blue", "green", "amber", "red", "purple") else "card-icon-blue"

    delta_html = ""
    if delta:
        delta_class = "card-delta-positive" if delta_positive else "card-delta-negative"
        delta_arrow = "▲" if delta_positive else "▼"
        delta_html = f'<span class="{delta_class}" style="margin-left:0.45rem; font-size:0.74rem; vertical-align:middle;">{delta_arrow} {delta}</span>'

    subtitle_html = (
        f'<div class="card-subtitle" style="margin-top:auto; padding-top:0.35rem; font-size:0.8rem; color:#64748B; font-weight:500; min-height:1.2rem; line-height:1.4;">{subtitle}</div>'
        if subtitle
        else '<div style="min-height:0.5rem;"></div>'
    )

    html = f"""
    <div class="card-surface {gradient_class}" style="height:100%; min-height:144px; display:flex; flex-direction:column; justify-content:space-between; padding:1.15rem 1.25rem; box-sizing:border-box;">
        <div class="card-header" style="margin-bottom:0.35rem; display:flex; align-items:center; gap:0.6rem;">
            <div class="card-icon {icon_class}" style="width:36px; height:36px; font-size:1.05rem; border-radius:9px; flex-shrink:0;">{icon}</div>
            <div class="card-title" style="font-size:0.78rem; font-weight:700; color:#64748B; margin:0; line-height:1.25; flex:1;">{title}</div>
        </div>
        <div style="flex:1; display:flex; align-items:center; margin:0.2rem 0;">
            <div class="card-value" style="font-size:1.6rem; font-weight:800; color:#0F172A; line-height:1.15; word-break:break-word;">
                {value}{delta_html}
            </div>
        </div>
        {subtitle_html}
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)


def render_metric_grid(cards: List[Dict[str, Any]], cols: int = 4):
    """
    Render a responsive grid of metric cards.
    """
    grid = st.columns(cols)
    for i, card in enumerate(cards):
        with grid[i % cols]:
            render_metric_card(
                title=card.get("title", ""),
                value=card.get("value", ""),
                subtitle=card.get("subtitle"),
                icon=card.get("icon", "📊"),
                variant=card.get("variant", "blue"),
                delta=card.get("delta"),
                delta_positive=card.get("delta_positive", True),
                help_text=card.get("help_text"),
            )


def render_stat_badge(label: str, value: str, icon: str = "🏷️", variant: str = "blue"):
    """
    Render a compact inline pill stat badge.
    """
    st.markdown(
        f"""
        <span class="pill pill-{variant}" style="display:inline-flex; align-items:center; gap:0.35rem; padding:0.28rem 0.75rem;">
            <span>{icon}</span>
            <span><b>{label}:</b> {value}</span>
        </span>
        """,
        unsafe_allow_html=True,
    )
