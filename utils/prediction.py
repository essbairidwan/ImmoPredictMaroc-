"""
utils/prediction.py — Logique de prédiction (couche métier / backend)
=====================================================================
Sépare la logique de prédiction de l'interface (principe SOLID :
séparation des responsabilités). Réutilisable par Streamlit ET l'API.
"""

import pandas as pd
import numpy as np


def construire_features(artifacts: dict, infos: dict) -> pd.DataFrame:
    """
    Construit le DataFrame d'une ligne avec les 14 features attendues,
    dans le bon ordre, à partir d'un dictionnaire de caractéristiques brutes.
    """
    stand_ord = artifacts["standing_order"]
    row = {
        "superficie":             infos["superficie"],
        "nb_chambres":            infos["nb_chambres"],
        "nb_salles_bain":         infos["nb_salles_bain"],
        "etage":                  infos["etage"],
        "standing_num":           stand_ord[infos["standing"]],
        "amenities_score":        int(infos.get("parking", False))
                                  + int(infos.get("ascenseur", False))
                                  + int(infos.get("terrasse", False)),
        "superficie_par_chambre": round(infos["superficie"] / infos["nb_chambres"], 1),
        "ratio_sdb_chambre":      round(infos["nb_salles_bain"] / infos["nb_chambres"], 2),
        "annee":                  infos.get("annee", 2026),
        "mois":                   infos.get("mois", 6),
        "trimestre":              (infos.get("mois", 6) - 1) // 3 + 1,
        "ville":                  infos["ville"],
        "quartier":               infos["quartier"],
        "type_bien":              infos["type_bien"],
    }
    return pd.DataFrame([row])[artifacts["features"]]


def predire(artifacts: dict, infos: dict) -> dict:
    """
    Prédit le prix d'un bien. Renvoie un dictionnaire de résultats :
    prix, prix_m2, intervalle de confiance, score de qualité.
    """
    X = construire_features(artifacts, infos)
    X = artifacts["te"].transform(X)        # TargetEncoder (ville, quartier)
    X = artifacts["oe"].transform(X)        # OrdinalEncoder (type_bien)

    log_prix = artifacts["model"].predict(X)[0]
    prix = float(np.expm1(log_prix))

    # Score de qualité du bien (0-100) basé sur standing + équipements
    score_equip = (int(infos.get("parking", False))
                   + int(infos.get("ascenseur", False))
                   + int(infos.get("terrasse", False)))
    score = min(100, int(
        artifacts["standing_order"][infos["standing"]] * 18
        + score_equip * 8
        + 10
    ))

    return {
        "prix":        prix,
        "prix_m2":     prix / infos["superficie"],
        "ic_bas":      prix * 0.90,
        "ic_haut":     prix * 1.10,
        "score":       score,
        "standing":    infos["standing"],
    }
