import streamlit as st
import pandas as pd
import os

# Load cleaned data
df = pd.read_csv(os.path.join("data", "cleaned_data.csv"))

st.title("Applications Ready for Review")

# Convert necessary column names to lowercase and safe format
if 'request_status' in df.columns:
    ready_df = df[df['request_status'].str.lower() == 'approved']
else:
    st.error("Missing 'request_status' column in dataset.")
    ready_df = pd.DataFrame()  # prevent NameError

# Filter: Application signed (formerly 'committee_signed')
if 'application_signed' in df.columns:
    # Normalize and map all variations to Y/N
    df['application_signed'] = (
        df['application_signed']
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({
            'yes': 'Y', 'y': 'Y',
            'no': 'N', 'n': 'N',
            'missing': 'N', 'none': 'N'
        })
    )

    signed_filter = st.sidebar.selectbox("Filter by Application Signed", ['All', 'Signed', 'Not Signed'])

    if signed_filter == 'Signed':
        ready_df = ready_df[df['application_signed'] == 'Y']
    elif signed_filter == 'Not Signed':
        ready_df = ready_df[df['application_signed'] == 'N']

# Show results
st.write(f"Total: {len(ready_df)} applications")
st.dataframe(ready_df)
