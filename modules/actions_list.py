import json
from pathlib import Path

import pandas as pd
import streamlit as st


ACTIONS_FILE = Path("data/actions.json")


def load_actions_as_df() -> pd.DataFrame:
    if not ACTIONS_FILE.exists():
        return pd.DataFrame()
    data = json.loads(ACTIONS_FILE.read_text(encoding="utf-8"))
    return pd.DataFrame(data)


def render() -> None:
    df = load_actions_as_df()
    if df.empty:
        st.info("Aucune action enregistrée. Crée d'abord une action (US-14).")
        return

    st.subheader("Liste des actions")

    col1, col2 = st.columns(2)
    statuses = sorted(df["status"].dropna().unique().tolist())
    status_filter = col1.multiselect("Statut", statuses, default=statuses)

    search = col2.text_input("Rechercher (titre ou client)")

    filtered = df[df["status"].isin(status_filter)]
    if search:
        mask = (
            filtered["title"].str.contains(search, case=False, na=False)
            | filtered["client_id"].astype(str).str.contains(search, case=False, na=False)
        )
        filtered = filtered[mask]

    st.write(f"**{len(filtered)} action(s)** affichée(s)")
    st.dataframe(
        filtered[["id", "title", "client_id", "owner", "deadline", "status"]],
        use_container_width=True,
    )


if __name__ == "__main__":
    st.set_page_config(page_title="US-16 — Liste des actions", layout="wide")
    st.title("US-16 — Liste des actions")
    render()
