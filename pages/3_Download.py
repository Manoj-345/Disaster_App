# pages/3_Download.py
import streamlit as st
from utils import load_data

st.title("💾 Download Dataset")

df = load_data()

st.write("You can download the processed dataset below:")

csv = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download CSV", data=csv, file_name="disasters_clean.csv", mime="text/csv")

st.dataframe(df.sample(10))
