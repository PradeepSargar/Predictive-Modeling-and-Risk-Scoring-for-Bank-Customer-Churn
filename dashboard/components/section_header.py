import streamlit as st


def display_section_header(title, description=None, accent_color="#0EA5E9", right_element=None):
    desc_html = ""
    if description:
        desc_html = f'<p class="section-header-description">{description}</p>'

    right_html = ""
    if right_element:
        right_html = f"<div>{right_element}</div>"

    st.markdown(
        f"""
        <div class="section-header-wrapper">
            <div class="section-header-left">
                <div class="section-header-accent" style="background: linear-gradient(180deg, {accent_color} 0%, #38BDF8 100%);"></div>
                <div>
                    <h3 class="section-header-title">{title}</h3>
                    {desc_html}
                </div>
            </div>
            {right_html}
        </div>
        """,
        unsafe_allow_html=True,
    )
