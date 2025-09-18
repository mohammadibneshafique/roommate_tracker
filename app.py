elif view == "Expense Journal":
    st.subheader("📜 All Logged Expenses")

    expenses_only = df[df["Type"] == "Expense"].reset_index(drop=True)

    if expenses_only.empty:
        st.info("No expenses logged yet.")
    else:
        for i, row in expenses_only.iterrows():
            with st.container():
                st.markdown(f"**Entry #{i}**")
                st.write(f"📅 Date: {row['Date']}")
                st.write(f"💰 Cost: SR {row['Cost (SR)']:.2f}")
                st.write(f"👤 Paid By: {row['Paid By']}")
                st.write(f"🧾 Voucher: {row['Voucher']}")

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
