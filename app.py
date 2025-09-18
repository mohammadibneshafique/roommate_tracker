import streamlit as st
import pandas as pd
from datetime import date
import os

EXCEL_FILE = "expenses.xlsx"

# Load or create Excel file
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=[
        "Date", "Item", "Quantity", "Unit", "Rate per Unit (SR)",
        "Cost (SR)", "Paid By", "Receipt", "Type"
    ])
    df.to_excel(EXCEL_FILE, index=False)

st.set_page_config(page_title="Roommate Ledger", page_icon="🏠")
st.title("🏠 Roommate Ledger")

section = st.sidebar.radio("Navigate", ["➕ Log Expenses", "💸 Record Payment", "📊 View Details"])

# ➕ Log Multiple Expenses
if section == "➕ Log Expenses":
    st.subheader("Log Multiple Expenses")

    if "item_count" not in st.session_state:
        st.session_state.item_count = 1

    inputs = []

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

        inputs.append({
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Item": item,
            "Quantity": quantity,
            "Unit": unit,
            "Rate per Unit (SR)": rate if rate > 0 else "N/A",
            "Cost (SR)": total_cost,
            "Paid By": payer,
            "Receipt": receipt.name if receipt else "None",
            "Type": "Expense"
        })

    if st.button("➕ Add Another Item"):
        st.session_state.item_count += 1

    if st.button("✅ Save All"):
        valid_entries = [entry for entry in inputs if entry["Item"] and entry["Cost (SR)"] > 0]
        if valid_entries:
            df = pd.concat([df, pd.DataFrame(valid_entries)], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success("All items saved to Excel!")
            st.session_state.item_count = 1
        else:
            st.warning("Please fill out all required fields.")

# 💸 Record Payment
elif section == "💸 Record Payment":
    st.subheader("Record a Payment Between Roommates")
    name = st.selectbox("Who paid back?", ["Abdullah", "Mahtab"])
    amount = st.number_input("Amount Paid (SR)", min_value=0.0, format="%.2f")

    if st.button("Confirm Payment"):
        if amount > 0:
            payment_entry = pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"),
                "Item": "Repayment",
                "Quantity": "N/A",
                "Unit": "N/A",
                "Rate per Unit (SR)": "N/A",
                "Cost (SR)": amount,
                "Paid By": name,
                "Receipt": "None",
                "Type": "Payment"
            }])
            df = pd.concat([df, payment_entry], ignore_index=True)
            df.to_excel(EXCEL_FILE, index=False)
            st.success(f"{name} paid SR {amount:.2f} toward their balance.")
        else:
            st.warning("Enter a valid amount.")

# 📊 View Details
elif section == "📊 View Details":
    view = st.radio("Choose View", ["Roommate Ledger", "Expense Journal"])

    if view == "Roommate Ledger":
        st.subheader("📋 Summary of Contributions & Balances")
        if df.empty:
            st.info("No data yet.")
        else:
            expenses_only = df[df["Type"] == "Expense"]
            payments_only = df[df["Type"] == "Payment"]

            totals = {"Abdullah": {"contribution": 0.0, "balance": 0.0},
                      "Mahtab": {"contribution": 0.0, "balance": 0.0}}

            for _, row in expenses_only.iterrows():
                payer = row["Paid By"]
                cost = row["Cost (SR)"]
                totals[payer]["contribution"] += cost
                split = cost / 2
                totals["Abdullah"]["balance"] += split
                totals["Mahtab"]["balance"] += split

            for _, row in payments_only.iterrows():
                payer = row["Paid By"]
                amount = row["Cost (SR)"]
                totals[payer]["balance"] -= amount

            for name in ["Abdullah", "Mahtab"]:
                st.write(f"**{name} Total Contribution:** SR {totals[name]['contribution']:.2f}")
                st.write(f"**{name} Current Balance:** SR {totals[name]['balance']:.2f}")

    elif view == "Expense Journal":
        st.subheader("📜 All Logged Expenses")
        if df.empty:
            st.info("No expenses logged yet.")
        else:
            st.dataframe(df[df["Type"] == "Expense"])
