"""
Module filtres — Alvin (AlvinDiesel09)

Couvre : US-09 (filtre segment), US-10 (filtre niveau de risque).
"""
import pandas as pd
import streamlit as st


def filter_by_segment(df: pd.DataFrame, segments: list, segment_column: str = "segment") -> pd.DataFrame:
    """US-09 — Filtre le DataFrame sur les segments sélectionnés."""
    if not segments or segment_column not in df.columns:
        return df
    return df[df[segment_column].isin(segments)]


def filter_by_risk(df: pd.DataFrame, risk_levels: list, risk_column: str = "risk_level") -> pd.DataFrame:
    """US-10 — Filtre sur les niveaux de risque sélectionnés."""
    if not risk_levels or risk_column not in df.columns:
        return df
    return df[df[risk_column].isin(risk_levels)]


def render_filter_segment(df: pd.DataFrame, segment_column: str = "segment") -> pd.DataFrame:
    """Widget de filtre par segment. Retourne le DataFrame filtré."""
    if segment_column not in df.columns:
        st.info("Aucune colonne segment trouvée.")
        return df
    options = sorted(df[segment_column].dropna().unique().tolist())
    selected = st.multiselect("Filtrer par segment", options, default=options)
    return filter_by_segment(df, selected, segment_column)


def render_filter_risk(df: pd.DataFrame, risk_column: str = "risk_level") -> pd.DataFrame:
    """Widget de filtre par niveau de risque. Retourne le DataFrame filtré."""
    if risk_column not in df.columns:
        st.info("Aucune colonne niveau de risque trouvée.")
        return df
    options = sorted(df[risk_column].dropna().unique().tolist())
    selected = st.multiselect("Filtrer par niveau de risque", options, default=options)
    return filter_by_risk(df, selected, risk_column)


def render_all(df: pd.DataFrame) -> pd.DataFrame:
    """Affiche tous les filtres côte à côte et enchaîne les filtrages."""
    c1, c2 = st.columns(2)
    with c1:
        df = render_filter_segment(df)
    with c2:
        df = render_filter_risk(df)
    return df
