"""
Module recommandations — Cléo (dcleooo)

Couvre : US-11 (reco auto), US-12 (catégorisation), US-13 (justification).
"""
import streamlit as st


def generate_recommendation(client):
    """US-11."""
    # TODO(US-11)
    raise NotImplementedError


def categorize_client(client):
    """US-12 : relancer / fidéliser / surveiller."""
    # TODO(US-12)
    raise NotImplementedError


def build_justification(client):
    """US-13."""
    # TODO(US-13)
    raise NotImplementedError


def render(df) -> None:
    """Vue Recommandations (placeholder)."""
    st.header("Recommandations")
    st.info("Module en cours de développement (Cléo).")
