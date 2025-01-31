import os
from .Linkedin import (
    get_statistics_for_day,
    main
)

# Définition des variables globales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exposition des fonctions du module
__all__ = [
    "get_statistics_for_day",
    "main"
]
