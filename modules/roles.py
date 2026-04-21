"""
US-18 — Rôles admin / user

En tant qu'administrateur, je veux distinguer au minimum un rôle admin
et un rôle user afin de limiter certaines actions critiques.

Branche : feature/US-18-LaNuggets-roles-admin-user
"""
from functools import wraps
from typing import Callable

import streamlit as st


ROLES = ("admin", "user")

# Actions et rôles autorisés
PERMISSIONS = {
    "view_dashboard": {"admin", "user"},
    "import_csv": {"admin", "user"},
    "delete_data": {"admin"},
    "manage_users": {"admin"},
    "view_audit_log": {"admin"},
}


def has_permission(user: dict, action: str) -> bool:
    """Vérifie si le user peut effectuer l'action."""
    if not user:
        return False
    return user.get("role") in PERMISSIONS.get(action, set())


def require_role(required_role: str):
    """Décorateur pour protéger une fonction Streamlit."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = st.session_state.get("user")
            if not user:
                st.error("Connexion requise.")
                st.stop()
            if user["role"] != required_role:
                st.error(f"Accès refusé. Rôle `{required_role}` requis.")
                st.stop()
            return func(*args, **kwargs)
        return wrapper
    return decorator


@require_role("admin")
def admin_zone() -> None:
    st.success("Bienvenue dans la zone admin.")
    st.write("Fonctionnalités critiques disponibles ici.")


def render(user: dict) -> None:
    st.write(f"Connecté : **{user['username']}** (rôle : `{user['role']}`)")

    st.subheader("Vos permissions")
    for action in PERMISSIONS:
        allowed = has_permission(user, action)
        icon = "✅" if allowed else "🚫"
        st.write(f"{icon} `{action}`")

    st.divider()
    st.subheader("Zone admin (réservée)")
    if user["role"] == "admin":
        admin_zone()
    else:
        st.info("Cette section est réservée aux administrateurs.")


if __name__ == "__main__":
    st.set_page_config(page_title="US-18 — Rôles", layout="wide")
    st.title("US-18 — Rôles admin / user")

    # Mock simple pour tester — à remplacer par la vraie auth US-17
    role = st.sidebar.radio("Simuler un rôle", ROLES)
    st.session_state["user"] = {"username": "demo", "role": role}

    render(st.session_state["user"])
