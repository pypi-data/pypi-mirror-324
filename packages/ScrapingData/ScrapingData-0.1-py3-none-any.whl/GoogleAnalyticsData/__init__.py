import os
from .GoogleAnalyticsFor3Data import (
    format_report,
    fetch_data_in_segments,
    main
)

# Définition des variables globales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exposition des fonctions du module
__all__ = [
    "format_report",
    "fetch_data_in_segments",
    "main"
]
