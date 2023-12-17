import os
import json
from datetime import datetime

# File path for storing account information
account_file_path = "accounts.json"

def load_accounts():
    if os.path.exists(account_file_path):
        with open(account_file_path, "r") as file:
            return json.load(file)
    else:
        return {}

def save_accounts(accounts):
    with open(account_file_path, "w") as file:
        json.dump(accounts, file, indent=2)

def main_menu():
    print("*************************** Welcome to ATM System ************************")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")


def create_account():
    name = input("Enter your name: ")
    initial_balance = float(input("Enter initial balance: "))

    account_number = str(hash(name))

    account = {"name": name, "balance": initial_balance, "transactions": []}

    accounts[account_number] = account
    save_accounts(accounts)

    print(f"Account created successfully. Your account number is: {account_number}")


def login():
    account_number = input("Enter your account number: ")

    # Check if the account number exists in the accounts dictionary
    if account_number in accounts:
        print(f"Welcome, {accounts[account_number]['name']}!")
        account_menu(account_number)
    else:
        print("Account not found. Please check your account number.")


def account_menu(account_number):
    while True:
        print("==== Account Menu ====")
        print("1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. Transfer Money")
        print("5. Check Transaction History")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print(f"Current Balance: {accounts[account_number]['balance']}")
        elif choice == "2":
            amount = float(input("Enter the amount to withdraw: "))
            if amount <= accounts[account_number]['balance']:
                accounts[account_number]['balance'] -= amount
                accounts[account_number]['transactions'].append({"type": "withdrawal", "amount": amount, "timestamp": str(datetime.now())})
                save_accounts(accounts)
                print(f"Withdrawal successful. New balance: {accounts[account_number]['balance']}")
            else:
                print("Insufficient funds.")
        elif choice == "3":
            amount = float(input("Enter the amount to deposit: "))
            accounts[account_number]['balance'] += amount
            accounts[account_number]['transactions'].append({"type": "deposit", "amount": amount, "timestamp": str(datetime.now())})
            save_accounts(accounts)
            print(f"Deposit successful. New balance: {accounts[account_number]['balance']}")
        elif choice == "4":
            target_account_number = input("Enter the target account number: ")
            if target_account_number in accounts:
                transfer_amount = float(input("Enter the amount to transfer: "))
                if transfer_amount <= accounts[account_number]['balance']:
                    accounts[account_number]['balance'] -= transfer_amount
                    accounts[target_account_number]['balance'] += transfer_amount
                    timestamp = str(datetime.now())
                    accounts[account_number]['transactions'].append({"type": "transfer", "amount": transfer_amount, "target_account": target_account_number, "timestamp": timestamp})
                    accounts[target_account_number]['transactions'].append({"type": "receive_transfer", "amount": transfer_amount, "source_account": account_number, "timestamp": timestamp})
                    save_accounts(accounts)
                    print(f"Transfer successful. New balance: {accounts[account_number]['balance']}")
                else:
                    print("Insufficient funds for transfer.")
            else:
                print("Target account not found.")
        elif choice == "5":
            print("==== Transaction History ====")
            for transaction in accounts[account_number]['transactions']:
                print(f"{transaction['timestamp']} - {transaction['type']}: {transaction['amount']}")
        elif choice == "6":
            print("Logout successful.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

accounts = load_accounts()

while True:
    main_menu()
    user_choice = input("Enter your choice: ")

    if user_choice == "1":
        create_account()
    elif user_choice == "2":
        login()
    elif user_choice == "3":
        print("Exiting the ATM system. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a valid option.")
