"""
Module ingestion — Baptiste (Baptistebdy1)

Couvre : US-01 (upload CSV), US-02 (aperçu), US-03 (qualité), US-04 (erreurs), US-19 (contrôle).
"""
import pandas as pd
import streamlit as st


def upload_csv():
    """US-01 — Upload d'un CSV et stockage dans la session.

    Les erreurs de lecture sont déléguées à `handle_invalid_file` (US-04).
    """
    uploaded = st.file_uploader(
        "Importer un fichier CSV",
        type=["csv"],
        help="Déposez le fichier client (UTF-8, séparateur `,`).",
    )
    if uploaded is None:
        return None

    try:
        df = pd.read_csv(uploaded)
    except Exception as error:
        handle_invalid_file(error)
        return None

    if df.empty:
        handle_invalid_file(ValueError("empty"))
        return None

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
    """US-04 — Affiche un message d'erreur compréhensible pour un fichier invalide.

    Mappe les exceptions techniques (`pandas`, décodage, I/O) sur un message
    orienté utilisateur, avec une piste de correction.
    """
    error_type = type(error).__name__
    message = str(error).lower()

    if isinstance(error, UnicodeDecodeError) or "codec" in message or "decode" in message:
        user_message = "Encodage du fichier non supporté."
        hint = "Ré-enregistrez le fichier en **UTF-8** avant de l'importer."
    elif "empty" in message or "no columns" in message:
        user_message = "Le fichier est vide ou ne contient aucune colonne."
        hint = "Vérifiez que le CSV contient une ligne d'en-tête et au moins une ligne de données."
    elif "tokenizing" in message or "expected" in message or isinstance(error, pd.errors.ParserError):
        user_message = "Format CSV invalide (séparateur ou guillemets incorrects)."
        hint = "Vérifiez que les colonnes sont séparées par `,` et que les guillemets sont bien fermés."
    else:
        user_message = f"Impossible de lire le fichier ({error_type})."
        hint = "Vérifiez l'extension `.csv`, l'encodage UTF-8 et la structure des colonnes."

    st.error(f"❌ {user_message}")
    st.info(f"💡 {hint}")


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
