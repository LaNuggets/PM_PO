"""
Module authentification et rôles — Aurélien (LaNuggets)

Couvre : US-17 (contrôle d'accès), US-18 (rôles admin/user).

Persistance : data/users.json
"""
import streamlit as st


ROLES = ("admin", "user")


def authenticate(username: str, password: str):
    """US-17 : vérifie les credentials."""
    # TODO(US-17)
    raise NotImplementedError


def require_auth():
    """US-17 : bloque l'accès si non authentifié."""
    # TODO(US-17)
    raise NotImplementedError


def has_permission(user: dict, action: str) -> bool:
    """US-18 : vérifie si le rôle du user autorise l'action."""
    # TODO(US-18)
    raise NotImplementedError


def logout() -> None:
    st.session_state.pop("user", None)
