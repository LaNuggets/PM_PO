"""
Module KPIs — Alvin (AlvinDiesel09)

Couvre : US-05 (total clients), US-06 (CA total), US-07 (segments), US-08 (clients à risque).
"""
import streamlit as st


def render_total_clients(df):
    """US-05."""
    # TODO(US-05)
    raise NotImplementedError


def render_total_revenue(df):
    """US-06."""
    # TODO(US-06)
    raise NotImplementedError


def render_segment_distribution(df):
    """US-07."""
    # TODO(US-07)
    raise NotImplementedError


def render_risk_clients(df):
    """US-08."""
    # TODO(US-08)
    raise NotImplementedError


def render_all(df) -> None:
    """Vue Dashboard (placeholder)."""
    st.header("Dashboard")
    st.info("Module en cours de développement (Alvin).")
    # TODO: appeler les 4 KPIs dans un st.columns(4)
