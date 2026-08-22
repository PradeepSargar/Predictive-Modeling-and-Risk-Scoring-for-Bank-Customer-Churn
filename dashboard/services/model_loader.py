import joblib
from pathlib import Path
from typing import Tuple, Any
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIRECTORY = PROJECT_ROOT / "models"

REQUIRED_FILES = [
    "gradient_boosting_model.pkl",
    "scaler.pkl",
    "label_encoder.pkl",
]


class ModelLoadError(Exception):
    pass


def _verify_models_directory() -> Tuple[bool, str]:
    if not MODELS_DIRECTORY.exists():
        return False, f"Models directory does not exist: {MODELS_DIRECTORY}"
    if not MODELS_DIRECTORY.is_dir():
        return False, f"Models path is not a directory: {MODELS_DIRECTORY}"
    for filename in REQUIRED_FILES:
        fp = MODELS_DIRECTORY / filename
        if not fp.exists():
            return False, f"Required model file missing: {filename}"
        if not fp.is_file():
            return False, f"Model path is not a file: {filename}"
        size = fp.stat().st_size
        if size == 0:
            return False, f"Model file is empty (0 bytes): {filename}"
    return True, "OK"


def _safe_load_pickle(filepath: Path) -> Any:
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    if filepath.stat().st_size == 0:
        raise ValueError(f"File is empty: {filepath}")
    try:
        return joblib.load(filepath)
    except Exception as exc:
        raise RuntimeError(f"Failed to deserialize {filepath.name}: {str(exc)}") from exc


@st.cache_resource(show_spinner=False)
def load_models() -> Tuple[Any, Any, Any]:
    """
    Load and cache production Gradient Boosting model, Scaler, and Label Encoder.
    """
    ok, msg = _verify_models_directory()
    if not ok:
        raise ModelLoadError(msg)

    try:
        gradient_boosting_model = _safe_load_pickle(MODELS_DIRECTORY / "gradient_boosting_model.pkl")
        if gradient_boosting_model is None:
            raise ModelLoadError("gradient_boosting_model.pkl loaded as None")

        scaler = _safe_load_pickle(MODELS_DIRECTORY / "scaler.pkl")
        if scaler is None:
            raise ModelLoadError("scaler.pkl loaded as None")
        if not hasattr(scaler, "transform"):
            raise ModelLoadError("Scaler object missing 'transform' method (invalid scaler)")

        label_encoder = _safe_load_pickle(MODELS_DIRECTORY / "label_encoder.pkl")
        if label_encoder is None:
            raise ModelLoadError("label_encoder.pkl loaded as None")

        return gradient_boosting_model, scaler, label_encoder

    except ModelLoadError:
        raise
    except FileNotFoundError as exc:
        raise ModelLoadError(f"Model file missing: {exc}") from exc
    except Exception as exc:
        raise ModelLoadError(f"Unexpected error loading models: {exc}") from exc
