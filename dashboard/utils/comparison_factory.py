# =============================================================================
# COMPARISON CHART FACTORY
# =============================================================================

"""
Reusable factory for comparison charts.
"""

import pandas as pd

from utils.chart_factory import create_bar_chart


def create_comparison_chart(
    df,
    category_column,
    target_column,
    chart_title,
    x_title,
    y_title,
    positive_label="Churned",
    negative_label="Retained"
):

    # ============================================================
    # Prepare Data
    # ============================================================

    comparison_df = (

        df.groupby(
            [category_column, target_column]
        )

        .size()

        .reset_index(name="Customers")

    )

    comparison_df[target_column] = comparison_df[target_column].replace({

        0: negative_label,

        1: positive_label

    })

    # ============================================================
    # Create Chart
    # ============================================================

    fig = create_bar_chart(

        data=comparison_df,

        x=category_column,

        y="Customers",

        color=target_column,

        text="Customers",

        title=chart_title,

        x_title=x_title,

        y_title=y_title

    )

    return fig

