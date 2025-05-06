import streamlit as st
import pandas as pd
import os

# Load data
df = pd.read_csv(os.path.join("data", "cleaned_data.csv"))

# Title
st.title("🎗️ Nebraska Cancer Specialists Hope Foundation Dashboard")
st.markdown("""
Welcome to the Hope Foundation dashboard. Use the tabs on the left to explore:

- **📋 Ready-for-Review Applications**  
- **📊 Support by Demographics**  
- **⏱️ Request to Support Delay Analysis**  
- **💰 Unused Grant Overview & Assistance Averages**  
- **📈 Annual Impact Summary for Stakeholders**

""")

# Quick KPI Cards
st.subheader("📌 Snapshot")
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

total_support = df['amount'].sum()
total_applications = len(df)
unique_patients = df['patient_idnumber'].nunique() if 'patient_idnumber' in df.columns else "N/A"

col1, col2, col3 = st.columns(3)
col1.metric("Total Support Given", f"${total_support:,.2f}")
col2.metric("Applications", total_applications)
col3.metric("Unique Patients", unique_patients)

st.info("Use the sidebar to switch between pages and explore detailed insights.")
