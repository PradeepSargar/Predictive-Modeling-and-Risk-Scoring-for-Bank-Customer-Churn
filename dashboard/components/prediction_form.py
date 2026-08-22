# =============================================================================
# PREDICTION FORM COMPONENT - THEMED EXECUTIVE INTAKE ENGINE
# =============================================================================

"""
Interactive Customer Intake Form with Quick-Load Presets, Themed Glassmorphic
Cards, and Full Palette Integration.
"""

import streamlit as st
import pandas as pd


def render_raw_html(html_str: str):
    """
    Safely render raw HTML directly into the DOM without CommonMark code-block conversion.
    """
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        clean_html = "".join(line.strip() for line in html_str.splitlines() if line.strip())
        st.markdown(clean_html, unsafe_allow_html=True)


PRESETS = {
    "Custom (Manual Input)": {
        "CreditScore": 650, "Age": 35, "Tenure": 5, "Balance": 50000.0,
        "EstimatedSalary": 50000.0, "Gender": "Male", "Geography": "France",
        "NumOfProducts": 1, "HasCrCard": 1, "IsActiveMember": 0
    },
    "🚨 High-Risk Attrition Profile (Middle-Aged, Inactive, Germany)": {
        "CreditScore": 580, "Age": 48, "Tenure": 2, "Balance": 125000.0,
        "EstimatedSalary": 85000.0, "Gender": "Female", "Geography": "Germany",
        "NumOfProducts": 1, "HasCrCard": 0, "IsActiveMember": 0
    },
    "🟢 Stable Loyal Customer (Active, Multi-Product, France)": {
        "CreditScore": 720, "Age": 32, "Tenure": 8, "Balance": 65000.0,
        "EstimatedSalary": 95000.0, "Gender": "Male", "Geography": "France",
        "NumOfProducts": 2, "HasCrCard": 1, "IsActiveMember": 1
    },
    "⚠️ VIP High-Balance Alert (High Balance, Inactive, 1 Product)": {
        "CreditScore": 690, "Age": 52, "Tenure": 6, "Balance": 180000.0,
        "EstimatedSalary": 140000.0, "Gender": "Female", "Geography": "Spain",
        "NumOfProducts": 1, "HasCrCard": 1, "IsActiveMember": 0
    },
}


def customer_prediction_form():
    """
    Render themed customer input form with preset selectors and formatted inputs.
    """
    intro_html = (
        "<div class='form-intro-card'>"
        "<div class='form-intro-icon'>📝</div>"
        "<div style='flex:1;'>"
        "<div class='form-intro-title'>Customer Risk Intake &amp; Scoring Engine</div>"
        "<div class='form-intro-body'>"
        "Enter customer attributes below or choose a <b>preset profile</b> to test scenarios instantly. "
        "Click <b>🔮 Predict Customer Churn Risk</b> to evaluate the Gradient Boosting production pipeline."
        "</div>"
        "</div>"
        "</div>"
    )
    render_raw_html(intro_html)

    # Dynamic presets support preloaded customer from Risk Portfolio
    presets_dict = dict(PRESETS)
    default_idx = 0
    if "loaded_customer_data" in st.session_state and st.session_state["loaded_customer_data"]:
        loaded = st.session_state["loaded_customer_data"]
        cid = loaded.get("CustomerId", "Profile")
        sname = loaded.get("Surname", "Account")
        loaded_key = f"👤 Selected Account #{cid} ({sname})"
        presets_dict = {loaded_key: loaded, **presets_dict}
        default_idx = 0

    preset_choice = st.selectbox(
        "⚡ Quick-Load Customer Presets (Demo Scenarios)",
        list(presets_dict.keys()),
        index=default_idx,
        help="Select a realistic banking customer persona to quickly populate all form fields."
    )
    p_data = presets_dict[preset_choice]

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#E0F2FE; color:#0284C7; border:1px solid #BAE6FD;'>📊 Financial &amp; Demographic Profile</span>"
            "</div>"
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=300,
            max_value=900,
            value=int(p_data["CreditScore"]),
            step=5,
            help="FICO-equivalent credit score (300–900).",
        )

        age = st.number_input(
            "Age (Years)",
            min_value=18,
            max_value=100,
            value=int(p_data["Age"]),
            step=1,
            help="Customer age in years. Middle-aged (40-55) cohorts historically show higher churn risk.",
        )

        tenure = st.number_input(
            "Tenure (Years with Bank)",
            min_value=0,
            max_value=10,
            value=int(p_data["Tenure"]),
            step=1,
            help="Relationship duration with the bank.",
        )

        balance = st.number_input(
            "Account Balance ($)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(p_data["Balance"]),
            step=1000.0,
            format="%.2f",
            help="Current total account balance.",
        )

        estimated_salary = st.number_input(
            "Estimated Annual Salary ($)",
            min_value=0.0,
            max_value=1000000.0,
            value=float(p_data["EstimatedSalary"]),
            step=1000.0,
            format="%.2f",
            help="Annual customer salary estimate.",
        )

    with col2:
        render_raw_html(
            "<div style='margin:0.25rem 0 0.5rem 0; display:flex; align-items:center; gap:0.4rem;'>"
            "<span class='filter-header-badge' style='background:#FAF5FF; color:#7E22CE; border:1px solid #DDD6FE;'>🏦 Product Holdings &amp; Engagement</span>"
            "</div>"
        )

        gender_opts = ["Male", "Female"]
        gender = st.selectbox(
            "Gender",
            gender_opts,
            index=gender_opts.index(p_data["Gender"]),
            help="Customer gender captured at account registration.",
        )

        geo_opts = ["France", "Germany", "Spain"]
        geography = st.selectbox(
            "Geography",
            geo_opts,
            index=geo_opts.index(p_data["Geography"]),
            help="Customer's primary country branch.",
        )

        num_products = st.selectbox(
            "Number of Bank Products Held",
            [1, 2, 3, 4],
            index=int(p_data["NumOfProducts"]) - 1,
            help="Total count of products (savings, loans, cards, investments).",
        )

        has_card = st.selectbox(
            "Credit Card Holder?",
            [1, 0],
            index=0 if p_data["HasCrCard"] == 1 else 1,
            format_func=lambda x: "Yes — Active Card Holder" if x == 1 else "No — No Credit Card",
            help="Whether the customer holds a bank-issued credit card.",
        )

        active_member = st.selectbox(
            "Active Member Status",
            [1, 0],
            index=0 if p_data["IsActiveMember"] == 1 else 1,
            format_func=lambda x: "Active — Engaged Customer" if x == 1 else "Inactive — Low Activity",
            help="Key engagement flag. Inactive members exhibit over 2× higher attrition rate.",
        )

    gender_num = 1 if gender == "Male" else 0
    geo_germany = 1 if geography == "Germany" else 0
    geo_spain = 1 if geography == "Spain" else 0

    customer_data = pd.DataFrame({
        "CreditScore": [credit_score],
        "Gender": [gender_num],
        "Age": [age],
        "Tenure": [tenure],
        "Balance": [balance],
        "NumOfProducts": [num_products],
        "HasCrCard": [has_card],
        "IsActiveMember": [active_member],
        "EstimatedSalary": [estimated_salary],
        "Geography_Germany": [geo_germany],
        "Geography_Spain": [geo_spain],
    })

    st.markdown('<div style="height:0.6rem;"></div>', unsafe_allow_html=True)

    predict_button = st.button(
        "🔮 Predict Customer Churn Risk",
        type="primary",
        use_container_width=True,
    )

    return customer_data, predict_button
