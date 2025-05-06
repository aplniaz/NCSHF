import streamlit as st
import pandas as pd
import os

# Load cleaned data
df = pd.read_csv(os.path.join("data", "cleaned_data.csv"))

# Clean numeric + date fields
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['grant_req_date'] = pd.to_datetime(df['grant_req_date'], errors='coerce')
df['year'] = df['grant_req_date'].dt.year

# Title
st.title("📈 Annual Impact Summary")

# KPIs
total_support = df['amount'].sum()
unique_patients = df['patient_idnumber'].nunique()
total_requests = len(df)

st.metric("Total Support Given", f"${total_support:,.2f}")
st.metric("Total Unique Patients", unique_patients)
st.metric("Total Applications", total_requests)

# Yearly trend
st.subheader("Support Given Over the Years")
yearly_support = df.groupby('year')['amount'].sum()
st.line_chart(yearly_support)

# By location
st.subheader("Top States by Support Amount")
state_support = df.groupby('pt_state')['amount'].sum().sort_values(ascending=False).head(10)
st.bar_chart(state_support)

# By type of assistance
if 'type_of_assistance_class' in df.columns:
    st.subheader("Support by Type of Assistance")
    type_breakdown = df.groupby('type_of_assistance_class')['amount'].sum().sort_values(ascending=False)
    st.bar_chart(type_breakdown)
