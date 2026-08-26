# =============================================================================
# ENTERPRISE PREDICTIVE ANALYTICS DESIGN SYSTEM & THEME
# =============================================================================

"""
Centralized Enterprise Design System module for Bank Churn Intelligence Platform.
Implements the Sky Blue / Purple enterprise analytics visual design language:
- Clean light analytical interface with zero animation lag on page switch
- Fixed 280px soft light-blue gradient sidebar with hidden scrollbars
- 14px rounded cards with restrained glassmorphism & subtle sky-blue shadows
- Uniform container spacing, layout alignment, and card heights
- High-contrast Inter typography
- Standardized insight & alert cards (SUCCESS, WARNING, RISK, INSIGHT, RECOMMENDATION)
"""

import streamlit as st


def apply_global_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        /* -------------------------------------------------------------------------
           1. ROOT RESETS & ZERO DISTRACTING JANK
           ------------------------------------------------------------------------- */
        *, *::before, *::after {
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        html, body, #root, [data-testid="stAppViewContainer"], [data-testid="stApp"], .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #F8FAFC !important;
            background: linear-gradient(180deg, #F0F9FF 0%, #F8FAFC 240px, #F8FAFC 100%) !important;
            background-attachment: fixed !important;
            color: #0F172A !important;
        }

        /* -------------------------------------------------------------------------
           2. STREAMLIT APP SHELL & 1440px CENTERED MAIN CONTAINER
           ------------------------------------------------------------------------- */
        @keyframes pageFadeInSlideUp {
            0% {
                opacity: 0;
                transform: translateY(6px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes tabFadeIn {
            0% {
                opacity: 0;
                transform: translateY(4px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        [data-testid="stHeader"] {
            background: rgba(255, 255, 255, 0.92) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-bottom: 1px solid #E2E8F0 !important;
            height: 56px;
            z-index: 100;
        }

        [data-testid="block-container"],
        .main .block-container {
            padding-top: 1.25rem !important;
            padding-bottom: 3rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            max-width: 1440px !important;
            margin: 0 auto !important;
            animation: pageFadeInSlideUp 0.28s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            will-change: opacity, transform;
        }

        [data-baseweb="tab-panel"] {
            animation: tabFadeIn 0.24s cubic-bezier(0.16, 1, 0.3, 1) forwards;
            will-change: opacity, transform;
        }

        /* Smooth interactive hover transitions on interactive cards and buttons */
        .card-surface,
        [data-testid="stMetric"],
        .status-banner,
        .stepper-card,
        .brand-header {
            transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                        box-shadow 0.2s cubic-bezier(0.16, 1, 0.3, 1),
                        border-color 0.18s ease !important;
        }

        /* -------------------------------------------------------------------------
           3. FIXED 280px LIGHT-BLUE GRADIENT SIDEBAR (NO SCROLLBARS)
           ------------------------------------------------------------------------- */
        section[data-testid="stSidebar"] {
            width: 280px !important;
            min-width: 280px !important;
            max-width: 280px !important;
            background: linear-gradient(180deg, #E0F2FE 0%, #BAE6FD 30%, #E0F2FE 70%, #F0F9FF 100%) !important;
            border-right: 1px solid rgba(14, 165, 233, 0.25) !important;
            box-shadow: 2px 0 16px rgba(14, 165, 233, 0.08) !important;
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
        }

        section[data-testid="stSidebar"]::-webkit-scrollbar {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }

        section[data-testid="stSidebar"] > div:first-child {
            scrollbar-width: none !important;
            -ms-overflow-style: none !important;
            padding-top: 0 !important;
        }

        section[data-testid="stSidebar"] > div:first-child::-webkit-scrollbar {
            display: none !important;
        }

        /* -------------------------------------------------------------------------
           HIDE DEFAULT STREAMLIT AUTO-GENERATED SIDEBAR NAVIGATION
           ------------------------------------------------------------------------- */
        [data-testid="stSidebarNav"],
        div[data-testid="stSidebarNav"],
        ul[data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        section[data-testid="stSidebar"] > div:first-child > div:has([data-testid="stSidebarNav"]) {
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
        }

        /* Custom Structured st.page_link Navigation Styles */
        .stPageLink {
            margin: 0.15rem 0.35rem !important;
        }

        .stPageLink a,
        div[data-testid="stPageLink-NavLink"] a {
            border-radius: 10px !important;
            padding: 0.5rem 0.85rem !important;
            color: #0F172A !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
            background: rgba(255, 255, 255, 0.45) !important;
            border: 1px solid rgba(14, 165, 233, 0.15) !important;
            display: flex !important;
            align-items: center !important;
            text-decoration: none !important;
            transition: background 0.12s ease, border-color 0.12s ease !important;
        }

        .stPageLink a:hover,
        div[data-testid="stPageLink-NavLink"] a:hover {
            background: #FFFFFF !important;
            color: #0284C7 !important;
            border-color: #BAE6FD !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.12) !important;
        }

        .stPageLink a[aria-current="page"],
        div[data-testid="stPageLink-NavLink"] a[aria-current="page"] {
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            border-color: #0EA5E9 !important;
            box-shadow: 0 3px 12px rgba(14, 165, 233, 0.32) !important;
        }

        .stPageLink a[aria-current="page"] span,
        .stPageLink a[aria-current="page"] div,
        .stPageLink a[aria-current="page"] p,
        div[data-testid="stPageLink-NavLink"] a[aria-current="page"] span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        .sidebar-brand {
            padding: 1.25rem 1.15rem 0.95rem 1.15rem;
            border-bottom: 1px solid rgba(14, 165, 233, 0.2);
            background: transparent;
        }

        .sidebar-logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .sidebar-logo-mark {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            font-weight: 800;
            box-shadow: 0 3px 10px rgba(14, 165, 233, 0.28);
            flex-shrink: 0;
        }

        .sidebar-brand-name {
            font-size: 0.95rem;
            font-weight: 800;
            color: #0F172A !important;
            letter-spacing: -0.01em;
            line-height: 1.15;
        }

        .sidebar-brand-tagline {
            font-size: 0.72rem;
            color: #0284C7 !important;
            font-weight: 600;
        }

        .sidebar-section {
            padding: 0.75rem 0.4rem 0.25rem 0.4rem;
        }

        .sidebar-section-title {
            font-size: 0.68rem;
            font-weight: 700;
            color: #0369A1 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            padding: 0 0.85rem;
            margin-bottom: 0.35rem;
        }

        .sidebar-metric-card {
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(14, 165, 233, 0.22);
            border-radius: 10px;
            padding: 0.65rem 0.85rem;
            margin: 0.3rem 0.45rem;
            backdrop-filter: blur(8px);
        }

        .sidebar-metric-label {
            font-size: 0.72rem;
            color: #475569 !important;
            font-weight: 600;
            margin-bottom: 0.15rem;
        }

        .sidebar-metric-value {
            font-size: 1.05rem;
            font-weight: 800;
            color: #0F172A !important;
        }

        .sidebar-footer {
            padding: 1rem 1.15rem;
            border-top: 1px solid rgba(14, 165, 233, 0.2);
            background: transparent;
            margin-top: 0.75rem;
        }

        .footer-name {
            font-size: 0.82rem;
            font-weight: 700;
            color: #0F172A !important;
        }

        .footer-text {
            font-size: 0.74rem;
            color: #475569 !important;
            line-height: 1.5;
            font-weight: 500;
        }

        /* -------------------------------------------------------------------------
           4. FLEXBOX COLUMNS & CONSISTENT SPACING
           ------------------------------------------------------------------------- */
        [data-testid="column"] {
            min-width: 0 !important;
        }

        [data-testid="column"] > div:has(.card-surface) {
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
        }

        /* -------------------------------------------------------------------------
           5. TYPOGRAPHY (INTER, SHARP CONTRAST)
           ------------------------------------------------------------------------- */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            margin: 0 0 0.25rem 0;
        }

        h1 { font-size: 1.75rem; line-height: 1.2; }
        h2 { font-size: 1.4rem; line-height: 1.25; }
        h3 { font-size: 1.12rem; line-height: 1.3; }
        h4 { font-size: 0.96rem; }

        p, div, span, label, li {
            color: #1E293B;
        }

        .stMarkdown p {
            color: #334155 !important;
            line-height: 1.6;
            font-size: 0.9rem;
        }

        .stMarkdown p strong {
            color: #0F172A !important;
            font-weight: 700;
        }

        hr {
            border: none;
            border-top: 1px solid #E2E8F0;
            margin: 1.25rem 0;
        }

        /* -------------------------------------------------------------------------
           6. 14px ROUNDED CARDS WITH RESTRAINED GLASSMORPHISM & SKY BLUE SHADOWS
           ------------------------------------------------------------------------- */
        .card-surface {
            background: rgba(255, 255, 255, 0.96);
            backdrop-filter: blur(16px) saturate(180%);
            -webkit-backdrop-filter: blur(16px) saturate(180%);
            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 14px;
            padding: 1.15rem 1.25rem;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.05);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            height: 100%;
            box-sizing: border-box;
            margin-bottom: 0.85rem;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }

        .card-surface:hover {
            border-color: #BAE6FD;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.08);
        }

        /* Card Header & Icon */
        .card-header {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.35rem;
            min-height: 38px;
        }

        .card-icon {
            width: 38px;
            height: 38px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            flex-shrink: 0;
        }

        .card-icon-blue { background: #E0F2FE; color: #0284C7; border: 1px solid #BAE6FD; }
        .card-icon-green { background: #D1FAE5; color: #065F46; border: 1px solid #A7F3D0; }
        .card-icon-amber { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
        .card-icon-red { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
        .card-icon-purple { background: #F3E8FF; color: #7E22CE; border: 1px solid #DDD6FE; }

        /* Card Typography */
        .card-title {
            font-size: 0.78rem;
            font-weight: 700;
            color: #64748B !important;
            letter-spacing: 0.03em;
            text-transform: uppercase;
            line-height: 1.25;
            margin: 0;
        }

        .card-value {
            font-size: 1.6rem;
            font-weight: 800;
            color: #0F172A !important;
            letter-spacing: -0.02em;
            line-height: 1.2;
        }

        .card-subtitle {
            font-size: 0.8rem;
            color: #64748B !important;
            font-weight: 500;
            line-height: 1.4;
            margin-top: auto;
            padding-top: 0.35rem;
        }

        /* Card Accent Variants (1px border + 3px top highlight) */
        .card-gradient-blue { border-top: 3px solid #0EA5E9; border-color: #BAE6FD; }
        .card-gradient-green { border-top: 3px solid #10B981; border-color: #A7F3D0; }
        .card-gradient-amber { border-top: 3px solid #F59E0B; border-color: #FDE68A; }
        .card-gradient-red { border-top: 3px solid #EF4444; border-color: #FECACA; }
        .card-gradient-purple { border-top: 3px solid #A855F7; border-color: #DDD6FE; }

        /* Delta Indicators */
        .card-delta-positive {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.74rem;
            font-weight: 700;
            color: #065F46 !important;
            background: #D1FAE5;
            padding: 0.18rem 0.55rem;
            border-radius: 6px;
        }

        .card-delta-negative {
            display: inline-flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.74rem;
            font-weight: 700;
            color: #991B1B !important;
            background: #FEE2E2;
            padding: 0.18rem 0.55rem;
            border-radius: 6px;
        }

        /* -------------------------------------------------------------------------
           7. EXECUTIVE BRAND HERO HEADER (SIDEBAR LIGHT-BLUE GRADIENT THEME)
           ------------------------------------------------------------------------- */
        .brand-header {
            background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 40%, #E0F2FE 75%, #F0F9FF 100%);
            color: #0F172A;
            border-radius: 14px;
            padding: 1.05rem 1.4rem;
            margin-bottom: 1.15rem;
            border: 1px solid #BAE6FD;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.09);
        }

        .brand-header-inner {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1.25rem;
            flex-wrap: wrap;
        }

        .brand-header-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            flex-shrink: 0;
            box-shadow: 0 3px 10px rgba(14, 165, 233, 0.25);
        }

        .brand-header-title,
        .brand-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #0F172A !important;
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin: 0;
        }

        .brand-header-subtitle,
        .brand-subtitle {
            font-size: 0.86rem;
            color: #0284C7 !important;
            font-weight: 600;
            margin-top: 0.2rem;
            line-height: 1.45;
        }

        .brand-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(255, 255, 255, 0.85);
            border: 1px solid rgba(14, 165, 233, 0.3);
            border-radius: 8px;
            padding: 0.35rem 0.75rem;
            font-size: 0.78rem;
            font-weight: 700;
            color: #0F172A;
            backdrop-filter: blur(8px);
        }

        /* -------------------------------------------------------------------------
           8. SECTION HEADERS & UNIFORM MARGINS
           ------------------------------------------------------------------------- */
        .section-header-wrapper {
            margin: 1.35rem 0 0.75rem 0;
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .section-header-left {
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }

        .section-header-accent {
            width: 4px;
            height: 28px;
            border-radius: 3px;
            background: #0EA5E9;
            flex-shrink: 0;
            margin-top: 2px;
        }

        .section-header-title {
            font-size: 1.12rem;
            font-weight: 700;
            color: #0F172A !important;
            letter-spacing: -0.01em;
            margin: 0;
            line-height: 1.25;
        }

        .section-header-description {
            font-size: 0.85rem;
            color: #64748B !important;
            font-weight: 500;
            margin: 0.15rem 0 0 0;
            line-height: 1.5;
        }

        .section-divider {
            height: 1px;
            background: linear-gradient(90deg, rgba(226, 232, 240, 0) 0%, #CBD5E1 15%, #CBD5E1 85%, rgba(226, 232, 240, 0) 100%);
            margin: 1.5rem 0 1.25rem 0;
        }

        .graph-group-header {
            display: flex;
            align-items: center;
            gap: 0.6rem;
            margin-bottom: 0.85rem;
            margin-top: 0.25rem;
        }

        .graph-group-title {
            font-size: 0.96rem;
            font-weight: 700;
            color: #0F172A !important;
            letter-spacing: -0.01em;
        }

        .graph-group-badge {
            background: #E0F2FE;
            color: #0284C7 !important;
            border: 1px solid #BAE6FD;
            padding: 0.2rem 0.65rem;
            border-radius: 6px;
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        /* -------------------------------------------------------------------------
           8b. PLOTLY INTERACTIVE MODEBAR CONTROLS (ZOOM, PAN, AUTOSCALE, RESET)
           ------------------------------------------------------------------------- */
        .js-plotly-plot .plotly .modebar-container {
            z-index: 99 !important;
            position: absolute !important;
            top: 8px !important;
            right: 12px !important;
            pointer-events: none !important;
        }

        .js-plotly-plot .plotly .modebar {
            display: inline-flex !important;
            align-items: center !important;
            gap: 2px !important;
            background: rgba(255, 255, 255, 0.94) !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            padding: 2px 5px !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
            pointer-events: auto !important;
            opacity: 0.65 !important;
            transition: all 0.2s ease !important;
        }

        .js-plotly-plot .plotly:hover .modebar {
            opacity: 1 !important;
            border-color: #BAE6FD !important;
            box-shadow: 0 3px 12px rgba(14, 165, 233, 0.15) !important;
        }

        .js-plotly-plot .plotly .modebar-btn {
            cursor: pointer !important;
            pointer-events: auto !important;
            padding: 2px 4px !important;
            border-radius: 4px !important;
            transition: background 0.15s ease !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        .js-plotly-plot .plotly .modebar-btn:hover {
            background: #F1F5F9 !important;
        }

        .js-plotly-plot .plotly .modebar-btn svg {
            width: 14px !important;
            height: 14px !important;
            pointer-events: none !important;
        }

        .js-plotly-plot .plotly .modebar-btn svg path {
            fill: #475569 !important;
            pointer-events: none !important;
        }

        .js-plotly-plot .plotly .modebar-btn.active svg path,
        .js-plotly-plot .plotly .modebar-btn:hover svg path {
            fill: #0284C7 !important;
        }

        /* -------------------------------------------------------------------------
           8c. TOP-RIGHT FULLSCREEN EXPAND IN LARGE CONTAINER BUTTON & TOOLBAR
           ------------------------------------------------------------------------- */
        [data-testid="stElementToolbar"],
        [data-testid="stElementToolbar"] > div {
            display: flex !important;
            opacity: 1 !important;
            visibility: visible !important;
            z-index: 100 !important;
            top: 6px !important;
            right: 8px !important;
        }

        [data-testid="StyledFullScreenButton"],
        [data-testid="stElementToolbarButton"],
        button[title="View fullscreen"],
        button[aria-label="Fullscreen"] {
            visibility: visible !important;
            opacity: 0.9 !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            background: #FFFFFF !important;
            border: 1.5px solid #BAE6FD !important;
            border-radius: 8px !important;
            padding: 4px 8px !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.16) !important;
            color: #0284C7 !important;
            cursor: pointer !important;
            transition: all 0.2s ease !important;
            min-height: 28px !important;
        }

        [data-testid="StyledFullScreenButton"]:hover,
        [data-testid="stElementToolbarButton"]:hover,
        button[title="View fullscreen"]:hover,
        button[aria-label="Fullscreen"]:hover {
            opacity: 1 !important;
            background: #E0F2FE !important;
            border-color: #0284C7 !important;
            color: #0369A1 !important;
            transform: scale(1.06) !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.26) !important;
        }

        [data-testid="StyledFullScreenButton"] svg,
        button[title="View fullscreen"] svg {
            fill: #0284C7 !important;
            stroke: #0284C7 !important;
            width: 14px !important;
            height: 14px !important;
        }

        /* -------------------------------------------------------------------------
           9. STREAMLIT METRICS, BUTTONS & FORM INPUTS
           ------------------------------------------------------------------------- */
        [data-testid="stMetric"] {
            background: rgba(255, 255, 255, 0.96);
            border: 1px solid rgba(226, 232, 240, 0.95);
            border-radius: 14px;
            padding: 1.1rem 1.2rem;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.05);
            margin-bottom: 0.85rem;
        }

        [data-testid="stMetricLabel"] {
            color: #64748B !important;
            font-weight: 700;
            font-size: 0.78rem;
            letter-spacing: 0.03em;
            text-transform: uppercase;
        }

        [data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-weight: 800;
            font-size: 1.6rem;
            letter-spacing: -0.02em;
        }

        /* -------------------------------------------------------------------------
           9. PROFESSIONAL THEME BUTTONS (PRIMARY, SECONDARY, DOWNLOAD, PAGELINKS)
           ------------------------------------------------------------------------- */
        .stButton > button,
        .stDownloadButton > button,
        [data-testid="baseButton-primary"],
        button[kind="primary"] {
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #0284C7 !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.4rem !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            letter-spacing: 0.01em !important;
            box-shadow: 0 4px 14px -2px rgba(14, 165, 233, 0.35), 0 2px 4px rgba(14, 165, 233, 0.15) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            cursor: pointer !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover,
        [data-testid="baseButton-primary"]:hover,
        button[kind="primary"]:hover {
            background: linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%) !important;
            border-color: #0284C7 !important;
            color: #FFFFFF !important;
            transform: translateY(-1.5px) !important;
            box-shadow: 0 6px 20px -2px rgba(14, 165, 233, 0.48), 0 3px 6px rgba(14, 165, 233, 0.2) !important;
        }

        .stButton > button:active,
        .stDownloadButton > button:active,
        [data-testid="baseButton-primary"]:active,
        button[kind="primary"]:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.3) !important;
        }

        .stButton > button[kind="secondary"],
        .stDownloadButton > button[kind="secondary"],
        [data-testid="baseButton-secondary"],
        button[kind="secondary"] {
            background: #FFFFFF !important;
            color: #334155 !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 10px !important;
            padding: 0.62rem 1.35rem !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.04) !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            cursor: pointer !important;
        }

        .stButton > button[kind="secondary"]:hover,
        .stDownloadButton > button[kind="secondary"]:hover,
        [data-testid="baseButton-secondary"]:hover,
        button[kind="secondary"]:hover {
            background: #F8FAFC !important;
            border-color: #BAE6FD !important;
            color: #0284C7 !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.12) !important;
        }

        /* Page Links (st.page_link) */
        [data-testid="stPageLink-NavLink"],
        .stPageLink a {
            background: linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%) !important;
            border: 1.5px solid #BAE6FD !important;
            border-radius: 10px !important;
            color: #0284C7 !important;
            font-weight: 700 !important;
            font-size: 0.88rem !important;
            padding: 0.65rem 1.25rem !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            text-decoration: none !important;
            box-shadow: 0 2px 8px rgba(14, 165, 233, 0.08) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stPageLink-NavLink"]:hover,
        .stPageLink a:hover {
            background: #E0F2FE !important;
            border-color: #38BDF8 !important;
            color: #0369A1 !important;
            transform: translateY(-1.5px) !important;
            box-shadow: 0 4px 14px rgba(14, 165, 233, 0.2) !important;
        }

        /* File Uploader Buttons */
        [data-testid="stFileUploader"] section button,
        [data-testid="stFileUploader"] button {
            background: #FFFFFF !important;
            border: 1.5px solid #0EA5E9 !important;
            color: #0284C7 !important;
            font-weight: 700 !important;
            border-radius: 8px !important;
            padding: 0.45rem 1.15rem !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stFileUploader"] section button:hover,
        [data-testid="stFileUploader"] button:hover {
            background: #E0F2FE !important;
            border-color: #0284C7 !important;
            color: #0369A1 !important;
            transform: translateY(-1px) !important;
        }

        /* Multi-select Tags & Badges */
        [data-baseweb="tag"] {
            background: #E0F2FE !important;
            border: 1px solid #BAE6FD !important;
            border-radius: 6px !important;
        }

        [data-baseweb="tag"] span {
            color: #0284C7 !important;
            font-weight: 700 !important;
            font-size: 0.8rem !important;
        }

        /* Widget Labels */
        [data-testid="stWidgetLabel"] label,
        [data-testid="stWidgetLabel"] p,
        .stTextInput label,
        .stSelectbox label,
        .stMultiSelect label,
        .stSlider label,
        .stNumberInput label {
            font-size: 0.84rem !important;
            font-weight: 700 !important;
            color: #1E293B !important;
            margin-bottom: 0.35rem !important;
            letter-spacing: 0.01em !important;
        }

        /* -------------------------------------------------------------------------
           9. STREAMLIT TEXT INPUTS, NUMBER INPUTS & TEXTAREAS (CRISP OUTLINE & LIGHT GREY TEXT)
           ------------------------------------------------------------------------- */
        [data-testid="stTextInput"] [data-baseweb="input"],
        [data-testid="stNumberInput"] [data-baseweb="input"],
        [data-testid="stTextArea"] [data-baseweb="textarea"],
        [data-baseweb="input"],
        [data-baseweb="base-input"],
        [data-baseweb="textarea"],
        .stTextInput > div > div,
        .stNumberInput > div > div,
        .stTextArea > div > div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1.5px solid #CBD5E1 !important; /* Soft border */
            border-radius: 10px !important;
            min-height: 42px !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stTextInput"] [data-baseweb="input"]:hover,
        [data-testid="stNumberInput"] [data-baseweb="input"]:hover,
        [data-testid="stTextArea"] [data-baseweb="textarea"]:hover,
        [data-baseweb="input"]:hover,
        [data-baseweb="base-input"]:hover,
        [data-baseweb="textarea"]:hover,
        .stTextInput > div > div:hover,
        .stNumberInput > div > div:hover,
        .stTextArea > div > div:hover {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
        }

        [data-testid="stTextInput"] [data-baseweb="input"]:focus-within,
        [data-testid="stNumberInput"] [data-baseweb="input"]:focus-within,
        [data-testid="stTextArea"] [data-baseweb="textarea"]:focus-within,
        [data-baseweb="input"]:focus-within,
        [data-baseweb="base-input"]:focus-within,
        [data-baseweb="textarea"]:focus-within,
        .stTextInput > div > div:focus-within,
        .stNumberInput > div > div:focus-within,
        .stTextArea > div > div:focus-within {
            border-color: #0284C7 !important;
            box-shadow: 0 0 0 3.5px rgba(14, 165, 233, 0.22) !important;
        }

        /* Inner typing container input & textarea element styling - LIGHT GREY VISIBLE TEXT */
        input,
        textarea,
        input[type="text"],
        input[type="number"],
        input[type="search"],
        input[type="password"],
        [data-baseweb="input"] input,
        [data-baseweb="base-input"] input,
        [data-baseweb="textarea"] textarea,
        [data-testid="stTextInput"] input,
        [data-testid="stNumberInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-testid="stChatInput"] textarea,
        [data-testid="stChatInput"] input,
        [data-testid="stSelectbox"] input,
        [data-testid="stMultiSelect"] input,
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background: transparent !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            caret-color: #64748B !important;
            font-size: 0.94rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            padding: 0.55rem 0.85rem !important;
        }

        input:focus,
        input:active,
        input:hover,
        textarea:focus,
        textarea:active,
        textarea:hover {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
        }

        /* Browser autofill styling to preserve light grey text on white background */
        input:-webkit-autofill,
        input:-webkit-autofill:hover,
        input:-webkit-autofill:focus,
        input:-webkit-autofill:active {
            -webkit-text-fill-color: #64748B !important;
            -webkit-box-shadow: 0 0 0px 1000px #FFFFFF inset !important;
            box-shadow: 0 0 0px 1000px #FFFFFF inset !important;
            transition: background-color 5000s ease-in-out 0s;
        }

        /* Number input stepper plus/minus buttons */
        [data-testid="stNumberInput"] button,
        [data-baseweb="input"] button {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
        }

        [data-testid="stNumberInput"] button svg,
        [data-baseweb="input"] button svg {
            fill: #64748B !important;
            stroke: #64748B !important;
            color: #64748B !important;
        }

        /* Input Placeholder styling */
        input::placeholder,
        textarea::placeholder,
        [data-baseweb="input"] input::placeholder,
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stNumberInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: #94A3B8 !important;
            -webkit-text-fill-color: #94A3B8 !important;
            font-weight: 500 !important;
            opacity: 1 !important;
        }

        /* -------------------------------------------------------------------------
           9b. BASEWEB SELECTBOX & MULTISELECT TRIGGER STYLES (LIGHT GREY TEXT)
           ------------------------------------------------------------------------- */
        [data-testid="stSelectbox"] > div > div,
        [data-testid="stMultiSelect"] > div > div,
        [data-baseweb="select"],
        [data-baseweb="select"] > div,
        [data-baseweb="select"] > div > div {
            background-color: #FFFFFF !important;
            background: #FFFFFF !important;
            border: 1.5px solid #CBD5E1 !important;
            border-radius: 10px !important;
            min-height: 42px !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
            transition: all 0.2s ease !important;
        }

        [data-testid="stSelectbox"] > div > div:hover,
        [data-testid="stMultiSelect"] > div > div:hover,
        [data-baseweb="select"]:hover,
        [data-baseweb="select"] > div:hover {
            border-color: #0EA5E9 !important;
            box-shadow: 0 0 0 3px rgba(14, 165, 233, 0.12) !important;
        }

        [data-testid="stSelectbox"] > div > div:focus-within,
        [data-testid="stMultiSelect"] > div > div:focus-within,
        [data-baseweb="select"]:focus-within,
        [data-baseweb="select"] > div:focus-within {
            border-color: #0284C7 !important;
            box-shadow: 0 0 0 3.5px rgba(14, 165, 233, 0.22) !important;
        }

        /* Selectbox value text & inner elements - FORCE LIGHT GREY VISIBILITY */
        [data-baseweb="select"],
        [data-baseweb="select"] *,
        [data-testid="stSelectbox"] div[data-baseweb="select"] *,
        [data-testid="stSelectbox"] [role="combobox"],
        [data-testid="stSelectbox"] [role="combobox"] *,
        [data-baseweb="select"] div[role="combobox"],
        [data-baseweb="select"] div[role="combobox"] div,
        [data-baseweb="select"] div[role="combobox"] span,
        [data-baseweb="select"] [data-testid="stMarkdownContainer"] p,
        [data-baseweb="select"] div[aria-selected="true"],
        [data-baseweb="select"] span:not([data-testid="stMultiSelectTagClose"]),
        [data-baseweb="select"] p,
        [data-baseweb="select"] div {
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-size: 0.92rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        }

        /* Selectbox chevron / dropdown arrow */
        [data-baseweb="select"] svg,
        [data-baseweb="select"] svg path,
        [data-testid="stSelectbox"] svg,
        [data-testid="stSelectbox"] svg path {
            fill: #0284C7 !important;
            stroke: #0284C7 !important;
            color: #0284C7 !important;
            opacity: 1 !important;
        }

        /* -------------------------------------------------------------------------
           9c. BASEWEB DROPDOWN POPOVERS & MENUS (LIGHT SKY BLUE THEME)
           ------------------------------------------------------------------------- */
        [data-baseweb="popover"],
        [data-baseweb="popover"] > div,
        [data-baseweb="menu"],
        [data-baseweb="menu"] > ul,
        ul[role="listbox"],
        div[data-testid="stSelectboxVirtualDropdown"] {
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            border: 1.5px solid #BAE6FD !important;
            border-radius: 12px !important;
            box-shadow: 0 10px 30px -4px rgba(14, 165, 233, 0.18), 0 4px 12px rgba(15, 23, 42, 0.06) !important;
            padding: 0.35rem !important;
            overflow: hidden !important;
        }

        /* List items / Options inside Selectbox & Multiselect */
        li[role="option"],
        [data-baseweb="menu"] li,
        ul[role="listbox"] li {
            background: #FFFFFF !important;
            background-color: #FFFFFF !important;
            color: #64748B !important;
            -webkit-text-fill-color: #64748B !important;
            font-size: 0.88rem !important;
            font-weight: 600 !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            border-radius: 8px !important;
            padding: 0.6rem 0.95rem !important;
            margin: 0.15rem 0 !important;
            transition: all 0.15s ease !important;
            cursor: pointer !important;
            border: 1px solid transparent !important;
        }

        /* Hover & Active Selected state on Dropdown Options (Light Sky Blue) */
        li[role="option"]:hover,
        li[role="option"]:focus,
        li[role="option"][aria-selected="true"],
        [data-baseweb="menu"] li:hover,
        [data-baseweb="menu"] li[aria-selected="true"],
        ul[role="listbox"] li:hover,
        ul[role="listbox"] li[aria-selected="true"] {
            background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%) !important;
            background-color: #E0F2FE !important;
            color: #0284C7 !important;
            -webkit-text-fill-color: #0284C7 !important;
            border-color: #BAE6FD !important;
            font-weight: 700 !important;
        }

        li[role="option"] div,
        li[role="option"] p,
        li[role="option"] span,
        [data-baseweb="menu"] span,
        [data-baseweb="menu"] div,
        ul[role="listbox"] span,
        ul[role="listbox"] div {
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
            font-weight: inherit !important;
        }

        label {
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 0.86rem !important;
        }

        /* -------------------------------------------------------------------------
           10. ENTERPRISE SEGMENTED TABS (PROFESSIONAL THEME BUTTON SHAPES)
           ------------------------------------------------------------------------- */
        .stTabs {
            margin-top: 0.5rem;
            margin-bottom: 1.25rem;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem !important;
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
            padding: 0.45rem 0.55rem !important;
            border-radius: 14px !important;
            margin-bottom: 1.25rem !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.03), inset 0 2px 4px rgba(15, 23, 42, 0.03) !important;
            display: inline-flex !important;
            flex-wrap: wrap !important;
            align-items: center !important;
        }

        .stTabs [data-baseweb="tab-highlight"],
        .stTabs [data-baseweb="tab-border"] {
            display: none !important;
            height: 0 !important;
            visibility: hidden !important;
        }

        .stTabs button[data-baseweb="tab"] {
            background: #FFFFFF !important;
            border-radius: 10px !important;
            padding: 0.6rem 1.25rem !important;
            color: #475569 !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            border: 1px solid #E2E8F0 !important;
            height: auto !important;
            white-space: nowrap !important;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
            cursor: pointer !important;
            display: inline-flex !important;
            align-items: center !important;
            gap: 0.5rem !important;
            box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important;
        }

        .stTabs button[data-baseweb="tab"]:hover {
            color: #0284C7 !important;
            background: #F0F9FF !important;
            border-color: #BAE6FD !important;
            transform: translateY(-1.5px) !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.15) !important;
        }

        .stTabs button[aria-selected="true"] {
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid #0284C7 !important;
            box-shadow: 0 4px 14px -2px rgba(14, 165, 233, 0.42), 0 2px 4px rgba(14, 165, 233, 0.2) !important;
            font-weight: 700 !important;
            transform: translateY(-1.5px) !important;
        }

        .stTabs button[aria-selected="true"]:hover {
            background: linear-gradient(135deg, #38BDF8 0%, #0EA5E9 100%) !important;
            box-shadow: 0 6px 18px -2px rgba(14, 165, 233, 0.5) !important;
        }

        .stTabs button[aria-selected="true"] div,
        .stTabs button[aria-selected="true"] p,
        .stTabs button[aria-selected="true"] span {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        .stTabs button[aria-selected="false"] div,
        .stTabs button[aria-selected="false"] p,
        .stTabs button[aria-selected="false"] span {
            color: #475569 !important;
            font-weight: 600 !important;
        }

        .stTabs [data-baseweb="tab-panel"] {
            padding-top: 0.25rem !important;
        }

        /* -------------------------------------------------------------------------
           11. STANDARDIZED INSIGHT & ALERT CARDS
           ------------------------------------------------------------------------- */
        .insight-card {
            border-radius: 14px;
            padding: 1.15rem 1.35rem;
            display: flex;
            align-items: flex-start;
            gap: 0.85rem;
            margin-bottom: 0.85rem;
        }

        .insight-card-blue, .insight-card-info { background: #F0F9FF; border: 1px solid #BAE6FD; }
        .insight-card-green, .insight-card-success { background: #ECFDF5; border: 1px solid #A7F3D0; }
        .insight-card-amber, .insight-card-warning { background: #FFFBEB; border: 1px solid #FDE68A; }
        .insight-card-red, .insight-card-risk { background: #FEF2F2; border: 1px solid #FECACA; }
        .insight-card-purple { background: #FAF5FF; border: 1px solid #DDD6FE; }

        .insight-card-icon {
            font-size: 1.3rem;
            flex-shrink: 0;
            line-height: 1;
        }

        .insight-card-title {
            font-size: 0.94rem;
            font-weight: 700;
            color: #0F172A !important;
            margin-bottom: 0.25rem;
        }

        .insight-card-body {
            font-size: 0.86rem;
            color: #334155 !important;
            line-height: 1.55;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.28rem 0.75rem;
            border-radius: 6px;
            font-size: 0.76rem;
            font-weight: 700;
        }

        .pill-blue { background: #E0F2FE; color: #0284C7 !important; border: 1px solid #BAE6FD; }
        .pill-green { background: #D1FAE5; color: #065F46 !important; border: 1px solid #A7F3D0; }
        .pill-amber { background: #FEF3C7; color: #92400E !important; border: 1px solid #FDE68A; }
        .pill-red { background: #FEE2E2; color: #991B1B !important; border: 1px solid #FECACA; }
        .pill-purple { background: #F3E8FF; color: #7E22CE !important; border: 1px solid #DDD6FE; }

        .list-clean {
            list-style: none;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .list-clean li {
            display: flex;
            align-items: flex-start;
            gap: 0.55rem;
            font-size: 0.86rem;
            color: #334155 !important;
            line-height: 1.5;
        }

        .list-check {
            color: #10B981 !important;
            font-weight: 800;
            flex-shrink: 0;
        }

        .action-card {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04);
        }

        .action-card-header {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            margin-bottom: 0.45rem;
        }

        .action-card-icon {
            width: 34px;
            height: 34px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1rem;
            flex-shrink: 0;
        }

        .action-card-title {
            font-size: 0.92rem;
            font-weight: 700;
            color: #0F172A !important;
            line-height: 1.3;
        }

        .form-intro-card {
            background: linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%);
            border: 1px solid #BAE6FD;
            border-radius: 14px;
            padding: 1rem 1.25rem;
            margin-bottom: 1.15rem;
            display: flex;
            align-items: center;
            gap: 0.85rem;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.08);
        }

        .form-intro-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
            color: #FFFFFF;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            flex-shrink: 0;
            box-shadow: 0 3px 10px rgba(14, 165, 233, 0.25);
        }

        .form-intro-title {
            font-size: 0.96rem;
            font-weight: 800;
            color: #0F172A !important;
            margin-bottom: 0.15rem;
        }

        .form-intro-body {
            font-size: 0.84rem;
            color: #334155 !important;
            line-height: 1.5;
        }

        .form-section-label {
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #0284C7 !important;
            margin: 0.75rem 0 0.4rem 0;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .form-card-container {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 14px;
            padding: 1.25rem 1.35rem;
            box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04);
            margin-bottom: 1rem;
        }

        /* -------------------------------------------------------------------------
           12. DATA TABLES & EXPANDERS
           ------------------------------------------------------------------------- */
        /* -------------------------------------------------------------------------
           12. DATA TABLES & EXPANDERS (ENTERPRISE FILTER THEME)
           ------------------------------------------------------------------------- */
        [data-testid="stDataFrame"], [data-testid="stTable"] {
            border-radius: 14px;
            overflow: hidden;
            border: 1px solid #E2E8F0;
            background: #FFFFFF;
            margin-bottom: 0.85rem;
        }

        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #BAE6FD !important;
            border-radius: 14px !important;
            overflow: hidden !important;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.07) !important;
            margin-bottom: 1.15rem !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }

        [data-testid="stExpander"]:hover {
            border-color: #38BDF8 !important;
            box-shadow: 0 6px 22px rgba(14, 165, 233, 0.12) !important;
        }

        [data-testid="stExpander"] summary {
            background: linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%) !important;
            padding: 0.9rem 1.25rem !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            color: #0284C7 !important;
            border-bottom: 1px solid #E0F2FE !important;
        }

        [data-testid="stExpander"] summary:hover {
            color: #0369A1 !important;
        }

        [data-testid="stExpander"] summary p,
        [data-testid="stExpander"] summary span {
            font-weight: 700 !important;
            color: #0284C7 !important;
            font-size: 0.95rem !important;
        }

        .filter-header-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            font-size: 0.74rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #0284C7;
            background: #E0F2FE;
            border: 1px solid #BAE6FD;
            padding: 0.22rem 0.65rem;
            border-radius: 6px;
            margin-bottom: 0.45rem;
        }

        /* -------------------------------------------------------------------------
           13. ENTERPRISE DATA TABLE (LIGHT SAAS RISK QUEUE & BENCHMARKS)
           ------------------------------------------------------------------------- */
        .enterprise-table-container,
        .portfolio-table-container {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            overflow-x: auto !important;
            box-shadow: 0 4px 18px -2px rgba(15, 23, 42, 0.04) !important;
            margin-bottom: 1.25rem !important;
        }

        .enterprise-table,
        .portfolio-table {
            width: 100% !important;
            border-collapse: collapse !important;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
            text-align: left !important;
        }

        .enterprise-table thead th,
        .portfolio-table thead th {
            background: #F8FAFC !important;
            color: #475569 !important;
            font-size: 0.76rem !important;
            font-weight: 700 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.03em !important;
            padding: 0.65rem 0.65rem !important;
            border-bottom: 2px solid #E2E8F0 !important;
            white-space: nowrap !important;
        }

        .enterprise-table tbody tr,
        .portfolio-table tbody tr {
            border-bottom: 1px solid #F1F5F9 !important;
            transition: background 0.15s ease !important;
            background: #FFFFFF !important;
        }

        .enterprise-table tbody tr:hover,
        .portfolio-table tbody tr:hover {
            background: #F0F9FF !important;
        }

        .enterprise-table tbody td,
        .portfolio-table tbody td {
            padding: 0.55rem 0.65rem !important;
            font-size: 0.84rem !important;
            color: #1E293B !important;
            vertical-align: middle !important;
            white-space: nowrap !important;
        }

        .portfolio-table .cust-id {
            font-weight: 700;
            color: #0284C7;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.88rem;
        }

        .portfolio-table .cust-name {
            font-weight: 700;
            color: #0F172A;
        }

        .portfolio-table .prob-badge-container {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .portfolio-table .prob-bar-bg {
            width: 65px;
            height: 7px;
            background: #E2E8F0;
            border-radius: 4px;
            overflow: hidden;
            display: inline-block;
        }

        .portfolio-table .prob-bar-fill-high {
            height: 100%;
            background: linear-gradient(90deg, #F87171 0%, #EF4444 100%);
            border-radius: 4px;
        }

        .portfolio-table .prob-bar-fill-med {
            height: 100%;
            background: linear-gradient(90deg, #FCD34D 0%, #F59E0B 100%);
            border-radius: 4px;
        }

        .portfolio-table .prob-bar-fill-low {
            height: 100%;
            background: linear-gradient(90deg, #6EE7B7 0%, #10B981 100%);
            border-radius: 4px;
        }

        /* -------------------------------------------------------------------------
           13b. UNIFIED HERO & STAT RIBBON CONTAINERS
           ------------------------------------------------------------------------- */
        .hero-card {
            background: linear-gradient(135deg, #F0F9FF 0%, #FFFFFF 100%) !important;
            border: 1px solid #BAE6FD !important;
            border-radius: 14px !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 1rem !important;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.08) !important;
            box-sizing: border-box !important;
        }

        .info-banner-card {
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-left: 4px solid #0EA5E9 !important;
            border-radius: 12px !important;
            padding: 0.75rem 1.1rem !important;
            margin-bottom: 0.85rem !important;
            box-sizing: border-box !important;
        }

        .stat-ribbon-container {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)) !important;
            gap: 0.65rem !important;
            margin-bottom: 0.85rem !important;
        }

        .stat-ribbon-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 0.55rem 0.85rem !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
            transition: all 0.2s ease !important;
            box-sizing: border-box !important;
        }

        .stat-ribbon-card:hover {
            border-color: #BAE6FD !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(14, 165, 233, 0.1) !important;
        }

        /* -------------------------------------------------------------------------
           14. STANDOUT CHART & VISUALIZATION CONTAINERS (ZERO SCROLLBARS, 100% RESPONSIVE)
           ------------------------------------------------------------------------- */
        [data-testid="stPlotlyChart"],
        .stPlotlyChart {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 0 !important;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.05) !important;
            margin-bottom: 0.85rem !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            width: 100% !important;
            max-width: 100% !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }

        [data-testid="stPlotlyChart"]:hover,
        .stPlotlyChart:hover {
            border-color: #BAE6FD !important;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.08) !important;
        }

        [data-testid="stPlotlyChart"] > div,
        [data-testid="stPlotlyChart"] iframe,
        .js-plotly-plot,
        .plotly,
        .plot-container,
        .main-svg {
            width: 100% !important;
            max-width: 100% !important;
            border-radius: 14px !important;
            overflow: hidden !important;
            box-sizing: border-box !important;
        }

        div[data-testid="stPyplot"],
        div[data-testid="stVegaEmbed"],
        .chart-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 14px !important;
            padding: 0.65rem 0.85rem !important;
            box-shadow: 0 4px 18px -2px rgba(14, 165, 233, 0.05) !important;
            margin-bottom: 0.85rem !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
            width: 100% !important;
            max-width: 100% !important;
            transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
        }

        div[data-testid="stPyplot"]:hover,
        div[data-testid="stVegaEmbed"]:hover,
        .chart-card:hover {
            border-color: #BAE6FD !important;
            box-shadow: 0 6px 20px rgba(14, 165, 233, 0.08) !important;
        }

        [data-testid="stPlotlyChart"]::-webkit-scrollbar,
        [data-testid="stPlotlyChart"] > div::-webkit-scrollbar,
        .js-plotly-plot::-webkit-scrollbar,
        .plotly::-webkit-scrollbar,
        .plot-container::-webkit-scrollbar {
            display: none !important;
            width: 0 !important;
            height: 0 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
