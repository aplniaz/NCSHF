import streamlit as st
import pandas as pd

# Load from session state
if 'cleaned_df' in st.session_state:
    df = st.session_state.cleaned_df.copy()
else:
    st.error("No cleaned data found. Please upload data from the Home page first.")
    st.stop()

# Ensure amount is numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Convert DOB and compute age
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
df['age'] = (pd.to_datetime("today") - df['dob']).dt.days // 365

# Create age groups
bins = [0, 18, 31, 46, 61, 76, 200]
labels = ['<18', '18–30', '31–45', '46–60', '61–75', '76+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

# Demographic options
options = {
    "State": "pt_state",
    "City": "pt_city",
    "Gender": "gender",
    "Insurance Type": "insurance_type",
    "Monthly Income": "total_household_gross_monthly_income",
    "Household Size": "household_size",
    "Age Group": "age_group"
}

st.title("Support Amount by Demographics")
selected = st.selectbox("Select a demographic factor:", list(options.keys()))
group_col = options[selected]

# Drop missing and group
group_data = df[[group_col, 'amount']].dropna()
summary = (
    group_data.groupby(group_col)['amount']
    .sum()
    .reset_index(name='Total Support Amount')
)

# Remove zero-support groups
summary = summary[summary['Total Support Amount'] > 0]

# Sort and reset index
summary = summary.sort_values(by='Total Support Amount', ascending=False)

# Show chart and table
st.bar_chart(data=summary, x=group_col, y="Total Support Amount")
st.dataframe(summary)
