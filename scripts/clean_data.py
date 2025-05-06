import pandas as pd
import os

# Load paths
data_path = '/Users/mdmonirulislam@unomaha.edu/Documents/projects/ECON-8320/data'
raw_path = os.path.join(data_path, 'raw_data.xlsx')
cleaned_path = os.path.join(data_path, 'cleaned_data.csv')

# Load raw data
df = pd.read_excel(raw_path)

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

# Convert dates
date_cols = ['date', 'dob', 'payment_submitted', 'grant_req_date']
for col in date_cols:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')

# Add derived 'year' from grant request
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

# Normalize values: categorical fields (case-insensitive cleanup)
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

# Optional: replace missing/none values
df.replace(['nan', 'none', 'None', 'missing', 'Missing'], pd.NA, inplace=True)

# Save cleaned file
df.to_csv(cleaned_path, index=False)
print(f"Cleaned data saved to: {cleaned_path}")
