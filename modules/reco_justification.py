import streamlit as st
import pandas as pd


def build_justification(client: pd.Series) -> str:
    """Produit une courte explication basée sur les données du client."""
    reasons = []

    risk = str(client.get("risk_level", "")).lower()
    revenue = float(client.get("revenue", 0) or 0)

    if risk in ("high", "élevé"):
        reasons.append("niveau de risque élevé")
    if revenue > 10000:
        reasons.append(f"chiffre d'affaires significatif ({revenue:,.0f} €)")
    elif revenue < 1000:
        reasons.append("faible chiffre d'affaires")

    if not reasons:
        return "Profil neutre : pas de facteur déclencheur identifié."
    return "Recommandation basée sur : " + ", ".join(reasons) + "."


def render(df: pd.DataFrame) -> None:
    client_id = st.selectbox("Choisir un client", df.index)
    client = df.loc[client_id]

    st.write("**Données client :**")
    st.write(client)

    st.info(build_justification(client))


if __name__ == "__main__":
    st.set_page_config(page_title="US-13 — Justification", layout="wide")
    st.title("US-13 — Justification des recommandations")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir les justifications.")
