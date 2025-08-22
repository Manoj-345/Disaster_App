# pages/1_Explore_Data.py
import streamlit as st
from utils import load_data, get_key_columns

st.title("🔍 Explore Disaster Data")

df = load_data()
cols = get_key_columns(df)

year_col, country_col, disaster_col = cols["year"], cols["country"], cols["disaster"]

# Sidebar filters
if country_col:
    countries = st.sidebar.multiselect("🌎 Select Countries", df[country_col].unique())
    df = df[df[country_col].isin(countries)] if countries else df
else:
    st.sidebar.warning("⚠️ No Country column detected.")

if disaster_col:
    disasters = st.sidebar.multiselect("🌪️ Select Disaster Types", df[disaster_col].unique())
    df = df[df[disaster_col].isin(disasters)] if disasters else df
else:
    st.sidebar.warning("⚠️ No Disaster Type column detected.")

st.subheader("📋 Filtered Data Preview")
st.dataframe(df.head(50))
st.write(f"Showing **{len(df)}** records.")
