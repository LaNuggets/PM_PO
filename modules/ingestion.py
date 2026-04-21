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
    """US-02 — Aperçu tabulaire du DataFrame chargé.

    Affiche les métadonnées (dimensions, types), un aperçu des premières
    lignes et un extrait configurable par l'utilisateur.
    """
    if df is None or df.empty:
        st.info("Aucune donnée à afficher.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Lignes", len(df))
    c2.metric("Colonnes", df.shape[1])
    c3.metric("Cellules vides", int(df.isna().sum().sum()))

    tab_preview, tab_schema = st.tabs(["Aperçu", "Schéma"])

    with tab_preview:
        n = st.slider("Nombre de lignes à afficher", 5, min(100, len(df)), 10)
        st.dataframe(df.head(n), use_container_width=True)

    with tab_schema:
        schema = pd.DataFrame(
            {
                "colonne": df.columns,
                "type": [str(t) for t in df.dtypes],
                "valeurs uniques": [df[c].nunique(dropna=True) for c in df.columns],
                "valeurs manquantes": [int(df[c].isna().sum()) for c in df.columns],
            }
        )
        st.dataframe(schema, use_container_width=True, hide_index=True)


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
    if df is None:
        df = st.session_state.get("df")

    if df is None:
        st.info("Aucun fichier chargé. Importez un CSV pour démarrer.")
        return

    st.success(
        f"Fichier `{st.session_state.get('filename', '')}` chargé : "
        f"**{len(df)} lignes**, **{df.shape[1]} colonnes**."
    )
    st.divider()
    st.subheader("Aperçu des données")
    preview_data(df)
