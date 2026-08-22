import streamlit as st


def display_customer_summary(customer_data):

    summary = customer_data.copy()

    summary["Gender"] = summary["Gender"].replace({
        1: "Male",
        0: "Female"
    })

    geography = []

    for _, row in summary.iterrows():
        if row["Geography_Germany"] == 1:
            geography.append("Germany")
        elif row["Geography_Spain"] == 1:
            geography.append("Spain")
        else:
            geography.append("France")

    summary["Geography"] = geography

    summary = summary.drop(
        columns=[
            "Geography_Germany",
            "Geography_Spain"
        ],
        errors="ignore"
    )

    summary = summary[[
        "CreditScore",
        "Gender",
        "Age",
        "Geography",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary"
    ]]

    cs = int(summary.iloc[0]["CreditScore"])
    gender = summary.iloc[0]["Gender"]
    age = int(summary.iloc[0]["Age"])
    geo = summary.iloc[0]["Geography"]
    tenure = int(summary.iloc[0]["Tenure"])
    balance = float(summary.iloc[0]["Balance"])
    products = int(summary.iloc[0]["NumOfProducts"])
    has_card = int(summary.iloc[0]["HasCrCard"])
    active = int(summary.iloc[0]["IsActiveMember"])
    salary = float(summary.iloc[0]["EstimatedSalary"])

    st.markdown(
        """
        <div style="background:#F0F9FF; border:1px solid #BAE6FD; border-radius:14px; padding:0.95rem 1.25rem; margin-bottom:1rem; display:flex; align-items:flex-start; gap:0.85rem; box-shadow:0 4px 18px -2px rgba(14,165,233,0.05);">
            <div style="width:38px; height:38px; border-radius:10px; background:linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color:#FFFFFF; display:flex; align-items:center; justify-content:center; font-size:1.1rem; flex-shrink:0; box-shadow:0 3px 10px rgba(14,165,233,0.25);">👤</div>
            <div style="flex:1;">
                <div style="font-size:0.74rem; font-weight:700; letter-spacing:0.05em; text-transform:uppercase; color:#0284C7; margin-bottom:0.15rem;">Input Profile Snapshot</div>
                <div style="font-size:1rem; font-weight:800; color:#0F172A; line-height:1.2;">Decoded Customer Features Evaluated in This Run</div>
                <div style="font-size:0.84rem; color:#334155; margin-top:0.2rem; line-height:1.45;">Standardized customer features ingested into the Gradient Boosting model.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    def _attr_card(icon, title, value, subtitle="", variant="blue"):
        sub_html = f'<div style="font-size:0.76rem; color:#64748B; font-weight:500; margin-top:0.25rem; line-height:1.3;">{subtitle}</div>' if subtitle else ""
        return f"""
        <div class="card-surface card-gradient-{variant}" style="padding:0.9rem 1.05rem; min-height:112px; display:flex; flex-direction:column; justify-content:space-between;">
            <div class="card-header" style="margin-bottom:0.25rem; gap:0.5rem; min-height:auto;">
                <div class="card-icon card-icon-{variant}" style="width:32px; height:32px; border-radius:8px; font-size:0.95rem;">{icon}</div>
                <div class="card-title" style="font-size:0.72rem; font-weight:700; color:#64748B;">{title}</div>
            </div>
            <div class="card-value" style="font-size:1.25rem; font-weight:800; color:#0F172A;">
                {value}
            </div>
            {sub_html}
        </div>
        """

    cs_variant = "green" if cs >= 700 else ("amber" if cs >= 600 else "red")
    cs_label = "Prime Tier" if cs >= 750 else ("Good Tier" if cs >= 700 else ("Fair Tier" if cs >= 600 else "Subprime Tier"))

    active_variant = "green" if active == 1 else "amber"
    active_label = "Active Member" if active == 1 else "Inactive Member"
    card_label = "Credit Card Holder" if has_card == 1 else "No Credit Card"

    geo_icon = {"France": "🇫🇷", "Germany": "🇩🇪", "Spain": "🇪🇸"}.get(geo, "🌍")
    gender_icon = {"Male": "👨", "Female": "👩"}.get(gender, "👤")

    st.markdown(
        f"""
        <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.75rem; margin-bottom:0.75rem;">
            {_attr_card(gender_icon, "Gender", gender, variant="purple")}
            {_attr_card("🎂", "Age", f"{age} yrs", variant="blue")}
            {_attr_card(geo_icon, "Country", geo, variant="purple")}
            {_attr_card("⏱️", "Tenure", f"{tenure} yrs", "with bank", variant="amber")}
            {_attr_card("⭐", "Credit Score", f"{cs:,}", cs_label, variant=cs_variant)}
        </div>
        <div style="display:grid; grid-template-columns:repeat(5, 1fr); gap:0.75rem;">
            {_attr_card("💰", "Account Balance", f"${balance:,.2f}", variant="green")}
            {_attr_card("💼", "Annual Salary", f"${salary:,.2f}", variant="green")}
            {_attr_card("📦", "Products Held", f"{products} Product{'s' if products != 1 else ''}", variant="blue")}
            {_attr_card("💳", "Card Status", card_label, variant="blue" if has_card == 1 else "amber")}
            {_attr_card("🟢" if active == 1 else "⚪", "Engagement", active_label, variant=active_variant)}
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:0.25rem;"></div>', unsafe_allow_html=True)

    with st.expander("🔍 View Raw Machine-Learning Ingestion Schema", expanded=False):
        display_df = summary.copy()
        display_df.columns = [
            "Credit Score",
            "Gender",
            "Age",
            "Geography",
            "Tenure",
            "Balance",
            "Products",
            "Credit Card",
            "Active Member",
            "Estimated Salary"
        ]
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )
