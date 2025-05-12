import streamlit as st
import pandas as pd
import os

DATA_PATH = "data/cleaned_data.csv"

st.set_page_config(page_title="Hope Foundation Dashboard", layout="wide")
st.title("🎗️ Nebraska Cancer Specialists Hope Foundation Dashboard")

st.markdown("""
Welcome to the Hope Foundation dashboard. 

📤 Upload your raw Excel file to clean and save it,  
📂 Or just explore the last uploaded dataset (auto-loaded from the `data/` folder).

**📋 Tabs available in sidebar:**
- Ready-for-Review Applications  
- Support by Demographics  
- Request to Support Delay Analysis  
- Unused Grant Overview  
- Annual Impact Summary  
""")

# File uploader
uploaded_file = st.file_uploader("Upload new raw Excel file", type=["xlsx"])

# If a file is uploaded, clean and save it
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # --- CLEANING START ---
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

        df.dropna(subset=['patient_idnumber'], inplace=True)

        date_cols = ['date', 'dob', 'payment_submitted', 'grant_req_date']
        for col in date_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')

        if 'grant_req_date' in df.columns:
            df['year'] = df['grant_req_date'].dt.year

        numeric_cols = [
            'remaining_balance',
            'total_household_gross_monthly_income',
            'amount',
            'distance_roundtrip_tx'
        ]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')

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

        df.replace(['nan', 'none', 'None', 'missing', 'Missing'], pd.NA, inplace=True)
        # --- CLEANING END ---

        df.to_csv(DATA_PATH, index=False)
        st.success("✅ New data cleaned and saved to `data/cleaned_data.csv`.")
        st.session_state.cleaned_df = df

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        st.stop()

# If no file uploaded but file already exists, load it
elif os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
    st.session_state.cleaned_df = df
    st.info("📂 Loaded previously cleaned data from `data/cleaned_data.csv`.")

# Neither uploaded nor saved data exists
else:
    st.warning("⚠️ No data found. Please upload an Excel file to begin.")
    st.stop()

# ---------- Dashboard content ----------

# KPIs
st.subheader("📌 Snapshot")
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
total_support = df['amount'].sum()
total_applications = len(df)
unique_patients = df['patient_idnumber'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Support Given", f"${total_support:,.2f}")
col2.metric("Applications", total_applications)
col3.metric("Unique Patients", unique_patients)

# Preview table
st.dataframe(df.head(50))

# Download button
cleaned_csv = df.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Download Cleaned CSV", cleaned_csv, "cleaned_data.csv", "text/csv")
