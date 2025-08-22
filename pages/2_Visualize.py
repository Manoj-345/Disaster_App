# pages/2_Visualize.py
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, get_key_columns

st.set_page_config(page_title="Disaster Visualization", layout="wide")
st.title("📊 Disaster Trends Dashboard")

# Load Data
df = load_data()
cols = get_key_columns(df)
year_col, country_col, disaster_col, numeric_cols = (
    cols["year"], cols["country"], cols["disaster"], cols["numeric"]
)

if year_col is None:
    st.error("⚠️ No Year column detected. Cannot plot trends.")
else:
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    countries = []
    if country_col:
        countries = st.sidebar.multiselect("Select Countries", df[country_col].unique())
        if countries:
            df = df[df[country_col].isin(countries)]

    disasters = []
    if disaster_col:
        disasters = st.sidebar.multiselect("Select Disaster Types", df[disaster_col].unique())
        if disasters:
            df = df[df[disaster_col].isin(disasters)]

    metric = st.sidebar.selectbox("📈 Metric", ["Record Count"] + numeric_cols)
    chart_type = st.sidebar.radio("📊 Chart Type", ["Line", "Bar", "Pie"])

    # Main Visualization
    st.subheader("📈 Overall Trends")
    if metric == "Record Count":
        trend = df.groupby(year_col).size().reset_index(name="count")
        y_col = "count"
    else:
        trend = df.groupby(year_col)[metric].sum().reset_index()
        y_col = metric

    if chart_type == "Line":
        fig = px.line(trend, x=year_col, y=y_col, markers=True,
                      title=f"{metric} Over Time")
    elif chart_type == "Bar":
        fig = px.bar(trend, x=year_col, y=y_col,
                     title=f"{metric} Over Time")
    elif chart_type == "Pie":
        latest_year = trend[year_col].max()
        latest_data = df[df[year_col] == latest_year]
        if disaster_col:
            pie_data = latest_data.groupby(disaster_col).size().reset_index(name="count")
            fig = px.pie(pie_data, values="count", names=disaster_col,
                         title=f"Disaster Breakdown ({latest_year})")
        else:
            st.warning("⚠️ Pie chart requires Disaster Type column.")
            fig = go.Figure()

    st.plotly_chart(fig, use_container_width=True)

    # Disaster Type Breakdown
    if disaster_col:
        st.subheader("🌪️ Disaster Type Breakdown Over Time")
        type_trend = df.groupby([year_col, disaster_col]).size().reset_index(name="count")
        fig2 = px.area(type_trend, x=year_col, y="count", color=disaster_col,
                       title="Proportion of Disasters by Type Over Time", groupnorm="fraction")
        st.plotly_chart(fig2, use_container_width=True)

    # Country-Level View
    if country_col:
        st.subheader("🌍 Country-Level Analysis")
        country_metric = df.groupby(country_col).size().reset_index(name="count")
        top_countries = country_metric.sort_values("count", ascending=False).head(10)

        fig3 = px.bar(top_countries, x=country_col, y="count", color=country_col,
                      title="Top 10 Countries by Disaster Count")
        st.plotly_chart(fig3, use_container_width=True)
