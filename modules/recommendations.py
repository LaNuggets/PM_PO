"""
Module recommandations — Cléo (dcleooo)

Couvre : US-11 (reco auto), US-12 (catégorisation), US-13 (justification).

⚠️ Hotfix : ce fichier compose les trois modules réellement implémentés
(`auto_recommendation.py`, `reco_justification.py`, `client_categorization.py`)
pour que `app.py` puisse accéder aux US-11/12/13 via un seul point d'entrée.
"""
from __future__ import annotations

import streamlit as st

from modules import (
    auto_recommendation,
    client_categorization,
    reco_justification,
)
from modules.auto_recommendation import (  # noqa: F401
    add_recommendations,
    generate_recommendation,
)
from modules.client_categorization import (  # noqa: F401
    CATEGORIES,
    add_categories,
    categorize_client,
)
from modules.reco_justification import build_justification  # noqa: F401


def render(df) -> None:
    """Vue Recommandations : catégorisation + reco auto + justification."""
    st.header("Recommandations")

    tab_reco, tab_cat, tab_just = st.tabs(
        ["🤖 Recommandations auto", "🏷️ Catégorisation", "💬 Justification"]
    )

    with tab_reco:
        auto_recommendation.render(df)

    with tab_cat:
        client_categorization.render(df)

    with tab_just:
        reco_justification.render(df)
