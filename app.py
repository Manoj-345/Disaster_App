# app.py
import streamlit as st
from utils import load_data, get_key_columns

st.set_page_config(page_title="🌍 Global Disaster Dashboard", layout="wide")

st.title("🌍 Global Disaster Dashboard")
st.markdown("Welcome to the **interactive disaster analytics app**. "
            "Use the sidebar to navigate across pages and explore insights from the dataset.")

# Load dataset
try:
    df = load_data()
    cols = get_key_columns(df)

    st.success("✅ Dataset loaded successfully!")
    st.write(f"**Rows:** {df.shape[0]} | **Columns:** {df.shape[1]}")
    st.dataframe(df.head(10))
except Exception as e:
    st.error(f"❌ Could not load dataset: {e}")
