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
        help=f"Déposez le fichier client (UTF-8, séparateur `,`, max {MAX_FILE_SIZE_MB} Mo).",
    )
    if uploaded is None:
        return None

    try:
        validate_file(uploaded)
    except FileValidationError as error:
        handle_invalid_file(error)
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


REQUIRED_COLUMNS = ("client_id", "segment", "risk_level", "revenue")
VALID_RISK_LEVELS = {"low", "medium", "high", "faible", "moyen", "élevé", "eleve"}


def check_data_quality(df):
    """US-03 — Détecte valeurs manquantes et incohérences, affiche un rapport.

    Retourne un dict `report` pour pouvoir être testé / réutilisé :
    - `missing_columns` : colonnes obligatoires absentes
    - `missing_values` : colonnes → nb de valeurs vides
    - `duplicates` : nb de client_id dupliqués
    - `invalid_revenue` : nb de valeurs revenue non numériques ou <= 0
    - `invalid_risk` : nb de valeurs risk_level hors liste autorisée
    - `severity` : "ok" | "warning" | "error"
    """
    report = {
        "missing_columns": [c for c in REQUIRED_COLUMNS if c not in df.columns],
        "missing_values": {},
        "duplicates": 0,
        "invalid_revenue": 0,
        "invalid_risk": 0,
        "severity": "ok",
    }

    for col in df.columns:
        n_missing = int(df[col].isna().sum())
        if n_missing:
            report["missing_values"][col] = n_missing

    if "client_id" in df.columns:
        report["duplicates"] = int(df["client_id"].duplicated().sum())

    if "revenue" in df.columns:
        numeric = pd.to_numeric(df["revenue"], errors="coerce")
        report["invalid_revenue"] = int(((numeric.isna()) | (numeric <= 0)).sum())

    if "risk_level" in df.columns:
        normalized = df["risk_level"].astype(str).str.lower().str.strip()
        report["invalid_risk"] = int((~normalized.isin(VALID_RISK_LEVELS)).sum())

    if report["missing_columns"] or report["duplicates"]:
        report["severity"] = "error"
    elif report["missing_values"] or report["invalid_revenue"] or report["invalid_risk"]:
        report["severity"] = "warning"

    _render_quality_report(df, report)
    return report


def _render_quality_report(df, report):
    """Affichage Streamlit du rapport qualité (interne à US-03)."""
    severity = report["severity"]
    if severity == "ok":
        st.success("✅ Qualité des données : aucune anomalie détectée.")
        return

    if severity == "error":
        st.error("⛔ Anomalies bloquantes détectées — corrigez le fichier avant exploitation.")
    else:
        st.warning("⚠️ Anomalies non bloquantes — analyse possible mais à surveiller.")

    if report["missing_columns"]:
        st.markdown("**Colonnes obligatoires manquantes :** " + ", ".join(f"`{c}`" for c in report["missing_columns"]))

    summary_rows = []
    if report["missing_values"]:
        for col, n in report["missing_values"].items():
            summary_rows.append({"colonne": col, "type d'anomalie": "valeurs manquantes", "nombre": n})
    if report["duplicates"]:
        summary_rows.append({"colonne": "client_id", "type d'anomalie": "doublons", "nombre": report["duplicates"]})
    if report["invalid_revenue"]:
        summary_rows.append({"colonne": "revenue", "type d'anomalie": "non numérique ou ≤ 0", "nombre": report["invalid_revenue"]})
    if report["invalid_risk"]:
        summary_rows.append({"colonne": "risk_level", "type d'anomalie": "valeur hors référentiel", "nombre": report["invalid_risk"]})

    if summary_rows:
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    with st.expander("Voir les lignes suspectes"):
        mask = pd.Series(False, index=df.index)
        if "client_id" in df.columns:
            mask |= df["client_id"].duplicated(keep=False) | df["client_id"].isna()
        if "revenue" in df.columns:
            numeric = pd.to_numeric(df["revenue"], errors="coerce")
            mask |= numeric.isna() | (numeric <= 0)
        if "risk_level" in df.columns:
            normalized = df["risk_level"].astype(str).str.lower().str.strip()
            mask |= ~normalized.isin(VALID_RISK_LEVELS)
        suspicious = df[mask]
        if suspicious.empty:
            st.caption("Aucune ligne isolable (anomalie au niveau des colonnes globales).")
        else:
            st.dataframe(suspicious, use_container_width=True)


def handle_invalid_file(error):
    """US-04 — Affiche un message d'erreur compréhensible pour un fichier invalide.

    Mappe les exceptions techniques (`pandas`, décodage, I/O) sur un message
    orienté utilisateur, avec une piste de correction.
    """
    error_type = type(error).__name__
    message = str(error).lower()

    if isinstance(error, FileValidationError):
        user_message = str(error)
        hint = f"Fichier attendu : `.csv` UTF-8, taille ≤ {MAX_FILE_SIZE_MB} Mo, au moins une ligne d'en-tête."
    elif isinstance(error, UnicodeDecodeError) or "codec" in message or "decode" in message:
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


MAX_FILE_SIZE_MB = 10
ALLOWED_EXTENSIONS = (".csv",)


class FileValidationError(Exception):
    """Erreur métier levée quand un fichier ne passe pas les contrôles d'import."""


def validate_file(file):
    """US-19 — Contrôle le fichier uploadé avant toute lecture pandas.

    Vérifie : extension, taille, nom (absence de séparateurs chemin), encodage
    UTF-8 sur un échantillon, présence d'au moins une ligne d'en-tête non vide.

    Lève `FileValidationError` avec un message explicite si le fichier est rejeté.
    """
    if file is None:
        raise FileValidationError("Aucun fichier fourni.")

    name = getattr(file, "name", "") or ""
    if "/" in name or "\\" in name:
        raise FileValidationError("Nom de fichier invalide (caractères de chemin interdits).")

    lowered = name.lower()
    if not any(lowered.endswith(ext) for ext in ALLOWED_EXTENSIONS):
        raise FileValidationError(
            f"Extension non autorisée. Extensions acceptées : {', '.join(ALLOWED_EXTENSIONS)}."
        )

    size_bytes = getattr(file, "size", None)
    if size_bytes is None:
        file.seek(0, 2)
        size_bytes = file.tell()
        file.seek(0)
    if size_bytes == 0:
        raise FileValidationError("Le fichier est vide.")
    max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        size_mb = size_bytes / (1024 * 1024)
        raise FileValidationError(
            f"Fichier trop volumineux : {size_mb:.1f} Mo (maximum : {MAX_FILE_SIZE_MB} Mo)."
        )

    head = file.read(4096)
    file.seek(0)
    try:
        decoded = head.decode("utf-8")
    except UnicodeDecodeError as e:
        raise FileValidationError("Encodage non supporté : attendu UTF-8.") from e

    if not decoded.strip():
        raise FileValidationError("Le fichier ne contient pas de ligne d'en-tête exploitable.")

    return {
        "name": name,
        "size_mb": round(size_bytes / (1024 * 1024), 2),
        "encoding": "utf-8",
    }


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

    st.divider()
    st.subheader("Qualité des données")
    check_data_quality(df)
