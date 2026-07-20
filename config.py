"""
config.py — Configuration centrale de l'application
====================================================
Regroupe tous les chemins, couleurs et constantes au même endroit.
Principe SOLID : une seule source de vérité pour la configuration.
"""

from pathlib import Path

# ── Chemins ──────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent
DATA_PATH  = BASE_DIR / "data" / "data_national_immobilier.csv"
MODEL_PATH = BASE_DIR / "models" / "immo_artifacts.pkl"

# ── Palette de couleurs (bleu professionnel) ─────────────────
COLORS = {
    "primary":    "#2563eb",   # bleu principal
    "primary_dk": "#1e3a8a",   # bleu foncé
    "success":    "#059669",   # vert
    "accent":     "#7c3aed",   # violet
    "warning":    "#f59e0b",   # orange
    "danger":     "#dc2626",   # rouge
    "light":      "#f1f5f9",   # gris clair
    "dark":       "#0f172a",   # gris foncé
}

# Séquence de couleurs pour les graphiques Plotly
PLOTLY_SEQ = ["#2563eb", "#059669", "#7c3aed", "#f59e0b",
              "#dc2626", "#0891b2", "#db2777", "#65a30d"]

# ── Coordonnées GPS des villes (pour la carte) ───────────────
VILLES_COORDS = {
    "Casablanca": {"lat": 33.5731, "lon": -7.5898},
    "Rabat":      {"lat": 34.0209, "lon": -6.8416},
    "Marrakech":  {"lat": 31.6295, "lon": -7.9811},
    "Fes":        {"lat": 34.0181, "lon": -5.0078},
    "Tanger":     {"lat": 35.7595, "lon": -5.8340},
    "Agadir":     {"lat": 30.4278, "lon": -9.5981},
}

# ── Métadonnées de l'application ─────────────────────────────
APP_TITLE   = "ImmoPredict Maroc"
APP_ICON    = "🏠"
APP_TAGLINE = "Estimation immobilière par Intelligence Artificielle"
