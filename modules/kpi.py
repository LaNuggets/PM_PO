import streamlit as st
import pandas as pd
import plotly.express as px


def compute_segment_distribution(df: pd.DataFrame, segment_column: str = "segment") -> pd.DataFrame:
    """Retourne un DataFrame segment -> count."""
    # TODO: adapter le nom de colonne
    if segment_column not in df.columns:
        raise KeyError(f"Colonne '{segment_column}' absente.")
    return (
        df[segment_column]
        .value_counts()
        .reset_index()
        .rename(columns={"index": segment_column, segment_column: "count"})
    )


def render(df: pd.DataFrame) -> None:
    try:
        dist = compute_segment_distribution(df)
        fig = px.pie(dist, names=dist.columns[0], values="count", title="Répartition par segment")
        st.plotly_chart(fig, use_container_width=True)
    except KeyError as e:
        st.error(str(e))


if __name__ == "__main__":
    st.set_page_config(page_title="US-07 — Segments", layout="wide")
    st.title("US-07 — Répartition par segment")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir le graphique.")