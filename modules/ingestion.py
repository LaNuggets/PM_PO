"""
Module ingestion — Baptiste (Baptistebdy1)

Couvre : US-01 (upload CSV), US-02 (aperçu), US-03 (qualité), US-04 (erreurs), US-19 (contrôle).
"""
import pandas as pd
import streamlit as st


def upload_csv():
    """US-01 — Upload d'un CSV et stockage dans la session."""
    uploaded = st.file_uploader(
        "Importer un fichier CSV",
        type=["csv"],
        help="Déposez le fichier client (UTF-8, séparateur `,`).",
    )
    if uploaded is None:
        return None

    df = pd.read_csv(uploaded)
    st.session_state["df"] = df
    st.session_state["filename"] = uploaded.name
    return df


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
    """Vue Import & données."""
    st.header("Import & données")

    df = upload_csv()

    if df is not None:
        st.success(
            f"Fichier `{st.session_state.get('filename', '')}` chargé : "
            f"**{len(df)} lignes**, **{df.shape[1]} colonnes**."
        )
    elif "df" in st.session_state:
        st.info(
            f"Fichier courant : `{st.session_state.get('filename', '')}` "
            f"({len(st.session_state['df'])} lignes)."
        )
    else:
        st.info("Aucun fichier chargé. Importez un CSV pour démarrer.")
