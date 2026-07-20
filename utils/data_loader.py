"""
utils/data_loader.py — Chargement des données et du modèle
==========================================================
Centralise le chargement (avec cache Streamlit) du dataset et des
artefacts du modèle. Gère les erreurs de fichiers manquants.
"""

import streamlit as st
import pandas as pd
import joblib
import sys
from pathlib import Path

# Permet d'importer config depuis le dossier parent
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_PATH, MODEL_PATH


@st.cache_data(show_spinner="Chargement des données…")
def load_data() -> pd.DataFrame:
    """Charge le dataset immobilier nettoyé. Retourne un DataFrame."""
    if not DATA_PATH.exists():
        st.error(f"❌ Dataset introuvable : {DATA_PATH}\n\n"
                 "Placez 'data_national_immobilier.csv' dans le dossier data/.")
        st.stop()
    df = pd.read_csv(DATA_PATH, parse_dates=["date_publication"])
    return df


@st.cache_resource(show_spinner="Chargement du modèle…")
def load_model():
    """Charge les artefacts du modèle (modèle + encodeurs). Retourne un dict."""
    if not MODEL_PATH.exists():
        st.error(f"❌ Modèle introuvable : {MODEL_PATH}\n\n"
                 "Placez 'immo_artifacts.pkl' dans le dossier models/.")
        st.stop()
    return joblib.load(MODEL_PATH)
