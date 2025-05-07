import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt



# Load cleaned data
#df = pd.read_csv(os.path.join("data", "cleaned_data.csv"))

if 'cleaned_df' in st.session_state:
    df = st.session_state.cleaned_df.copy()
else:
    st.error("No cleaned data found. Please upload data from the Home page first.")
    st.stop()


# Ensure amount is numeric
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Convert DOB to datetime and calculate age
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
df['age'] = (pd.to_datetime("today") - df['dob']).dt.days // 365

# Create age groups
bins = [0, 17, 30, 45, 60, 75, 100]
labels = ['<18', '18–30', '31–45', '46–60', '61–75', '76+']
df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)

# Define demographic options
options = {
    "State": "pt_state",
    "City": "pt_city",
    "Gender": "gender",
    "Insurance Type": "insurance_type",
    "Monthly Income": "total_household_gross_monthly_income",
    "Household Size": "household_size",
    "Age Group": "age_group"
}

# Streamlit UI
st.title("Support Amount by Demographics")
selected = st.selectbox("Select a demographic factor:", list(options.keys()))
group_col = options[selected]

# Drop missing
group_data = df[[group_col, 'amount']].dropna()

# Group and summarize
summary = group_data.groupby(group_col)['amount'].sum().sort_values(ascending=False)

# Display
st.bar_chart(summary)

#fig, ax = plt.subplots()
#summary.plot(kind='bar', ax=ax)
#ax.set_title(f"Total Support by {selected}")
#ax.set_xlabel(selected)
#ax.set_ylabel("Total Support Amount ($)")
#st.pyplot(fig)

st.dataframe(summary.reset_index(name="Total Support Amount"))






