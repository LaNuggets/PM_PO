import streamlit as st
import pandas as pd


def filter_by_segment(df: pd.DataFrame, segments: list, segment_column: str = "segment") -> pd.DataFrame:
    """Filtre le DataFrame sur les segments sélectionnés."""
    if not segments or segment_column not in df.columns:
        return df
    return df[df[segment_column].isin(segments)]


def render_filter(df: pd.DataFrame, segment_column: str = "segment") -> pd.DataFrame:
    """Affiche le widget de filtre et retourne le DataFrame filtré."""
    if segment_column not in df.columns:
        st.info("Aucune colonne segment trouvée.")
        return df

    options = sorted(df[segment_column].dropna().unique().tolist())
    selected = st.multiselect("Filtrer par segment", options, default=options)
    return filter_by_segment(df, selected, segment_column)


if __name__ == "__main__":
    st.set_page_config(page_title="US-09 — Filtre segment", layout="wide")
    st.title("US-09 — Filtre par segment")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        filtered = render_filter(df)
        st.write(f"**{len(filtered)} lignes** après filtrage")
        st.dataframe(filtered)
    else:
        st.info("Charge un CSV pour tester le filtre.")
