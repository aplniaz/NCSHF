import streamlit as st
import pandas as pd
import os

# Load cleaned data
df = pd.read_csv(os.path.join("data", "cleaned_data.csv"))

# Convert date columns
df['grant_req_date'] = pd.to_datetime(df['grant_req_date'], errors='coerce')
df['payment_submitted'] = pd.to_datetime(df['payment_submitted'], errors='coerce')

# Calculate delay in days
df['delay_days'] = (df['payment_submitted'] - df['grant_req_date']).dt.days

# Filter valid rows
valid_delays = df[df['delay_days'].notnull() & (df['delay_days'] >= 0)]

# Title
st.title("⏱️ Delay Between Request and Support Sent")

# Stats
st.write("### Summary Statistics")
st.write(valid_delays['delay_days'].describe())

# Histogram
st.write("### Distribution of Delay (Days)")
st.bar_chart(valid_delays['delay_days'].value_counts().sort_index())

# Trend over time
df['year'] = df['grant_req_date'].dt.year
yearly_delay = valid_delays.groupby('year')['delay_days'].mean().dropna()

st.write("### Average Delay by Year")
st.line_chart(yearly_delay)
