# =============================================================================
# BUSINESS INSIGHTS
# =============================================================================

"""
Reusable Business Insight Generator
"""

import streamlit as st


def generate_top_category_insight(

    df,

    category_column,

    target_column,

    positive_label="Churned Customers"

):
    """
    Display the category with the highest number of positive events.
    """

    insight_data = (

        df[df[target_column] == 1]

        .groupby(category_column)

        .size()

        .sort_values(ascending=False)

    )

    if insight_data.empty:

        st.warning("No data available.")

        return

    top_category = insight_data.index[0]

    top_value = insight_data.iloc[0]

    st.info(

        f"""
📌 **Business Insight**

**{top_category}** has the highest number of
**{positive_label.lower()}**
with **{top_value:,} customers**.

This segment should be prioritized for customer
retention strategies.
        """

    )