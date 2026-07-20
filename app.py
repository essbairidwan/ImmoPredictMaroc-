"""
====================================================================
  ImmoPredict Maroc — Application d'estimation immobilière par IA
  Point d'entrée principal (navigation + pages)
====================================================================
  Lancement :  streamlit run app.py
  PFE Data Science — Prédiction des prix immobiliers au Maroc
====================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from config import APP_TITLE, APP_ICON, APP_TAGLINE, COLORS, PLOTLY_SEQ
from utils.data_loader import load_data, load_model
from utils.prediction import predire
from utils.visualizations import bar_comparaison

st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON,
                   layout="wide", initial_sidebar_state="expanded")

# ── Styles globaux ───────────────────────────────────────────
st.markdown(f"""
<style>
    .block-container {{ padding-top: 2rem; }}
    .hero {{
        background: linear-gradient(135deg, {COLORS['primary_dk']} 0%, {COLORS['primary']} 100%);
        padding: 2rem 2.5rem; border-radius: 18px; margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(37,99,235,0.25);
    }}
    .hero h1 {{ color: white; margin: 0; font-size: 2.2rem; font-weight: 800; }}
    .hero p  {{ color: #dbeafe; margin: 0.4rem 0 0 0; font-size: 1.05rem; }}
    .kpi-card {{
        background: white; border-radius: 14px; padding: 1.3rem 1.5rem;
        box-shadow: 0 4px 14px rgba(0,0,0,0.07);
        border-top: 4px solid {COLORS['primary']};
    }}
    .kpi-card .kpi-label {{ color: #64748b; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.5px; }}
    .kpi-card .kpi-value {{ color: {COLORS['dark']}; font-size: 1.9rem; font-weight: 800; margin-top: 0.2rem; }}
    .kpi-card .kpi-sub   {{ color: #94a3b8; font-size: 0.8rem; }}
    .price-card {{
        background: linear-gradient(135deg, {COLORS['success']} 0%, #10b981 100%);
        padding: 2rem; border-radius: 16px; text-align: center;
        box-shadow: 0 8px 24px rgba(16,185,129,0.3);
    }}
    .price-card .label {{ color: #d1fae5; font-size: 1rem; }}
    .price-card .value {{ color: white; font-size: 2.6rem; font-weight: 800; }}
    .price-card .sub   {{ color: #a7f3d0; font-size: 0.95rem; margin-top: 0.4rem; }}
    .info-box {{ background: {COLORS['light']}; border-left: 4px solid {COLORS['primary']};
                 padding: 1rem 1.2rem; border-radius: 8px; margin-top: 1rem; }}
</style>
""", unsafe_allow_html=True)

# ── Chargement (cache) ───────────────────────────────────────
df = load_data()
artifacts = load_model()

# ── Sidebar navigation ───────────────────────────────────────
with st.sidebar:
    st.markdown(f"## {APP_ICON} {APP_TITLE}")
    st.caption(APP_TAGLINE)
    st.divider()
    page = st.radio("Navigation",
        ["🏠 Dashboard", "💰 Estimation", "📊 Analyse du marché",
         "🧠 Explainable AI", "🏆 Comparaison modèles",
         "💡 Insights", "🗺️ Carte"],
        label_visibility="collapsed")
    st.divider()
    st.caption(f"📦 {len(df):,} annonces".replace(",", " "))
    st.caption(f"🏙️ {df['ville'].nunique()} villes · {df['quartier'].nunique()} quartiers")


# ═════════════════════════════════════════════════════════════
#  PAGE : DASHBOARD
# ═════════════════════════════════════════════════════════════
def page_dashboard():
    st.markdown("""<div class="hero"><h1>🏠 Tableau de Bord</h1>
    <p>Vue d'ensemble du marché immobilier marocain · 2020–2026</p></div>""",
    unsafe_allow_html=True)

    def kpi(col, label, value, sub=""):
        col.markdown(f"""<div class="kpi-card"><div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>""",
        unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    kpi(c1, "Annonces", f"{len(df):,}".replace(",", " "), "biens analysés")
    kpi(c2, "Prix moyen", f"{df['prix'].mean()/1e6:.2f} M DH",
        f"médian : {df['prix'].median()/1e6:.2f} M DH")
    kpi(c3, "Prix moyen / m²", f"{df['prix_par_m2'].mean():,.0f} DH".replace(",", " "), "toutes villes")
    st.write("")
    c4, c5, c6 = st.columns(3)
    kpi(c4, "Surface moyenne", f"{df['superficie'].mean():.0f} m²",
        f"médiane : {df['superficie'].median():.0f} m²")
    kpi(c5, "Villes", f"{df['ville'].nunique()}", "couvertes")
    kpi(c6, "Quartiers", f"{df['quartier'].nunique()}", "référencés")
    st.divider()

    g1, g2 = st.columns(2)
    with g1:
        st.subheader("💰 Prix médian par ville")
        ppv = df.groupby("ville")["prix"].median().sort_values().reset_index()
        fig = px.bar(ppv, x="prix", y="ville", orientation="h",
                     color="prix", color_continuous_scale="Blues",
                     labels={"prix": "Prix médian (DH)", "ville": ""})
        fig.update_layout(height=350, coloraxis_showscale=False, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)
    with g2:
        st.subheader("🏗️ Répartition par type de bien")
        tb = df["type_bien"].value_counts().reset_index()
        tb.columns = ["type_bien", "count"]
        fig = px.pie(tb, names="type_bien", values="count", hole=0.45,
                     color_discrete_sequence=PLOTLY_SEQ)
        fig.update_layout(height=350, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("📈 Évolution du prix médian au m² (par an)")
    eve = df.groupby("annee")["prix_par_m2"].median().reset_index()
    fig = px.line(eve, x="annee", y="prix_par_m2", markers=True,
                  labels={"prix_par_m2": "Prix médian / m² (DH)", "annee": "Année"})
    fig.update_traces(line_color=COLORS["primary"], line_width=3)
    fig.update_layout(height=320, margin=dict(l=0,r=0,t=10,b=0))
    st.plotly_chart(fig, use_container_width=True)


# ═════════════════════════════════════════════════════════════
#  PAGE : ESTIMATION
# ═════════════════════════════════════════════════════════════
def page_estimation():
    st.markdown("""<div class="hero"><h1>💰 Estimation de Prix</h1>
    <p>Modèle CatBoost (R² = 0.98) · Renseignez les caractéristiques du bien</p></div>""",
    unsafe_allow_html=True)

    VILLES = artifacts["villes"]; TYPES = artifacts["types"]
    STANDINGS = artifacts["standings"]; QPV = artifacts["quartiers_par_ville"]

    colf, colr = st.columns([3, 2])
    with colf:
        st.subheader("📋 Caractéristiques")
        cc1, cc2 = st.columns(2)
        with cc1:
            ville = st.selectbox("Ville", VILLES)
            quartier = st.selectbox("Quartier", QPV[ville])
            type_bien = st.selectbox("Type de bien", TYPES)
            standing = st.select_slider("Standing", options=STANDINGS, value=STANDINGS[1])
        with cc2:
            superficie = st.number_input("Superficie (m²)", 20, 1000, 100, step=5)
            nb_chambres = st.number_input("Chambres", 1, 10, 3)
            nb_salles_bain = st.number_input("Salles de bain", 1, 8, 2)
            etage = st.number_input("Étage", 0, 30, 2)
        st.write("**Équipements**")
        e1, e2, e3 = st.columns(3)
        parking = e1.checkbox("🅿️ Parking", value=True)
        ascenseur = e2.checkbox("🛗 Ascenseur", value=False)
        terrasse = e3.checkbox("🌿 Terrasse", value=True)
        go_btn = st.button("💰 Estimer le prix", type="primary", use_container_width=True)

    with colr:
        if go_btn:
            res = predire(artifacts, {
                "ville": ville, "quartier": quartier, "type_bien": type_bien,
                "standing": standing, "superficie": superficie,
                "nb_chambres": nb_chambres, "nb_salles_bain": nb_salles_bain,
                "etage": etage, "parking": parking, "ascenseur": ascenseur,
                "terrasse": terrasse})
            prix_fmt = "{:,.0f}".format(res["prix"]).replace(",", " ")
            ppm2_fmt = "{:,.0f}".format(res["prix_m2"]).replace(",", " ")
            st.markdown(f"""<div class="price-card"><div class="label">💰 Prix estimé</div>
            <div class="value">{prix_fmt} DH</div>
            <div class="sub">≈ {ppm2_fmt} DH / m²</div></div>""", unsafe_allow_html=True)

            bas = "{:,.0f}".format(res["ic_bas"]).replace(",", " ")
            haut = "{:,.0f}".format(res["ic_haut"]).replace(",", " ")
            st.markdown(f"""<div class="info-box" style="text-align:center;border-left-color:{COLORS['success']};">
            📈 Fourchette estimée (±10 %)<br><b>{bas} – {haut} DH</b></div>""", unsafe_allow_html=True)

            st.write("")
            st.metric("⭐ Score qualité du bien", f"{res['score']}/100")
            st.progress(res["score"] / 100)
        else:
            st.info("👈 Renseignez les caractéristiques puis cliquez **« Estimer le prix »**.")


# ═════════════════════════════════════════════════════════════
#  PAGE : COMPARAISON DES MODELES
# ═════════════════════════════════════════════════════════════
def page_comparaison():
    st.markdown("""<div class="hero"><h1>🏆 Comparaison des Modèles</h1>
    <p>7 algorithmes de Machine Learning & Deep Learning évalués</p></div>""",
    unsafe_allow_html=True)

    # Résultats issus de votre notebook (Section 6)
    results = pd.DataFrame([
        {"name": "CatBoost",          "R2": 0.9794, "MAE": 339565, "RMSE": 681148,  "MAPE": 8.85,  "famille": "Boosting"},
        {"name": "Gradient Boosting", "R2": 0.9773, "MAE": 349583, "RMSE": 716254,  "MAPE": 8.95,  "famille": "Boosting"},
        {"name": "XGBoost",           "R2": 0.9764, "MAE": 352642, "RMSE": 729829,  "MAPE": 8.99,  "famille": "Boosting"},
        {"name": "Random Forest",     "R2": 0.9665, "MAE": 419172, "RMSE": 869612,  "MAPE": 10.60, "famille": "Bagging"},
        {"name": "AdaBoost",          "R2": 0.9550, "MAE": 495183, "RMSE": 1007428, "MAPE": 12.42, "famille": "Boosting"},
        {"name": "MLP (Keras)",       "R2": 0.9377, "MAE": 581486, "RMSE": 1185127, "MAPE": 15.59, "famille": "Deep Learning"},
        {"name": "Ridge Regression",  "R2": 0.8419, "MAE": 736141, "RMSE": 1888162, "MAPE": 18.07, "famille": "Linéaire"},
    ]).sort_values("R2", ascending=False).reset_index(drop=True)

    best = results.iloc[0]
    c1, c2, c3 = st.columns(3)
    c1.metric("🥇 Meilleur modèle", best["name"], f"R² = {best['R2']:.4f}")
    c2.metric("Erreur moyenne (MAE)", f"{best['MAE']:,.0f} DH".replace(",", " "))
    c3.metric("Erreur relative (MAPE)", f"{best['MAPE']:.2f} %")
    st.divider()

    g1, g2 = st.columns(2)
    with g1:
        st.plotly_chart(bar_comparaison(results, "R2", "R² (plus haut = meilleur)",
                        ascending=True, fmt=".4f"), use_container_width=True)
    with g2:
        st.plotly_chart(bar_comparaison(results, "MAE", "MAE en DH (plus bas = meilleur)",
                        ascending=False, fmt=",.0f"), use_container_width=True)

    st.subheader("📋 Tableau détaillé")
    show = results.copy()
    show["R2"]   = show["R2"].map(lambda v: f"{v:.4f}")
    show["MAE"]  = show["MAE"].map(lambda v: f"{v:,.0f} DH".replace(",", " "))
    show["RMSE"] = show["RMSE"].map(lambda v: f"{v:,.0f} DH".replace(",", " "))
    show["MAPE"] = show["MAPE"].map(lambda v: f"{v:.2f} %")
    show.columns = ["Modèle", "R²", "MAE", "RMSE", "MAPE", "Famille"]
    st.dataframe(show, use_container_width=True, hide_index=True)

    st.info("💡 **Analyse** : les modèles de **boosting par arbres** (CatBoost, "
            "Gradient Boosting, XGBoost) dominent avec R² ≈ 0.98. Le réseau de "
            "neurones (MLP, R²=0.94) reste en retrait, confirmant que les arbres "
            "sont mieux adaptés aux **données tabulaires**.")


# ── Pages à venir ────────────────────────────────────────────
def page_a_venir(nom):
    st.markdown(f"""<div class="hero"><h1>{nom}</h1>
    <p>Cette page sera construite à l'étape suivante 🚧</p></div>""", unsafe_allow_html=True)
    st.info("Page en cours de développement.")


# ── Routeur ──────────────────────────────────────────────────
if page == "🏠 Dashboard":          page_dashboard()
elif page == "💰 Estimation":        page_estimation()
elif page == "🏆 Comparaison modèles": page_comparaison()
else:                                page_a_venir(page)
