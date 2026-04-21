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


def compute_total_revenue(df: pd.DataFrame, revenue_column: str = "revenue") -> float:
    """Retourne la somme du chiffre d'affaires."""
    # TODO: adapter le nom de colonne selon le CSV réel
    if revenue_column not in df.columns:
        raise KeyError(f"Colonne '{revenue_column}' absente du CSV.")
    return float(df[revenue_column].sum())


def format_currency(value: float, currency: str = "€") -> str:
    """Formate un montant avec séparateur de milliers."""
    return f"{value:,.0f} {currency}".replace(",", " ")


def render(df: pd.DataFrame) -> None:
    try:
        total = compute_total_revenue(df)
        st.metric(label="Chiffre d'affaires total", value=format_currency(total))
    except KeyError as e:
        st.error(str(e))


if __name__ == "__main__":
    st.set_page_config(page_title="US-05 — Total clients", layout="wide")
    st.title("US-05 — Nombre total de clients")
    st.set_page_config(page_title="US-06 — CA total", layout="wide")
    st.title("US-06 — Chiffre d'affaires total")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir le KPI.")
