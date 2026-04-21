"""
Module actions — Cléo (dcleooo)

Couvre : US-14 (créer action), US-15 (statut), US-16 (liste).

⚠️ Hotfix : ce fichier compose les trois modules réellement implémentés
(`create_action.py`, `action_status.py`, `actions_list.py`) pour que `app.py`
accède aux US-14/15/16 via un seul point d'entrée.
"""
from __future__ import annotations

import streamlit as st

from modules import action_status, actions_list, create_action as _create_action
from modules.action_status import (  # noqa: F401
    STATUS_EMOJI,
    STATUSES,
    update_status,
)
from modules.create_action import (  # noqa: F401
    create_action,
    load_actions,
    save_actions,
)


def render() -> None:
    """Vue Actions : onglets Créer / Statut / Liste."""
    st.header("Actions")

    tab_create, tab_status, tab_list = st.tabs(
        ["➕ Créer", "🔄 Statuts", "📋 Liste"]
    )

    with tab_create:
        _create_action.render()

    with tab_status:
        action_status.render()

    with tab_list:
        actions_list.render()
