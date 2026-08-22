# =============================================================================
# DATA LOADER (Wrapper around DataService)
# =============================================================================

from services.data_service import DataService


def load_dataset():
    """
    Load the cached European Bank dataset.
    """
    return DataService.load_dataset()