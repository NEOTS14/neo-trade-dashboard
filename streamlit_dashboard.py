
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NEO Trading Log Dashboard", layout="wide")

# Load log data
@st.cache_data
def load_data():
    df = pd.read_csv("log_data.csv", parse_dates=["Timestamp"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()

# Title
st.title("📊 NEO Trading Systems - Live Log Dashboard")

# Summary statistics
st.subheader("📌 Summary Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Trades", df[df['Event'].str.contains("Long trade placed")].shape[0])
col2.metric("Trailing Stop Adjustments", df[df['Event'].str.contains("Trailing Stop updated")].shape[0])
col3.metric("MaxBars Exits", df[df['Event'].str.contains("MaxBarsInTrade")].shape[0])

# Timeline Chart
st.subheader("📈 Trade Timeline")
fig, ax = plt.subplots(figsize=(10, 4))
df['hour'] = df['Timestamp'].dt.hour
df[df['Event'].str.contains("Long trade placed")].groupby('hour').size().plot(kind='bar', ax=ax, color='skyblue')
ax.set_title("Trades by Hour")
ax.set_xlabel("Hour of Day")
ax.set_ylabel("Number of Trades")
st.pyplot(fig)

# Table of latest events
st.subheader("🧾 Latest Events Log")
st.dataframe(df.sort_values("Timestamp", ascending=False).reset_index(drop=True), use_container_width=True)

# Symbol filter
st.subheader("🔍 Filter by Symbol")
symbols = df['Symbol'].unique()
selected_symbol = st.selectbox("Select Symbol", symbols)
filtered = df[df['Symbol'] == selected_symbol]
st.dataframe(filtered.sort_values("Timestamp", ascending=False).reset_index(drop=True), use_container_width=True)
