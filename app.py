import streamlit as st
import pandas as pd
from datetime import date
import os

EXCEL_FILE = "expenses.xlsx"

# Load or create Excel file
if os.path.exists(EXCEL_FILE):
    df = pd.read_excel(EXCEL_FILE)
else:
    df = pd.DataFrame(columns=["Date", "Cost (SR)", "Paid By", "Voucher", "Type"])
    df.to_excel(EXCEL_FILE, index=False)

st.set_page_config(page_title="Roommate Ledger", page_icon="🏠")
st.title("🏠 Roommate Ledger")

section = st.sidebar.radio("Navigate", ["➕ Log Expense", "💸 Record Payment", "📊 View Details", "🧹 Reset All"])

# ➕ Log Expense
if section == "➕ Log Expense":
    st.subheader("Add a New Expense")

    cost = st.number_input("Total Cost (SR)", min_value=0.0, format="%.2f")
    payer = st.selectbox("Paid By", ["Abdullah", "Mahtab"])
    expense_date = st.date_input("Date", value=date.today())
    voucher = st.text_input("Voucher filename (optional)")

    if st.button("✅ Save Expense"):
        new_entry = pd.DataFrame([{
            "Date": expense_date.strftime("%Y-%m-%d"),
            "Cost (SR)": cost,
            "Paid By": payer,
            "Voucher": voucher if voucher else "None",
            "Type": "Expense"
        }])
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_excel(EXCEL_FILE, index=False)
        st.success("Expense saved to Excel!")

# 💸 Record Payment
elif section == "💸 Record Payment":
    st.subheader("Record a Payment Between Roommates")
    name = st.selectbox("Who paid back?", ["Abdullah", "Mahtab"])
    amount = st.number_input("Amount Paid (SR)", min_value=0.0, format="%.2f")

    if st.button("Confirm Payment"):
        if amount > 0:
            payment_entry = pd.DataFrame([{
                "Date": date.today().strftime("%Y-%m-%d"),
                "Cost (SR)": amount,
                "Paid By": name,
                "Voucher": "None",
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
                other = "Mahtab" if payer == "Abdullah" else "Abdullah"
                totals[other]["balance"] += split

            for _, row in payments_only.iterrows():
                payer = row["Paid By"]
                amount = row["Cost (SR)"]
                totals[payer]["balance"] -= amount

            total_expenses = expenses_only["Cost (SR)"].sum()

            for name in ["Abdullah", "Mahtab"]:
                st.write(f"**{name} Total Contribution:** SR {totals[name]['contribution']:.2f}")
                st.write(f"**{name} Total Due:** SR {totals[name]['balance']:.2f}")

            st.markdown("---")
            st.write(f"🧾 **Total Expenses (All): SR {total_expenses:.2f}**")

    elif view == "Expense Journal":
        st.subheader("📜 All Logged Expenses")

        expenses_only = df[df["Type"] == "Expense"].reset_index(drop=True)

        if expenses_only.empty:
            st.info("No expenses logged yet.")
        else:
            st.dataframe(expenses_only.style.set_table_styles([
                {"selector": "th", "props": [("border", "1px solid #ccc"), ("background-color", "#f2f2f2")]},
                {"selector": "td", "props": [("border", "1px solid #ccc")]}
            ]))

            for i, row in expenses_only.iterrows():
                st.markdown(f"**Entry #{i} Controls**")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"✏️ Edit Entry #{i}", key=f"edit_{i}"):
                        with st.form(f"edit_form_{i}"):
                            new_date = st.date_input("Date", value=pd.to_datetime(row["Date"]))
                            new_cost = st.number_input("Cost (SR)", value=float(row["Cost (SR)"]), format="%.2f")
                            new_payer = st.selectbox("Paid By", ["Abdullah", "Mahtab"], index=["Abdullah", "Mahtab"].index(row["Paid By"]))
                            new_voucher = st.text_input("Voucher filename", value=row["Voucher"])
                            submitted = st.form_submit_button("✅ Save Changes")
                            if submitted:
                                original_index = df[(df["Type"] == "Expense")].index[i]
                                df.at[original_index, "Date"] = new_date.strftime("%Y-%m-%d")
                                df.at[original_index, "Cost (SR)"] = new_cost
                                df.at[original_index, "Paid By"] = new_payer
                                df.at[original_index, "Voucher"] = new_voucher
                                df.to_excel(EXCEL_FILE, index=False)
                                st.success("Entry updated successfully.")
                                st.experimental_rerun()
                with col2:
                    if st.button(f"🗑️ Delete Entry #{i}", key=f"delete_{i}"):
                        original_index = df[(df["Type"] == "Expense")].index[i]
                        df = df.drop(index=original_index).reset_index(drop=True)
                        df.to_excel(EXCEL_FILE, index=False)
                        st.success("Entry deleted successfully.")
                        st.experimental_rerun()

# 🧹 Reset All
elif section == "🧹 Reset All":
    st.subheader("⚠️ Clear All Data")
    st.warning("This will delete all entries permanently.")

    if st.button("🧹 Confirm Reset"):
        df = pd.DataFrame(columns=["Date", "Cost (SR)", "Paid By", "Voucher", "Type"])
        df.to_excel(EXCEL_FILE, index=False)
        st.success("All data cleared. Ledger restarted.")
