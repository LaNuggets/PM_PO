"""
Module audit — Aurélien (LaNuggets)

Couvre : US-20 (journal d'audit).

Persistance : data/audit.log.jsonl
"""
import streamlit as st


def log_event(user: str, action: str, details: dict | None = None) -> None:
    """Ajoute une entrée dans le journal d'audit."""
    # TODO(US-20)
    raise NotImplementedError


def render_admin_view() -> None:
    """Vue Admin (placeholder)."""
    st.header("Admin — Journal d'audit")
    st.info("Module en cours de développement (Aurélien).")
