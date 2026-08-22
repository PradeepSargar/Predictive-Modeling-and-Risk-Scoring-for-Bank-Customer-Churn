import streamlit as st
import time
import uuid
from typing import Any, Callable, Optional, Tuple


def init_session_state_defaults():
    defaults = {
        "scenario_run_count": 0,
        "last_error": None,
        "model_health": "UNKNOWN",
        "simulator_baseline_params": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def render_toast(message: str, variant: str = "info", duration: float = 2.5):
    try:
        icon = {
            "info": "ℹ️",
            "success": "✅",
            "warning": "⚠️",
            "error": "❌",
        }.get(variant, "ℹ️")
        st.toast(f"{icon} {message}", icon=None)
    except Exception:
        pass


def safe_execute(
    func: Callable,
    *args,
    fallback_value: Any = None,
    error_message: str = "Operation failed",
    show_error: bool = True,
    log_error: bool = True,
    **kwargs,
) -> Tuple[bool, Any, Optional[str]]:
    try:
        result = func(*args, **kwargs)
        return True, result, None
    except Exception as exc:
        err_detail = f"{error_message}: {str(exc)}"
        if log_error:
            st.session_state["last_error"] = err_detail
            st.session_state["last_error_time"] = time.time()
        if show_error:
            try:
                st.error(err_detail)
            except Exception:
                pass
        return False, fallback_value, err_detail


def spinner_while(func: Callable, message: str = "Processing...", *args, **kwargs):
    with st.spinner(message):
        return func(*args, **kwargs)


def generate_component_id(prefix: str = "comp") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * clamp(t, 0.0, 1.0)


def format_currency(value: float, symbol: str = "$") -> str:
    try:
        value = float(value)
        if abs(value) >= 1_000_000:
            return f"{symbol}{value / 1_000_000:.2f}M"
        if abs(value) >= 1_000:
            return f"{symbol}{value:,.0f}"
        return f"{symbol}{value:.2f}"
    except (TypeError, ValueError):
        return f"{symbol}0"


def format_percent(value: float, decimals: int = 1) -> str:
    try:
        value = float(value)
        return f"{value * 100:.{decimals}f}%"
    except (TypeError, ValueError):
        return "0%"


def format_delta(delta_abs: float, delta_pct: Optional[float] = None) -> str:
    try:
        da = float(delta_abs) * 100
        arrow = "▼" if da < -0.05 else ("▲" if da > 0.05 else "—")
        base = f"{arrow} {da:+.1f}pp"
        if delta_pct is not None:
            dp = float(delta_pct)
            base += f" ({dp:+.1f}%)"
        return base
    except (TypeError, ValueError):
        return "—"


def compute_safe_delta(baseline: float, scenario: float) -> Tuple[float, float]:
    """Calculate absolute and relative delta between baseline and scenario probabilities."""
    try:
        b = float(baseline)
        s = float(scenario)
        delta_abs = s - b
        delta_pct = ((s - b) / b * 100.0) if b > 0.0001 else 0.0
        return delta_abs, delta_pct
    except Exception:
        return 0.0, 0.0


def get_tier_from_probability(p: float) -> Tuple[str, str, str]:
    from utils.constants import (
        LOW_RISK_THRESHOLD,
        MEDIUM_RISK_THRESHOLD,
        LOW_RISK,
        MEDIUM_RISK,
        HIGH_RISK,
    )
    if p < LOW_RISK_THRESHOLD:
        return LOW_RISK, "green", "🟢"
    if p < MEDIUM_RISK_THRESHOLD:
        return MEDIUM_RISK, "amber", "🟡"
    return HIGH_RISK, "red", "🔴"


def render_error_banner(title: str, detail: str, suggestion: Optional[str] = None):
    suggestion_html = ""
    if suggestion:
        suggestion_html = f'<div style="font-size:0.84rem; color:#B91C1C; margin-top:0.45rem;">💡 {suggestion}</div>'
    st.markdown(
        f"""
        <div style="
            padding:1.1rem 1.35rem;
            background:linear-gradient(135deg, #FEF2F2 0%, #FFFFFF 100%);
            border:1px solid #FECACA;
            border-radius:14px;
            margin-bottom:1rem;
        ">
            <div style="display:flex; align-items:flex-start; gap:0.85rem;">
                <div style="width:40px; height:40px; border-radius:11px;
                    background:linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
                    color:#FFFFFF; display:flex; align-items:center; justify-content:center;
                    font-size:1.1rem; flex-shrink:0;">⛔</div>
                <div style="flex:1;">
                    <div style="font-weight:800; font-size:1rem; color:#7F1D1D; margin-bottom:0.2rem;">{title}</div>
                    <div style="font-size:0.88rem; color:#991B1B;">{detail}</div>
                    {suggestion_html}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_success_banner(title: str, detail: str):
    st.markdown(
        f"""
        <div style="
            padding:1rem 1.3rem;
            background:linear-gradient(135deg, #ECFDF5 0%, #FFFFFF 100%);
            border:1px solid #A7F3D0;
            border-radius:14px;
            margin-bottom:1rem;
        ">
            <div style="display:flex; align-items:center; gap:0.75rem;">
                <div style="width:38px; height:38px; border-radius:11px;
                    background:linear-gradient(135deg, #059669 0%, #10B981 100%);
                    color:#FFFFFF; display:flex; align-items:center; justify-content:center;
                    font-size:1.05rem; flex-shrink:0;">✓</div>
                <div>
                    <div style="font-weight:700; font-size:0.96rem; color:#064E3B;">{title}</div>
                    <div style="font-size:0.84rem; color:#047857;">{detail}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
