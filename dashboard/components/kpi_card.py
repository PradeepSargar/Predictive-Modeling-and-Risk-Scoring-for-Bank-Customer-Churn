import streamlit as st


def _card_html(
    label,
    value,
    icon="📊",
    icon_style="blue",
    card_style="default",
    delta=None,
    delta_positive=True,
    subtitle=None,
):
    gradient_class = {
        "blue": "card-gradient-blue",
        "green": "card-gradient-green",
        "amber": "card-gradient-amber",
        "red": "card-gradient-red",
        "purple": "card-gradient-purple",
        "default": "card-gradient-blue",
    }.get(card_style, "card-gradient-blue")

    icon_class = {
        "blue": "card-icon-blue",
        "green": "card-icon-green",
        "amber": "card-icon-amber",
        "red": "card-icon-red",
        "purple": "card-icon-purple",
    }.get(icon_style, "card-icon-blue")

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

    return f"""
    <div class="card-surface {gradient_class}" style="height:100%; min-height:144px; display:flex; flex-direction:column; justify-content:space-between; padding:1.15rem 1.25rem; box-sizing:border-box;">
        <div class="card-header" style="margin-bottom:0.35rem; display:flex; align-items:center; gap:0.6rem;">
            <div class="card-icon {icon_class}" style="width:36px; height:36px; font-size:1.05rem; border-radius:9px; flex-shrink:0;">{icon}</div>
            <div class="card-title" style="font-size:0.78rem; font-weight:700; color:#64748B; margin:0; line-height:1.25; flex:1;">{label}</div>
        </div>
        <div style="flex:1; display:flex; align-items:center; margin:0.2rem 0;">
            <div class="card-value" style="font-size:1.6rem; font-weight:800; color:#0F172A; line-height:1.15; word-break:break-word;">
                {value}{delta_html}
            </div>
        </div>
        {subtitle_html}
    </div>
    """


def display_kpi_card(
    title,
    value,
    icon="📊",
    help_text=None,
    variant="blue",
    delta=None,
    delta_positive=True,
    subtitle=None,
):
    gradient_map = {
        "blue": "blue",
        "green": "green",
        "amber": "amber",
        "red": "red",
        "purple": "purple",
        "default": "default",
    }
    style = gradient_map.get(variant, "default")
    html = _card_html(title, value, icon, variant, style, delta, delta_positive, subtitle)
    st.markdown(html, unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)


def render_kpi_row(cards, cols=4):
    """
    Render a responsive, equal-height grid of KPI cards.
    """
    grid = st.columns(cols)
    for i, card in enumerate(cards):
        with grid[i % cols]:
            display_kpi_card(
                title=card.get("title", ""),
                value=card.get("value", ""),
                icon=card.get("icon", "📊"),
                variant=card.get("variant", "blue"),
                delta=card.get("delta"),
                delta_positive=card.get("delta_positive", True),
                subtitle=card.get("subtitle"),
                help_text=card.get("help_text"),
            )
