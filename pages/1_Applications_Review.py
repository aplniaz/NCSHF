import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Load cleaned data
if 'cleaned_df' in st.session_state:
    df = st.session_state.cleaned_df.copy()
else:
    st.error("No cleaned data found. Please upload data from the Home page first.")
    st.stop()

st.title("📋 Applications Ready for Review")

# Normalize 'request_status' first
df['request_status'] = df['request_status'].astype(str).str.strip().str.lower()

# Normalize 'application_signed' to just Y/N
df['application_signed'] = (
    df['application_signed']
    .astype(str)
    .str.strip()
    .str.lower()
    .replace({
        'yes': 'Y', 'y': 'Y',
        'no': 'N', 'n': 'N',
        'missing': 'N', 'none': 'N',
        'n/a': 'N',
        'nan': 'N'
    })
)

# Filter: Only approved applications
ready_df = df[df['request_status'] == 'approved']

# Sidebar filter for signed status
signed_filter = st.sidebar.selectbox("Filter by Application Signed", ['All', 'Signed', 'Not Signed'])

if signed_filter == 'Signed':
    ready_df = ready_df[ready_df['application_signed'] == 'Y']
elif signed_filter == 'Not Signed':
    ready_df = ready_df[ready_df['application_signed'] == 'N']

# Show result
st.write(f"Total: {len(ready_df)} applications")
st.dataframe(ready_df)
