import streamlit as st
import pandas as pd


def compute_total_clients(df: pd.DataFrame, client_column: str = "client_id") -> int:
    """Retourne le nombre de clients uniques."""
    # TODO: adapter le nom de la colonne selon le CSV fourni par le PO
    if client_column in df.columns:
        return df[client_column].nunique()
    return len(df)


def render(df: pd.DataFrame) -> None:
    """Affiche le KPI dans Streamlit."""
    total = compute_total_clients(df)
    st.metric(label="Nombre total de clients", value=f"{total:,}")


if __name__ == "__main__":
    st.set_page_config(page_title="US-05 — Total clients", layout="wide")
    st.title("US-05 — Nombre total de clients")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir le KPI.")