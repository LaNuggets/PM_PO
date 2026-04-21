import streamlit as st
import pandas as pd


CATEGORIES = {
    "relancer": {"color": "#e74c3c", "emoji": "🔴"},
    "fidéliser": {"color": "#2ecc71", "emoji": "🟢"},
    "surveiller": {"color": "#f39c12", "emoji": "🟡"},
}


def categorize_client(client: pd.Series) -> str:
    risk = str(client.get("risk_level", "")).lower()
    revenue = float(client.get("revenue", 0) or 0)

    if risk in ("high", "élevé"):
        return "relancer"
    if revenue > 10000:
        return "fidéliser"
    return "surveiller"


def add_categories(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["category"] = df.apply(categorize_client, axis=1)
    return df


def render(df: pd.DataFrame) -> None:
    categorized = add_categories(df)

    cols = st.columns(len(CATEGORIES))
    for col, (cat, style) in zip(cols, CATEGORIES.items()):
        count = (categorized["category"] == cat).sum()
        col.metric(label=f"{style['emoji']} {cat.capitalize()}", value=int(count))

    st.subheader("Détail par client")
    st.dataframe(categorized)


if __name__ == "__main__":
    st.set_page_config(page_title="US-12 — Catégories", layout="wide")
    st.title("US-12 — Catégorisation des clients")

    uploaded = st.file_uploader("Importer un CSV", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        render(df)
    else:
        st.info("Charge un CSV pour voir les catégories.")
