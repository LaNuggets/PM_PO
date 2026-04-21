import json
from pathlib import Path

import streamlit as st


ACTIONS_FILE = Path("data/actions.json")
STATUSES = ["à faire", "en cours", "terminée"]
STATUS_EMOJI = {"à faire": "⏳", "en cours": "🔄", "terminée": "✅"}


def load_actions() -> list[dict]:
    if not ACTIONS_FILE.exists():
        return []
    return json.loads(ACTIONS_FILE.read_text(encoding="utf-8"))


def save_actions(actions: list[dict]) -> None:
    ACTIONS_FILE.parent.mkdir(exist_ok=True)
    ACTIONS_FILE.write_text(json.dumps(actions, indent=2, ensure_ascii=False), encoding="utf-8")


def update_status(action_id: int, new_status: str) -> bool:
    if new_status not in STATUSES:
        raise ValueError(f"Statut invalide : {new_status}")
    actions = load_actions()
    for action in actions:
        if action["id"] == action_id:
            action["status"] = new_status
            save_actions(actions)
            return True
    return False


def render() -> None:
    actions = load_actions()
    if not actions:
        st.info("Aucune action enregistrée. Crée d'abord une action (US-14).")
        return

    for action in actions:
        with st.expander(f"{STATUS_EMOJI[action['status']]} #{action['id']} — {action['title']}"):
            st.write(f"Client : `{action['client_id']}`")
            st.write(f"Responsable : {action.get('owner', '-')}")
            st.write(f"Échéance : {action.get('deadline', '-')}")
            current = action["status"]
            new_status = st.selectbox(
                "Statut",
                STATUSES,
                index=STATUSES.index(current),
                key=f"status_{action['id']}",
            )
            if new_status != current:
                if update_status(action["id"], new_status):
                    st.success("Statut mis à jour.")
                    st.rerun()


if __name__ == "__main__":
    st.set_page_config(page_title="US-15 — Statut des actions", layout="wide")
    st.title("US-15 — Statut des actions")
    render()
