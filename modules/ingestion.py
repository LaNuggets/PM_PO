"""
Module ingestion — Baptiste (Baptistebdy1)

Couvre : US-01 (upload CSV), US-02 (aperçu), US-03 (qualité), US-04 (erreurs), US-19 (contrôle).
"""
import streamlit as st


def upload_csv():
    """US-01 — Upload CSV."""
    # TODO(US-01): implémenter l'upload + validation + stockage dans st.session_state["df"]
    raise NotImplementedError


def preview_data(df):
    """US-02 — Aperçu tabulaire."""
    # TODO(US-02)
    raise NotImplementedError


def check_data_quality(df):
    """US-03 — Valeurs manquantes / incohérentes."""
    # TODO(US-03)
    raise NotImplementedError


def handle_invalid_file(error):
    """US-04 — Message d'erreur clair."""
    # TODO(US-04)
    raise NotImplementedError


def validate_file(file):
    """US-19 — Contrôle taille, extension, encodage."""
    # TODO(US-19)
    raise NotImplementedError


def render() -> None:
    """Vue Import & données (placeholder)."""
    st.header("Import & données")
    st.info("Module en cours de développement (Baptiste).")
    # TODO: appeler upload_csv(), preview_data(), check_data_quality()
