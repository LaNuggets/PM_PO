import json
from datetime import date, datetime
from pathlib import Path

import streamlit as st


ACTIONS_FILE = Path("data/actions.json")


def load_actions() -> list[dict]:
    if not ACTIONS_FILE.exists():
        return []
    return json.loads(ACTIONS_FILE.read_text(encoding="utf-8"))


def save_actions(actions: list[dict]) -> None:
    ACTIONS_FILE.parent.mkdir(exist_ok=True)
    ACTIONS_FILE.write_text(json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8")


def create_action(title: str, client_id: str, deadline: str, owner: str, recommendation: str = "") -> dict:
    """Crée et persiste une action."""
    actions = load_actions()
    action = {
        "id": len(actions) + 1,
        "title": title,
        "client_id": client_id,
        "deadline": deadline,
        "owner": owner,
        "recommendation": recommendation,
        "status": "à faire",
        "created_at": datetime.utcnow().isoformat(timespec="seconds"),
    }
    actions.append(action)
    save_actions(actions)
    return action


def render() -> None:
    st.subheader("Créer une action")
    with st.form("new_action"):
        title = st.text_input("Titre de l'action")
        client_id = st.text_input("Client ID")
        deadline = st.date_input("Échéance", value=date.today())
        owner = st.text_input("Responsable")
        recommendation = st.text_area("Recommandation associée (optionnel)")

        submitted = st.form_submit_button("Créer")
        if submitted and title and client_id:
            action = create_action(title, client_id, deadline.isoformat(), owner, recommendation)
            st.success(f"Action #{action['id']} créée.")


if __name__ == "__main__":
    st.set_page_config(page_title="US-14 — Créer une action", layout="wide")
    st.title("US-14 — Création d'une action")
    render()
