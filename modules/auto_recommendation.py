"""
US-11 — Recommandation automatique

En tant que manager, je veux obtenir une recommandation automatique
pour chaque client à risque afin de décider plus vite d'une action pertinente.

Branche : feature/US-11-dcleooo-auto-recommendation
"""
import streamlit as st
import pandas as pd


def generate_recommendation(client: pd.Series) -> str:
    """Retourne la reco pour un client (basique, à enrichir)."""
    # TODO: affiner la logique selon les colonnes réelles du CSV
    risk = str(client.get("risk_level", "")).lower()
    revenue = float(client.get("revenue", 0) or 0)

    if risk in ("high", "élevé"):
        if revenue > 10000:
            return "Contact commercial prioritaire — client à forte valeur"
        return "Appel de suivi + proposition d'offre de rétention"
    if risk in ("medium", "moyen"):
        return "Surveiller l'activité + email personnalisé"
    return "Aucune action immédiate requise"


def add_recommendations(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute une colonne 'recommendation' au DataFrame."""
    df = df.copy()
    df["recommendation"] = df.apply(generate_recommendation, axis=1)
    return df


def render(df: pd.DataFrame) -> None:
    recos = add_recommendations(df)
    st.subheader("Recommandations par client")
    st.dataframe(recos)


if __name__ == "__main__":
    st.set_page_config(page_title="US-11 — Recommandations", layout="wide")
    st.title("US-11 — Recommandations automatiques")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir les recommandations.")
