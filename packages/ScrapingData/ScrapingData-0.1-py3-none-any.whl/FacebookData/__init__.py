import os
from .Facebook import (
    fetch_day_metrics,
    fetch_lifetime_metrics,
    fetch_posts,
    generate_page_insights_csv,
    generate_post_csv,
    generate_fans_csv,
    main
)

# Définition des variables globales
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Exposition des fonctions du module
__all__ = [
    "fetch_day_metrics",
    "fetch_lifetime_metrics",
    "fetch_posts",
    "generate_page_insights_csv",
    "generate_post_csv",
    "generate_fans_csv",
    "main"
]
