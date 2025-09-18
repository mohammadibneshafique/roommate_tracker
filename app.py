import streamlit as st
import pandas as pd
from datetime import datetime
import os

EXCEL_FILE = "expenses.xlsx"

# Load or create the Excel file
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Cost (SR)", "Paid By", "Notes", "Voucher"])

st.set_page_config(page_title="Roommate Tracker", page_icon="📒")
st.title("📒 Roommate Expense Tracker")

section = st.sidebar.radio("Navigate", ["➕ Log Expense", "📜 View Journal"])

if section == "➕ Log Expense":
    st.subheader("Add a New Expense")

    cost = st.number_input("Total Cost (SR)", min_value=0.0, format="%.2f")
    payer = st.selectbox("Paid By", ["Abdullah", "Mahtab"])
    notes = st.text_input("Notes (e.g. groceries, snacks)")
    voucher = st.text_input("Voucher filename (optional)")
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if st.button("✅ Save Expense"):
        new_entry = pd.DataFrame([{
            "Date": date,
            "Cost (SR)": cost,
            "Paid By": payer,
            "Notes": notes,
            "Voucher": voucher if voucher else "None"
        }])

        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)

        st.success("Expense saved to Excel!")

elif section == "📜 View Journal":
    st.subheader("All Logged Expenses")

    if df.empty:
        st.info("No expenses logged yet.")
    else:
        st.dataframe(df)
