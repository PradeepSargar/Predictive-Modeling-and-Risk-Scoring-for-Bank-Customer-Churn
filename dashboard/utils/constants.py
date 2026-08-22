# =============================================================================
# DESIGN SYSTEM CONSTANTS & TOKENS
# =============================================================================

# Primary Brand (Sky Blue)
PRIMARY_SKY = "#0EA5E9"
PRIMARY_DARK = "#0284C7"
PRIMARY_SKY_DARK = "#0284C7"
PRIMARY_LIGHT = "#E0F2FE"
PRIMARY_SKY_LIGHT = "#E0F2FE"
PRIMARY_SOFT = "#F0F9FF"
PRIMARY_SKY_SOFT = "#F0F9FF"

# Secondary Brand (Purple)
SECONDARY_PURPLE = "#A855F7"
SECONDARY_DARK = "#7E22CE"
SECONDARY_PURPLE_DARK = "#7E22CE"
SECONDARY_LIGHT = "#F3E8FF"
SECONDARY_PURPLE_LIGHT = "#F3E8FF"
SECONDARY_SOFT = "#FAF5FF"
SECONDARY_PURPLE_SOFT = "#FAF5FF"

# Semantic Status Tokens
SUCCESS_GREEN = "#10B981"
SUCCESS_LIGHT = "#D1FAE5"

WARNING_AMBER = "#F59E0B"
WARNING_LIGHT = "#FEF3C7"

DANGER_RED = "#EF4444"
DANGER_LIGHT = "#FEE2E2"

INFO_BLUE = "#38BDF8"
INFO_LIGHT = "#E0F2FE"

# Surface & Background Tokens
BG_MAIN = "#F8FAFC"
BG_TOP = "#F0F9FF"
BG_SOFT = "#F1F5F9"
BG_CARD = "#FFFFFF"

# Neutral Text Tokens
TEXT_PRIMARY = "#0F172A"
TEXT_SECONDARY = "#334155"
TEXT_MUTED = "#64748B"
TEXT_LIGHT = "#94A3B8"

# Border Tokens
BORDER_DEFAULT = "#E2E8F0"
BORDER_STRONG = "#CBD5E1"
BORDER_ACCENT = "#BAE6FD"

# Chart Color Palette (Standardized 10-Color Sequence)
CHART_COLOR_PALETTE = [
    "#0EA5E9",  # Sky Blue
    "#A855F7",  # Purple
    "#10B981",  # Emerald Green
    "#F59E0B",  # Amber
    "#EF4444",  # Crimson Red
    "#38BDF8",  # Light Sky
    "#EC4899",  # Pink
    "#6366F1",  # Indigo
    "#14B8A6",  # Teal
    "#C084FC",  # Lavender
]

# Legacy Compatibility Aliases
PRIMARY_BLUE = PRIMARY_SKY
PRIMARY_BLUE_LIGHT = PRIMARY_DARK
PRIMARY_BLUE_SOFT = PRIMARY_LIGHT
PURPLE = SECONDARY_PURPLE
CYAN = INFO_BLUE
GOLD = WARNING_AMBER
NEUTRAL_700 = TEXT_SECONDARY
NEUTRAL_500 = TEXT_MUTED
NEUTRAL_300 = BORDER_STRONG
NEUTRAL_100 = BG_SOFT
CARD_BORDER = BORDER_DEFAULT
CARD_SHADOW = "rgba(14, 165, 233, 0.05)"
BG_SURFACE = BG_CARD
BG_SURFACE_ALT = BG_MAIN
BG_GRADIENT_START = BG_TOP
BG_GRADIENT_END = BG_MAIN

# Typography & Chart Layout
FONT_FAMILY = "Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
FONT_SIZE = 13
CHART_HEIGHT = 440
PLOTLY_TEMPLATE = "plotly_white"

# Business & Threshold Constants
LOW_RISK_THRESHOLD = 0.30
MEDIUM_RISK_THRESHOLD = 0.60
HIGH_RISK_THRESHOLD = 0.60
LOW_RISK = "Low Risk"
MEDIUM_RISK = "Medium Risk"
HIGH_RISK = "High Risk"
CHURN = "Elevated Churn Risk"
NO_CHURN = "Likely to Stay"

# Brand Metadata
BRAND_NAME = "Bank Churn Intelligence"
BRAND_TAGLINE = "Predictive Analytics & Risk Platform"
DEVELOPER_NAME = "Pradeep Sargar"
UNIVERSITY_NAME = "University of Mumbai"
DEGREE_NAME = "Computer Engineering"
