import streamlit as st
import pandas as pd

if "transactions" not in st.session_state:
    st.session_state.transactions = []

if "totals" not in st.session_state:
    st.session_state.totals = {
        "Abdullah": {"input": 0.0, "cost_per_person": 0.0},
        "Mahtab": {"input": 0.0, "cost_per_person": 0.0}
    }

st.title("🏠 Roommate Expense Tracker")

option = st.sidebar.radio("Choose Function", ["Add", "Paid", "Details"])

if option == "Add":
    st.subheader("➕ Add Expense")
    item = st.text_input("Item Description")
    cost = st.number_input("Total Cost (SR)", min_value=0.0, format="%.2f")
    payer = st.selectbox("Who Paid?", ["Abdullah", "Mahtab"])

    if st.button("Add Transaction"):
        st.session_state.transactions.append({"item": item, "cost": cost, "payer": payer})
        st.session_state.totals[payer]["input"] += cost
        split = cost / 2
        st.session_state.totals["Abdullah"]["cost_per_person"] += split
        st.session_state.totals["Mahtab"]["cost_per_person"] += split
        st.success("Transaction Added!")

elif option == "Paid":
    st.subheader("💸 Record Payment")
    name = st.selectbox("Who Paid Back?", ["Abdullah", "Mahtab"])
    amount = st.number_input("Amount Paid (SR)", min_value=0.0, format="%.2f")

    if st.button("Record Payment"):
        st.session_state.totals[name]["cost_per_person"] -= amount
        st.success("Payment Recorded!")

elif option == "Details":
    st.subheader("📊 Summary")
    for name in ["Abdullah", "Mahtab"]:
        st.write(f"**{name} Total Input:** SR {st.session_state.totals[name]['input']:.2f}")
        st.write(f"**{name} Total Cost Per Person:** SR {st.session_state.totals[name]['cost_per_person']:.2f}")

    st.subheader("🧾 All Transactions")
    df = pd.DataFrame(st.session_state.transactions)
    if not df.empty:
        st.table(df)
    else:
        st.info("No transactions yet.")