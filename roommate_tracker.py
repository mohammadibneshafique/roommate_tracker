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

if "item_count" not in st.session_state:
    st.session_state.item_count = 1

if "inputs" not in st.session_state:
    st.session_state.inputs = []

st.set_page_config(page_title="Roommate Ledger", page_icon="🏠")
st.title("🏠 Roommate Ledger")

# Sidebar navigation
section = st.sidebar.radio("Navigate", ["➕ Log Expenses", "💸 Record Payment", "📊 View Details"])

# ➕ Log Multiple Expenses
if section == "➕ Log Expenses":
    st.subheader("Log Multiple Expenses")

    for i in range(st.session_state.item_count):
        st.markdown(f"### Item {i + 1}")
        item = st.text_input(f"Item Name {i + 1}", key=f"item_{i}")
        quantity = st.number_input(f"Quantity {i + 1}", min_value=0.0, format="%.2f", key=f"qty_{i}")
        unit = st.selectbox(f"Unit {i + 1}", ["kg", "liter", "pack", "bottle", "piece", "other"], key=f"unit_{i}")
        rate = st.number_input(f"Rate per {unit} (SR) {i + 1} (optional)", min_value=0.0, format="%.2f", key=f"rate_{i}")

        if rate > 0:
            total_cost = quantity * rate
            st.write(f"**Calculated Total Cost:** SR {total_cost:.2f}")
        else:
            total_cost = st.number_input(f"Enter Total Cost Manually (SR) {i + 1}", min_value=0.0, format="%.2f", key=f"manual_cost_{i}")

        payer = st.selectbox(f"Payer {i + 1}", ["Abdullah", "Mahtab"], key=f"payer_{i}")
        expense_date = st.date_input(f"Date {i + 1}", value=date.today(), key=f"date_{i}")
        receipt = st.file_uploader(f"Receipt {i + 1} (optional)", type=["jpg", "jpeg", "png", "pdf"], key=f"receipt_{i}")

        st.session_state.inputs.append({
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Item": item,
            "Quantity": quantity,
            "Unit": unit,
            "Rate per Unit (SR)": rate if rate > 0 else "N/A",
            "Cost (SR)": total_cost,
            "Paid By": payer,
            "Receipt": receipt.name if receipt else "None"
        })

    if st.button("➕ Add Another Item"):
        st.session_state.item_count += 1

    if st.button("✅ Save All"):
        for entry in st.session_state.inputs:
            if entry["Item"] and entry["Cost (SR)"] > 0:
                st.session_state.transactions.append(entry)
                payer = entry["Paid By"]
                cost = entry["Cost (SR)"]
                st.session_state.totals[payer]["contribution"] += cost
                split = cost / 2
                st.session_state.totals["Abdullah"]["balance"] += split
                st.session_state.totals["Mahtab"]["balance"] += split

        st.success("All items saved successfully!")
        st.session_state.inputs = []
        st.session_state.item_count = 1

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