import pandas as pd
import os

# Define file paths
DATA_DIR = "data"
RAW_PATH = os.path.join(DATA_DIR, "raw_data.xlsx")
CLEANED_PATH = os.path.join(DATA_DIR, "cleaned_data.csv")

# Load raw Excel file
df = pd.read_excel(RAW_PATH)

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

# Drop rows without required ID
df.dropna(subset=['patient_idnumber'], inplace=True)

# Convert date columns
date_cols = ['date', 'dob', 'payment_submitted', 'grant_req_date']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')

# Add derived year column
if 'grant_req_date' in df.columns:
    df['year'] = df['grant_req_date'].dt.year

# Convert numeric fields
numeric_cols = [
    'remaining_balance',
    'total_household_gross_monthly_income',
    'amount',
    'distance_roundtrip_tx'
]
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Clean and format categorical columns
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

# Normalize pt_state missing/inconsistent entries
if 'pt_state' in df.columns:
    df['pt_state'] = (
        df['pt_state']
        .astype(str)
        .str.strip()
        .str.upper()
        .replace({
            'NAN': 'Missing',
            'NaN': 'Missing',
            'NONE': 'Missing',
            '': 'Missing',
            'MISSING': 'Missing'
        })
    )

# Replace other placeholders with NA and unify 'pt_state'
df.replace(['nan', 'none', 'None', 'missing', 'Missing'], pd.NA, inplace=True)
df['pt_state'] = df['pt_state'].replace({pd.NA: 'Missing'})

# Save cleaned data
df.to_csv(CLEANED_PATH, index=False, na_rep="Missing")
print(f"Cleaned data saved to: {CLEANED_PATH}")
