"""
Module KPIs — Alvin (AlvinDiesel09)

Couvre : US-05 (total clients), US-06 (CA total), US-07 (segments), US-08 (clients à risque).

Hotfix : restaure US-05/06/07 supprimées lors des merges #30 et #32, et ajoute
`render_all(df)` attendu par `app.py`.
"""
import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------------------------
# Compute
# ---------------------------------------------------------------------------

def compute_total_clients(df: pd.DataFrame, client_column: str = "client_id") -> int:
    """US-05 — Nombre de clients uniques."""
    if client_column in df.columns:
        return int(df[client_column].nunique())
    return len(df)


def compute_total_revenue(df: pd.DataFrame, revenue_column: str = "revenue") -> float:
    """US-06 — Somme du chiffre d'affaires."""
    if revenue_column not in df.columns:
        return 0.0
    numeric = pd.to_numeric(df[revenue_column], errors="coerce")
    return float(numeric.sum(skipna=True))


def format_currency(value: float, currency: str = "€") -> str:
    return f"{value:,.0f} {currency}".replace(",", " ")


def compute_segment_distribution(df: pd.DataFrame, segment_column: str = "segment") -> pd.DataFrame:
    """US-07 — Répartition segment → count."""
    if segment_column not in df.columns:
        return pd.DataFrame(columns=[segment_column, "count"])
    return (
        df[segment_column]
        .value_counts(dropna=False)
        .rename_axis(segment_column)
        .reset_index(name="count")
    )


def compute_risk_clients(
    df: pd.DataFrame,
    risk_column: str = "risk_level",
    risk_values: tuple = ("high", "élevé"),
) -> int:
    """US-08 — Nombre de clients considérés à risque."""
    if risk_column not in df.columns:
        return 0
    return int(df[risk_column].isin(risk_values).sum())


# ---------------------------------------------------------------------------
# Render (Streamlit)
# ---------------------------------------------------------------------------

def render_total_clients(df: pd.DataFrame) -> None:
    total = compute_total_clients(df)
    st.metric(label="Nombre total de clients", value=f"{total:,}".replace(",", " "))


def render_total_revenue(df: pd.DataFrame) -> None:
    total = compute_total_revenue(df)
    st.metric(label="Chiffre d'affaires total", value=format_currency(total))


def render_risk_clients(df: pd.DataFrame) -> None:
    count = compute_risk_clients(df)
    st.metric(
        label="Clients à risque",
        value=count,
        help="Clients avec un niveau de risque élevé.",
    )
    if count > 0:
        st.warning(f"⚠️ {count} client(s) nécessitent une attention prioritaire.")


def render_segment_distribution(df: pd.DataFrame) -> None:
    dist = compute_segment_distribution(df)
    if dist.empty:
        st.info("Colonne `segment` absente — répartition non disponible.")
        return
    fig = px.pie(dist, names=dist.columns[0], values="count", title="Répartition par segment")
    st.plotly_chart(fig, use_container_width=True)


def render_all(df: pd.DataFrame) -> None:
    """Vue Dashboard : tous les KPIs + visualisations."""
    c1, c2, c3 = st.columns(3)
    with c1:
        render_total_clients(df)
    with c2:
        render_total_revenue(df)
    with c3:
        render_risk_clients(df)

    st.divider()
    render_segment_distribution(df)
