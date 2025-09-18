import streamlit as st
import pandas as pd
from datetime import date

# Initialize session state
if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "totals" not in st.session_state:
    st.session_state.totals = {
        "Abdullah": {"contribution": 0.0, "balance": 0.0},
        "Mahtab": {"contribution": 0.0, "balance": 0.0}
    }

st.set_page_config(page_title="Roommate Ledger", page_icon="🏠")
st.title("🏠 Roommate Ledger")

# Sidebar navigation
section = st.sidebar.radio("Navigate", ["➕ Log Expense", "💸 Record Payment", "📊 View Details"])

# ➕ Log Expense
if section == "➕ Log Expense":
    st.subheader("Log a New Expense")
    item = st.text_input("What was purchased?")
    cost = st.number_input("Total Cost (SR)", min_value=0.0, format="%.2f")
    payer = st.selectbox("Who paid?", ["Abdullah", "Mahtab"])
    expense_date = st.date_input("Date of Expense", value=date.today())
    receipt = st.file_uploader("Upload Receipt (optional)", type=["jpg", "jpeg", "png", "pdf"])

    if st.button("Save Expense"):
        if item and cost > 0:
            st.session_state.transactions.append({
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Item": item,
                "Cost (SR)": cost,
                "Paid By": payer,
                "Receipt": receipt.name if receipt else "None"
            })

            st.session_state.totals[payer]["contribution"] += cost
            split = cost / 2
            st.session_state.totals["Abdullah"]["balance"] += split
            st.session_state.totals["Mahtab"]["balance"] += split

            st.success(f"Saved: {item} for SR {cost:.2f} by {payer} on {expense_date.strftime('%Y-%m-%d')}")
        else:
            st.warning("Please enter a valid item and cost.")

# 💸 Record Payment
elif section == "💸 Record Payment":
    st.subheader("Record a Payment Between Roommates")
    name = st.selectbox("Who paid back?", ["Abdullah", "Mahtab"])
    amount = st.number_input("Amount Paid (SR)", min_value=0.0, format="%.2f")

    if st.button("Confirm Payment"):
        if amount > 0:
            st.session_state.totals[name]["balance"] -= amount
            st.success(f"{name} paid SR {amount:.2f} toward their balance.")
        else:
            st.warning("Enter a valid amount.")

# 📊 View Details
elif section == "📊 View Details":
    view = st.radio("Choose View", ["Roommate Ledger", "Expense Journal"])

    if view == "Roommate Ledger":
        st.subheader("📋 Summary of Contributions & Balances")
        for name in ["Abdullah", "Mahtab"]:
            st.write(f"**{name} Total Contribution:** SR {st.session_state.totals[name]['contribution']:.2f}")
            st.write(f"**{name} Current Balance:** SR {st.session_state.totals[name]['balance']:.2f}")

    elif view == "Expense Journal":
        st.subheader("📜 All Logged Expenses")
        if st.session_state.transactions:
            df = pd.DataFrame(st.session_state.transactions)
            st.table(df)
        else:
            st.info("No expenses logged yet.")