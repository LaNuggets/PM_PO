import streamlit as st
import pandas as pd


def filter_by_risk(df: pd.DataFrame, risk_levels: list, risk_column: str = "risk_level") -> pd.DataFrame:
    """Filtre sur les niveaux de risque sélectionnés."""
    if not risk_levels or risk_column not in df.columns:
        return df
    return df[df[risk_column].isin(risk_levels)]


def render_filter(df: pd.DataFrame, risk_column: str = "risk_level") -> pd.DataFrame:
    """Affiche le widget de filtre et retourne le DataFrame filtré."""
    if risk_column not in df.columns:
        st.info("Aucune colonne niveau de risque trouvée.")
        return df

    options = sorted(df[risk_column].dropna().unique().tolist())
    selected = st.multiselect("Filtrer par niveau de risque", options, default=options)
    return filter_by_risk(df, selected, risk_column)


if __name__ == "__main__":
    st.set_page_config(page_title="US-10 — Filtre risque", layout="wide")
    st.title("US-10 — Filtre par niveau de risque")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        filtered = render_filter(df)
        st.write(f"**{len(filtered)} lignes** après filtrage")
        st.dataframe(filtered)
    else:
        st.info("Charge un CSV pour tester le filtre.")
