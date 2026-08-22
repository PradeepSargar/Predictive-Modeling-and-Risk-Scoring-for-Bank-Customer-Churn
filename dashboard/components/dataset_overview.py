import streamlit as st

from components.kpi_card import render_kpi_row
from components.section_header import display_section_header


def display_dataset_overview():
    display_section_header(
        "Dataset Overview",
        "European Bank customer cohort — 10,000 customer profiles with 11 input features and a binary churn target.",
        accent_color="#1E40AF",
    )

    cards = [
        {"title": "Total Customers", "value": "10,000", "icon": "👥", "variant": "blue",
         "subtitle": "Labelled cohort"},
        {"title": "Input Features", "value": "11", "icon": "🧬", "variant": "purple",
         "subtitle": "Demographics + behaviour"},
        {"title": "Target Variable", "value": "Exited", "icon": "🎯", "variant": "red",
         "subtitle": "0 = Stayed · 1 = Churned"},
        {"title": "Champion Model", "value": "Gradient Boosting", "icon": "🏆", "variant": "green",
         "subtitle": "86.31% CV Accuracy"},
    ]
    render_kpi_row(cards, cols=4)
