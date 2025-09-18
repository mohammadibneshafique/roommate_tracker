class Roommate:
    def __init__(self, name):
        self.name = name
        self.expenses = []

    def add_expense(self, amount, description):
        self.expenses.append((amount, description))

    def edit_expense(self, index, new_amount, new_description):
        if 0 <= index < len(self.expenses):
            self.expenses[index] = (new_amount, new_description)
        else:
            print("Invalid index.")

    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            del self.expenses[index]
        else:
            print("Invalid index.")

    def clear_expenses(self):
        self.expenses = []

    def total_expense(self):
        return sum(amount for amount, _ in self.expenses)

    def show_expenses(self):
        if not self.expenses:
            print("No expenses recorded.")
        for i, (amount, desc) in enumerate(self.expenses):
            print(f"{i}. {desc}: {amount} SAR")

# Setup
roommate1 = Roommate("Mohammad")
roommate2 = Roommate("Mahtab")

# Menu loop
while True:
    print("\n📋 Expense Tracker Menu:")
    print("1. Add Expense")
    print("2. Show Expenses")
    print("3. Edit Expense")
    print("4. Delete Expense")
    print("5. Clear All Expenses")
    print("6. Show Summary")
    print("7. Exit")

    choice = input("Choose an option (1–7): ")

    if choice == "1":
        name = input("Who paid? (Mohammad/Mahtab): ")
        amount = float(input("Amount (SAR): "))
        desc = input("Description: ")
        if name.lower() == "mohammad":
            roommate1.add_expense(amount, desc)
        elif name.lower() == "mahtab":
            roommate2.add_expense(amount, desc)
        else:
            print("Invalid name.")

    elif choice == "2":
        print("\nMohammad's Expenses:")
        roommate1.show_expenses()
        print("\nMahtab's Expenses:")
        roommate2.show_expenses()

    elif choice == "3":
        name = input("Whose expense to edit? (Mohammad/Mahtab): ")
        index = int(input("Expense index to edit: "))
        new_amount = float(input("New amount (SAR): "))
        new_desc = input("New description: ")
        if name.lower() == "mohammad":
            roommate1.edit_expense(index, new_amount, new_desc)
        elif name.lower() == "mahtab":
            roommate2.edit_expense(index, new_amount, new_desc)

    elif choice == "4":
        name = input("Whose expense to delete? (Mohammad/Mahtab): ")
        index = int(input("Expense index to delete: "))
        if name.lower() == "mohammad":
            roommate1.delete_expense(index)
        elif name.lower() == "mahtab":
            roommate2.delete_expense(index)

    elif choice == "5":
        confirm = input("⚠️ Are you sure you want to clear all data? (yes/no): ")
        if confirm.lower() == "yes":
            roommate1.clear_expenses()
            roommate2.clear_expenses()
            print("All expenses cleared.")

    elif choice == "6":
        total1 = roommate1.total_expense()
        total2 = roommate2.total_expense()
        total_shared = total1 + total2
        split = total_shared / 2
        print(f"\n💰 Summary:")
        print(f"Total spent by Mohammad: {total1} SAR")
        print(f"Total spent by Mahtab: {total2} SAR")
        print(f"Each should pay: {split:.2f} SAR")
        if total1 > split:
            print(f"Mahtab owes Mohammad: {total1 - split:.2f} SAR")
        elif total2 > split:
            print(f"Mohammad owes Mahtab: {total2 - split:.2f} SAR")
        else:
            print("You're all settled up!")

    elif choice == "7":
        print("Exiting... Have a fair day!")
        break

    else:
        print("Invalid option. Try again.")
