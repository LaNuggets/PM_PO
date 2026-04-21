"""
AIDA — AI Decision Assistant
Point d'entrée Streamlit.

Lancer : streamlit run app.py
"""
import streamlit as st

from modules import ingestion, kpi, filters, recommendations, actions, auth, audit


st.set_page_config(page_title="AIDA — AI Decision Assistant", layout="wide")


def main() -> None:
    st.sidebar.title("AIDA")

    user = auth.require_auth()
    st.sidebar.write(f"Connecté : **{user['username']}** (`{user['role']}`)")
    if st.sidebar.button("Se déconnecter"):
        auth.logout()

    pages = ["Import & données", "Dashboard", "Recommandations", "Actions"]
    if user["role"] == "admin":
        pages.append("Admin")

    page = st.sidebar.radio("Navigation", pages)

    st.title("AIDA — AI Decision Assistant")

    if page == "Import & données":
        ingestion.render()
    elif page == "Dashboard":
        df = st.session_state.get("df")
        if df is None:
            st.info("Importe d'abord un CSV dans l'onglet *Import & données*.")
            return
        filtered = filters.render_all(df)
        kpi.render_all(filtered)
    elif page == "Recommandations":
        df = st.session_state.get("df")
        if df is None:
            st.info("Importe d'abord un CSV.")
            return
        recommendations.render(df)
    elif page == "Actions":
        actions.render()
    elif page == "Admin":
        if not auth.has_permission(user, "view_audit_log"):
            st.error("Accès refusé : rôle `admin` requis.")
            return
        audit.render_admin_view()


if __name__ == "__main__":
    main()
