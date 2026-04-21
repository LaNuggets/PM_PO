"""
Module actions — Cléo (dcleooo)

Couvre : US-14 (créer action), US-15 (statut), US-16 (liste).

Persistance : data/actions.json
"""
import streamlit as st


def create_action(title, client_id, deadline, owner, recommendation=""):
    """US-14."""
    # TODO(US-14)
    raise NotImplementedError


def update_status(action_id, new_status):
    """US-15."""
    # TODO(US-15)
    raise NotImplementedError


def render() -> None:
    """Vue Actions (placeholder)."""
    st.header("Actions")
    st.info("Module en cours de développement (Cléo).")
    # TODO(US-14, 15, 16): formulaire création + liste avec filtres
