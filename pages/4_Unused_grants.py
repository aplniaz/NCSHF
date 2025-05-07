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


# Convert numeric columns
df['remaining_balance'] = pd.to_numeric(df['remaining_balance'], errors='coerce')
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Title
st.title("💰 Unused Grant Analysis & Assistance Type Summary")

# 1. Patients with unused grant (Remaining balance > 0)
unused_grants = df[df['remaining_balance'] > 0]
st.subheader("Patients With Unused Grant Funds")
st.write(f"Total: {len(unused_grants)} applications with unused funds.")
st.dataframe(unused_grants[['patient_idnumber', 'app_year', 'remaining_balance', 'amount']])

# 2. Average amount by assistance type
st.subheader("Average Amount by Assistance Type")
avg_by_type = df.groupby('type_of_assistance_class')['amount'].mean().sort_values(ascending=False)
#st.bar_chart(avg_by_type)


#fig, ax = plt.subplots()
#avg_by_type.plot(kind='bar', ax=ax)
#ax.set_title("Average Grant Amount by Assistance Type")
#ax.set_xlabel("Type of Assistance")
#ax.set_ylabel("Average Amount ($)")
#st.pyplot(fig)




st.dataframe(avg_by_type.reset_index(name='average_amount'))
