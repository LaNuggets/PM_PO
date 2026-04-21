import streamlit as st
import pandas as pd


def compute_risk_clients(
    df: pd.DataFrame,
    risk_column: str = "risk_level",
    risk_values: tuple = ("high", "élevé"),
) -> int:
    """Compte les clients considérés à risque."""
    if risk_column not in df.columns:
        return 0
    return int(df[risk_column].isin(risk_values).sum())


def render(df: pd.DataFrame) -> None:
    count = compute_risk_clients(df)
    st.metric(
        label="Clients à risque",
        value=count,
        delta=None,
        help="Clients avec un niveau de risque élevé.",
    )
    if count > 0:
        st.warning(f"⚠️ {count} client(s) nécessitent une attention prioritaire.")


if __name__ == "__main__":
    st.set_page_config(page_title="US-08 — Clients à risque", layout="wide")
    st.title("US-08 — Clients à risque")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir le KPI.")
