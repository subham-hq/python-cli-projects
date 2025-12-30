import json
import time
from datetime import datetime


# ==========================================================
# DATA LOADING
# ==========================================================
# Load expense data once at program start.
# Keeping file operations minimal is a good practice.
try:
    with open("expenses.json", "r") as json_file:
        data = json.load(json_file)
except FileNotFoundError:
    print("Error: expenses.json file not found.")
    exit()


# ==========================================================
# UTILITY: LOADING ANIMATIONS (UX IMPROVEMENT)
# ==========================================================
def loading_animation_save(duration=3):
    print("Saving Data", end="")
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\nDone!")


def loading_animation_del(duration=3):
    print("Deleting Data", end="")
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\nDone!")


def loading_animation_flush(duration=3):
    print("Loading", end="")
    for _ in range(duration):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print("\nDone!\n")


# ==========================================================
# 1. ADD EXPENSE
# ==========================================================
def run_task_one():
    """
    Adds a new expense after validating user input.
    """

    new_date = input("Enter Date (YYYY-MM-DD): ")
    new_category = input("Enter Category: ").strip().capitalize()
    new_description = input("Enter Description: ")
    new_amount = input("Enter Amount: ")

    # --- Local Validators (acceptable for CLI scope) ---
    def validate_date(date_value):
        try:
            datetime.strptime(date_value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def validate_amount(amount_value):
        try:
            float(amount_value)
            return True
        except ValueError:
            return False

    # --- Validation ---
    if not validate_date(new_date):
        print("Error: Invalid date format. Use YYYY-MM-DD.")
        return

    if new_category not in data["categories"]:
        print("Error: Category not found.")
        return

    if not validate_amount(new_amount):
        print("Error: Amount must be numeric.")
        return

    # --- Transaction ID Handling (safe even if empty) ---
    if data["expenses"]:
        new_id = max(exp["id"] for exp in data["expenses"]) + 1
    else:
        new_id = 1

    # --- Create Expense Record ---
    new_expense = {
        "id": new_id,
        "date": new_date,
        "category": new_category,
        "description": new_description.capitalize(),
        "amount": float(new_amount)
    }

    data["expenses"].append(new_expense)

    with open("expenses.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    loading_animation_save()
    print("Expense recorded successfully.")


# ==========================================================
# 2. REMOVE EXPENSE
# ==========================================================
def run_task_two():
    """
    Deletes an expense using transaction ID.
    """

    try:
        target_id = int(input("Enter the Transaction ID to delete: "))
    except ValueError:
        print("Error: Transaction ID must be a number.")
        return

    for expense in data["expenses"]:
        if expense["id"] == target_id:
            print(
                f"Deleting expense ID {expense['id']} | "
                f"{expense['category']} | {expense['description']} | INR {expense['amount']}"
            )
            data["expenses"].remove(expense)

            with open("expenses.json", "w") as json_file:
                json.dump(data, json_file, indent=4)

            loading_animation_del()
            print("Expense deleted successfully.")
            return

    print(f"Error: Transaction ID {target_id} not found.")


# ==========================================================
# 3. VIEW ALL EXPENSES
# ==========================================================
def run_task_three():
    print("Showing All Expenses:\n")
    loading_animation_flush()

    for txn in data["expenses"]:
        print(
            f"Txn ID: {txn['id']} | Date: {txn['date']} | "
            f"Category: {txn['category']} | Amount: {txn['amount']}"
        )
        print("-" * 30)


# ==========================================================
# 4. FILTER BY CATEGORY
# ==========================================================
def run_task_four():
    print("\n--- FILTER BY CATEGORY ---")

    for idx, cat in enumerate(data["categories"], 1):
        print(f"{idx}. {cat}")
    print(f"{len(data['categories']) + 1}. Return to Main Menu")

    try:
        choice = int(input("Select Category: "))
    except ValueError:
        print("Invalid input.")
        return

    if choice == len(data["categories"]) + 1:
        return

    if not (1 <= choice <= len(data["categories"])):
        print("Invalid category selection.")
        return

    selected_category = data["categories"][choice - 1]
    total = 0
    found = False

    for txn in data["expenses"]:
        if txn["category"] == selected_category:
            print(
                f"Txn ID: {txn['id']} | Date: {txn['date']} | "
                f"{txn['description']} | Amount: {txn['amount']}"
            )
            total += txn["amount"]
            found = True

    if found:
        print("-" * 30)
        print(f"Total spent on {selected_category}: {total}")
    else:
        print(f"No transactions found for {selected_category}.")


# ==========================================================
# 5. FILTER BY DATE
# ==========================================================
def run_task_five():
    date_search = input("Enter Date (YYYY-MM-DD): ")

    try:
        datetime.strptime(date_search, "%Y-%m-%d")
    except ValueError:
        print("Invalid date format.")
        return

    total = 0
    found = False

    for txn in data["expenses"]:
        if txn["date"] == date_search:
            print(
                f"Txn ID: {txn['id']} | Category: {txn['category']} | "
                f"Amount: {txn['amount']}"
            )
            total += txn["amount"]
            found = True

    if found:
        print("-" * 30)
        print(f"Total spent on {date_search}: {total}")
    else:
        print("No transactions found on this date.")


# ==========================================================
# 6. VIEW ALL CATEGORIES
# ==========================================================
def run_task_six():
    print("All categories:")
    for idx, category in enumerate(data["categories"], 1):
        print(f"{idx}. {category}")
    print("-" * 30)


# ==========================================================
# 7. ABOUT PROJECT
# ==========================================================
def run_task_seven():
    meta = data["metadata"]
    print(
        f"\nAbout This Project\n"
        f"Currency: {meta['currency']}\n"
        f"Created By: {meta['created_by']}\n"
        f"Created On: {meta['created_on']}\n"
        f"Last Updated: {meta['last_updated']}"
    )
    print("-" * 30)


# ==========================================================
# MAIN MENU
# ==========================================================
def main():
    while True:
        print(
            "\nWelcome to Smart Expense Tracker!\n"
            "=== MAIN MENU ===\n"
            "1. Add Expense\n"
            "2. Remove Expense\n"
            "3. View All Expenses\n"
            "4. Filter by Category\n"
            "5. Filter by Date\n"
            "6. View All Categories\n"
            "7. About this Project\n"
            "8. Exit\n"
        )

        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            run_task_one()
        elif choice == "2":
            run_task_two()
        elif choice == "3":
            run_task_three()
        elif choice == "4":
            run_task_four()
        elif choice == "5":
            run_task_five()
        elif choice == "6":
            run_task_six()
        elif choice == "7":
            run_task_seven()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()