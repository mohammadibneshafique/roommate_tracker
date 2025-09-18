import pandas as pd

# Initialize empty DataFrame
try:
    df = pd.read_excel("expenses.xlsx")
except FileNotFoundError:
    df = pd.DataFrame(columns=["Name", "Amount", "Description"])

def save_to_excel():
    df.to_excel("expenses.xlsx", index=False)
    print("✅ Data saved to expenses.xlsx")

def add_expense():
    name = input("Who paid? (Mohammad/Mahtab): ").strip()
    amount = float(input("Amount (SAR): "))
    description = input("Description: ").strip()
    global df
    df = pd.concat([df, pd.DataFrame([{
        "Name": name,
        "Amount": amount,
        "Description": description
    }])], ignore_index=True)
    save_to_excel()

def show_expenses():
    if df.empty:
        print("No expenses recorded.")
    else:
        print("\n📋 All Expenses:")
        print(df)

def edit_expense():
    show_expenses()
    index = int(input("Enter index to edit: "))
    if 0 <= index < len(df):
        new_amount = float(input("New amount (SAR): "))
        new_desc = input("New description: ")
        df.at[index, "Amount"] = new_amount
        df.at[index, "Description"] = new_desc
        save_to_excel()
    else:
        print("Invalid index.")

def delete_expense():
    show_expenses()
    index = int(input("Enter index to delete: "))
    if 0 <= index < len(df):
        global df
        df = df.drop(index).reset_index(drop=True)
        save_to_excel()
    else:
        print("Invalid index.")

def clear_expenses():
    confirm = input("⚠️ Clear all data? (yes/no): ")
    if confirm.lower() == "yes":
        global df
        df = pd.DataFrame(columns=["Name", "Amount", "Description"])
        save_to_excel()
        print("All expenses cleared.")

def show_summary():
    total_mohammad = df[df["Name"].str.lower() == "mohammad"]["Amount"].sum()
    total_mahtab = df[df["Name"].str.lower() == "mahtab"]["Amount"].sum()
    total = total_mohammad + total_mahtab
    split = total / 2
    print(f"\n💰 Summary:")
    print(f"Total spent by Mohammad: {total_mohammad:.2f} SAR")
    print(f"Total spent by Mahtab: {total_mahtab:.2f} SAR")
    print(f"Each should pay: {split:.2f} SAR")
    if total_mohammad > split:
        print(f"Mahtab owes Mohammad: {total_mohammad - split:.2f} SAR")
    elif total_mahtab > split:
        print(f"Mohammad owes Mahtab: {total_mahtab - split:.2f} SAR")
    else:
        print("You're all settled up!")

# Menu loop
while True:
    print("\n📌 Menu:")
    print("1. Add Expense")
    print("2. Show Expenses")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Clear All Expenses")
    print("6. Show Summary")
    print("7. Exit")

    choice = input("Choose an option (1–7): ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        show_expenses()
    elif choice == "3":
        edit_expense()
    elif choice == "4":
        delete_expense()
    elif choice == "5":
        clear_expenses()
    elif choice == "6":
        show_summary()
    elif choice == "7":
        print("Goodbye, Mohammad! Stay fair and balanced.")
        break
    else:
        print("Invalid option. Try again.")
