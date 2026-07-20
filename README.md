# 🏠 ImmoPredict Maroc — Étape A (Base + Dashboard)

Application web professionnelle d'estimation immobilière par IA.
**PFE Data Science** — Prédiction des prix immobiliers au Maroc.

---

## 📁 Structure du projet

```
project/
├── app.py                 ← point d'entrée + navigation + Dashboard
├── config.py              ← chemins, couleurs, coordonnées GPS
├── requirements.txt       ← dépendances
│
├── models/
│   └── immo_artifacts.pkl ← modèle + encodeurs (depuis Colab)
│
├── data/
│   └── data_national_immobilier.csv  ← dataset (depuis Colab)
│
└── utils/
    ├── __init__.py
    ├── data_loader.py     ← chargement données + modèle (caché)
    └── prediction.py      ← logique de prédiction (backend réutilisable)
```

> Les dossiers `pages/` (une page par fichier) seront ajoutés aux étapes suivantes.

---

## ⚙️ Installation

1. Placez vos 2 fichiers générés depuis Colab :
   - `immo_artifacts.pkl` → dans `models/`
   - `data_national_immobilier.csv` → dans `data/`

2. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

3. Lancez l'application :
   ```bash
   streamlit run app.py
   ```

---

## ✅ État d'avancement

| Page | Statut |
|---|---|
| 🏠 Dashboard | ✅ Fait (KPI + graphiques Plotly) |
| 💰 Estimation | ✅ Fait (estimation + score qualité) |
| 📊 Analyse du marché | 🚧 Étape C |
| 🧠 Explainable AI (SHAP) | 🚧 Étape D |
| 🏆 Comparaison modèles | ✅ Fait (7 modèles + graphiques) |
| 💡 Insights | 🚧 Étape F |
| 🗺️ Carte interactive | 🚧 Étape G |

---

## 🏗️ Choix d'architecture

- **Séparation des responsabilités** : `config` (constantes), `utils`
  (logique métier), `app` (interface) — conforme aux principes SOLID.
- **Cache Streamlit** : `@st.cache_data` et `@st.cache_resource` évitent de
  recharger les données et le modèle à chaque interaction → performances.
- **Backend réutilisable** : `utils/prediction.py` ne dépend pas de Streamlit,
  il pourra alimenter directement l'**API FastAPI** (étape J).
