# =============================================================================
# EXPLAINABILITY SERVICE
# =============================================================================

"""
Reusable service for loading explainability artifacts.
"""

# =============================================================================
# Import Required Libraries
# =============================================================================

import joblib
from pathlib import Path

# =============================================================================
# Project Paths
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIRECTORY = PROJECT_ROOT / "models"

# =============================================================================
# Explainability Service
# =============================================================================

class ExplainabilityService:

    # ============================================================
    # Load SHAP Explainer
    # ============================================================

    @staticmethod
    def load_explainer():

        return joblib.load(

            MODELS_DIRECTORY / "shap_explainer.pkl"

        )

    # ============================================================
    # Load SHAP Values
    # ============================================================

    @staticmethod
    def load_shap_values():

        return joblib.load(

            MODELS_DIRECTORY / "shap_values.pkl"

        )

    # ============================================================
    # Load Feature Importance
    # ============================================================

    @staticmethod
    def load_feature_importance():

        return joblib.load(

            MODELS_DIRECTORY / "feature_importance.pkl"

        )

    # ============================================================
    # Load Feature Names
    # ============================================================

    @staticmethod
    def load_feature_names():

        return joblib.load(

            MODELS_DIRECTORY / "feature_names.pkl"

        )

    # ============================================================
    # Load X Test Dataset
    # ============================================================

    @staticmethod
    def load_x_test():

        return joblib.load(

            MODELS_DIRECTORY / "X_test.pkl"

        )