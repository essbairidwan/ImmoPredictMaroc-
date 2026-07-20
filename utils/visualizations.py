"""
utils/visualizations.py — Fonctions de visualisation Plotly réutilisables
=========================================================================
Centralise la création des graphiques (principe DRY : ne pas se répéter).
"""

import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from config import COLORS, PLOTLY_SEQ


def bar_comparaison(df_results, metric, titre, ascending=True, fmt=".4f"):
    """Barre horizontale comparant les modèles sur une métrique donnée."""
    d = df_results.sort_values(metric, ascending=ascending)
    # Le meilleur (en haut) est mis en vert
    colors = [COLORS["success"] if i == len(d) - 1 else COLORS["primary"]
              for i in range(len(d))]
    fig = go.Figure(go.Bar(
        x=d[metric], y=d["name"], orientation="h",
        marker_color=colors,
        text=[f"{v:{fmt}}" for v in d[metric]],
        textposition="outside",
    ))
    fig.update_layout(title=titre, height=380,
                      margin=dict(l=0, r=20, t=40, b=0),
                      xaxis_title=metric, yaxis_title="")
    return fig
