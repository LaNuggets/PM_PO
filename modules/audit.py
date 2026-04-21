from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st


LOG_FILE = Path("data/audit.log.jsonl")


def log_event(user: str, action: str, details: dict | None = None) -> None:
    """Ajoute une entrée dans le journal d'audit (JSONL)."""
    entry = {
        "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
        "user": user,
        "action": action,
        "details": details or {},
    }
    LOG_FILE.parent.mkdir(exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_log() -> pd.DataFrame:
    if not LOG_FILE.exists():
        return pd.DataFrame(columns=["timestamp", "user", "action", "details"])
    rows = [json.loads(line) for line in LOG_FILE.read_text(encoding="utf-8").splitlines() if line.strip()]
    return pd.DataFrame(rows)


def render_admin_view() -> None:
    st.subheader("Journal d'audit (admin uniquement)")
    df = read_log()
    if df.empty:
        st.info("Aucun événement journalisé.")
        return

    col1, col2 = st.columns(2)
    users = sorted(df["user"].dropna().unique().tolist())
    user_filter = col1.multiselect("Utilisateur", users, default=users)
    actions = sorted(df["action"].dropna().unique().tolist())
    action_filter = col2.multiselect("Action", actions, default=actions)

    mask = df["user"].isin(user_filter) & df["action"].isin(action_filter)
    st.dataframe(df[mask].sort_values("timestamp", ascending=False), use_container_width=True)


if __name__ == "__main__":
    st.set_page_config(page_title="US-20 — Audit", layout="wide")
    st.title("US-20 — Journal d'audit")

    # Démo : ajouter un événement
    with st.form("demo_event"):
        st.write("Ajouter un événement test")
        user = st.text_input("User", value="demo")
        action = st.selectbox("Action", ["login", "import_csv", "create_action", "delete_data"])
        if st.form_submit_button("Logger"):
            log_event(user, action, {"source": "demo"})
            st.success("Événement journalisé.")

    st.divider()
    render_admin_view()