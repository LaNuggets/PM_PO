import hashlib
from pathlib import Path
import json

import streamlit as st


USERS_FILE = Path("data/users.json")


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> dict:
    if not USERS_FILE.exists():
        # Comptes par défaut pour dev
        default = {
            "admin": {"password": hash_password("admin123"), "role": "admin"},
            "user": {"password": hash_password("user123"), "role": "user"},
        }
        USERS_FILE.parent.mkdir(exist_ok=True)
        USERS_FILE.write_text(json.dumps(default, indent=2), encoding="utf-8")
        return default
    return json.loads(USERS_FILE.read_text(encoding="utf-8"))


def authenticate(username: str, password: str) -> dict | None:
    """Retourne le user si credentials OK, sinon None."""
    users = load_users()
    user = users.get(username)
    if user and user["password"] == hash_password(password):
        return {"username": username, "role": user["role"]}
    return None


def login_form() -> dict | None:
    """Affiche le formulaire et retourne l'utilisateur connecté."""
    if "user" in st.session_state:
        return st.session_state["user"]

    st.subheader("🔐 Connexion requise")
    with st.form("login"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            user = authenticate(username, password)
            if user:
                st.session_state["user"] = user
                st.rerun()
            else:
                st.error("Identifiants invalides.")
    return None


def logout() -> None:
    st.session_state.pop("user", None)
    st.rerun()


def require_auth() -> dict:
    """Bloque l'accès si non authentifié. Retourne le user."""
    user = login_form()
    if not user:
        st.stop()
    return user


if __name__ == "__main__":
    st.set_page_config(page_title="US-17 — Authentification", layout="wide")
    st.title("US-17 — Contrôle d'accès")

    user = require_auth()
    st.success(f"Connecté en tant que **{user['username']}** (rôle : `{user['role']}`)")
    st.write("Cette zone est protégée.")

    if st.button("Se déconnecter"):
        logout()
