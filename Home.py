import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")
st.title("🎗️ Nebraska Cancer Specialists Hope Foundation Dashboard")

st.markdown("""
Welcome to the Hope Foundation dashboard. Upload your raw Excel file below to clean and explore the data.

**📋 Tabs available in sidebar:**
- Ready-for-Review Applications  
- Support by Demographics  
- Request to Support Delay Analysis  
- Unused Grant Overview  
- Annual Impact Summary  
""")

# Upload Section
uploaded_file = st.file_uploader("📤 Upload Raw Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # --- CLEANING START ---
        # Standardize column names
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
            .str.replace("#", "number")
            .str.replace("/", "_")
            .str.replace("?", "")
            .str.replace(":", "")
            .str.replace("(", "")
            .str.replace(")", "")
        )

        # Drop rows without required patient ID
        df.dropna(subset=['patient_idnumber'], inplace=True)

        # Convert date fields
        date_cols = ['date', 'dob', 'payment_submitted', 'grant_req_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')

        # Derive 'year' from grant request date
        if 'grant_req_date' in df.columns:
            df['year'] = df['grant_req_date'].dt.year

        # Convert numeric columns
        numeric_cols = [
            'remaining_balance',
            'total_household_gross_monthly_income',
            'amount',
            'distance_roundtrip_tx'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

        # Normalize categorical fields
        cleanup_cols = {
            'pt_state': 'upper',
            'gender': 'title',
            'insurance_type': 'title',
            'application_signed': 'upper',
            'request_status': 'title',
            'type_of_assistance_class': 'title'
        }

        for col, method in cleanup_cols.items():
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                if method == 'upper':
                    df[col] = df[col].str.upper()
                elif method == 'lower':
                    df[col] = df[col].str.lower()
                elif method == 'title':
                    df[col] = df[col].str.title()

        # Replace common string placeholders with pd.NA
        df.replace(['nan', 'none', 'None', 'missing', 'Missing'], pd.NA, inplace=True)

        # --- CLEANING END ---

        # Store cleaned data in session_state so it can be accessed across pages
        st.session_state.cleaned_df = df

        st.success("✅ Data cleaned successfully!")

        # Quick KPI Cards
        st.subheader("📌 Snapshot")
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
        total_support = df['amount'].sum()
        total_applications = len(df)
        unique_patients = df['patient_idnumber'].nunique()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Support Given", f"${total_support:,.2f}")
        col2.metric("Applications", total_applications)
        col3.metric("Unique Patients", unique_patients)

        # Data Preview
        st.dataframe(df.head(50))

        # Download cleaned file
        cleaned_csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Cleaned CSV", cleaned_csv, "cleaned_data.csv", "text/csv")

    except Exception as e:
        st.error(f"❌ Error loading or processing file: {e}")
else:
    st.info("📎 Upload an Excel file (.xlsx) to clean and explore the data.")
