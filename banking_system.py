import random
import datetime

# In-memory storage for bank accounts
# Structure:
# accounts = {
#     account_number (int): {
#         "name": str,
#         "phone": str,
#         "pin": str,
#         "balance": float,
#         "transactions": list of dicts
#     }
# }
accounts = {}


def generate_account_number():
    """Generate a unique 8-digit bank account number."""
    while True:
        acc_num = random.randint(10000000, 99999999)
        if acc_num not in accounts:
            return acc_num


def record_transaction(account_number, trans_type, amount, details=""):
    """
    Record a timestamped transaction in the account's transaction history.
    
    Parameters:
      account_number (int): The target account number
      trans_type (str): Type of transaction ('DEPOSIT', 'WITHDRAWAL', 'TRANSFER_SENT', 'TRANSFER_RECEIVED')
      amount (float): Amount involved in the transaction
      details (str): Additional description (e.g. transfer recipient/sender)
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_balance = accounts[account_number]["balance"]
    
    transaction_entry = {
        "timestamp": now,
        "type": trans_type,
        "amount": amount,
        "details": details,
        "balance_after": current_balance
    }
    accounts[account_number]["transactions"].append(transaction_entry)


def create_account():
    """Prompt user for details and create a new bank account."""
    print("\n" + "=" * 50)
    print("           CREATE NEW BANK ACCOUNT")
    print("=" * 50)
    
    # 1. Enter and validate full name
    while True:
        name = input("Enter Full Name: ").strip()
        if len(name) >= 2 and all(part.isalpha() for part in name.split()):
            break
        print("[!] Invalid Name. Please enter alphabetic characters only.")

    # 2. Enter and validate 10-digit phone number
    while True:
        phone = input("Enter 10-digit Phone Number: ").strip()
        if phone.isdigit() and len(phone) == 10:
            break
        print("[!] Invalid Phone Number. Must be exactly 10 digits.")

    # 3. Create and confirm 4-digit security PIN
    while True:
        pin = input("Create 4-digit PIN: ").strip()
        if not (pin.isdigit() and len(pin) == 4):
            print("[!] PIN must be exactly 4 numeric digits.")
            continue
        
        confirm_pin = input("Confirm 4-digit PIN: ").strip()
        if pin == confirm_pin:
            break
        print("[!] PINs do not match. Please try again.")

    # 4. Optional initial deposit
    initial_balance = 0.0
    while True:
        init_dep_input = input("Enter Initial Deposit Amount (Min 0): ").strip()
        if not init_dep_input:
            initial_balance = 0.0
            break
        try:
            val = float(init_dep_input)
            if val >= 0:
                initial_balance = val
                break
            else:
                print("[!] Amount cannot be negative.")
        except ValueError:
            print("[!] Please enter a valid numerical amount.")

    # Generate unique account number and store record
    account_number = generate_account_number()
    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": initial_balance,
        "transactions": []
    }

    if initial_balance > 0:
        record_transaction(account_number, "DEPOSIT", initial_balance, "Initial Account Opening Deposit")

    print("\n" + "-" * 50)
    print("[SUCCESS] Account Created Successfully!")
    print(f"  Account Holder Name : {name}")
    print(f"  Account Number      : {account_number}")
    print(f"  Phone Number        : {phone}")
    print(f"  Current Balance     : Rs. {initial_balance:.2f}")
    print("-" * 50)
    print("[NOTE] Please save your Account Number and PIN securely for login.")


def login():
    """Authenticate user with Account Number and PIN."""
    print("\n" + "=" * 50)
    print("                ACCOUNT LOGIN")
    print("=" * 50)
    
    acc_input = input("Enter Account Number: ").strip()
    if not acc_input.isdigit():
        print("[!] Invalid account number format.")
        return None

    account_number = int(acc_input)
    if account_number not in accounts:
        print("[!] Account number not found. Please create an account first.")
        return None

    pin = input("Enter 4-digit PIN: ").strip()
    if accounts[account_number]["pin"] == pin:
        print(f"\n[SUCCESS] Welcome back, {accounts[account_number]['name']}! Login successful.")
        return account_number
    else:
        print("[!] Incorrect PIN. Access denied.")
        return None


def check_balance(account_number):
    """Display the current available balance for the logged-in account."""
    acc = accounts[account_number]
    print("\n" + "-" * 40)
    print(f"Account Holder : {acc['name']}")
    print(f"Account Number : {account_number}")
    print(f"Current Balance: Rs. {acc['balance']:.2f}")
    print("-" * 40)


def deposit_money(account_number):
    """Deposit money into the user's account."""
    print("\n" + "-" * 40)
    print("               DEPOSIT MONEY")
    print("-" * 40)
    
    try:
        amount = float(input("Enter amount to deposit (Rs.): ").strip())
        if amount <= 0:
            print("[!] Deposit amount must be greater than zero.")
            return

        accounts[account_number]["balance"] += amount
        record_transaction(account_number, "DEPOSIT", amount, "Cash Deposit")
        
        print(f"\n[SUCCESS] Rs. {amount:.2f} deposited successfully!")
        print(f"  Updated Balance: Rs. {accounts[account_number]['balance']:.2f}")
    except ValueError:
        print("[!] Invalid input. Please enter a valid numeric amount.")


def withdraw_money(account_number):
    """Withdraw money from the user's account after verifying sufficient funds."""
    print("\n" + "-" * 40)
    print("              WITHDRAW MONEY")
    print("-" * 40)
    
    try:
        amount = float(input("Enter amount to withdraw (Rs.): ").strip())
        if amount <= 0:
            print("[!] Withdrawal amount must be greater than zero.")
            return

        current_balance = accounts[account_number]["balance"]
        if amount > current_balance:
            print(f"[!] Insufficient funds! Your available balance is Rs. {current_balance:.2f}.")
            return

        accounts[account_number]["balance"] -= amount
        record_transaction(account_number, "WITHDRAWAL", amount, "Cash Withdrawal")
        
        print(f"\n[SUCCESS] Rs. {amount:.2f} withdrawn successfully!")
        print(f"  Remaining Balance: Rs. {accounts[account_number]['balance']:.2f}")
    except ValueError:
        print("[!] Invalid input. Please enter a valid numeric amount.")


def transfer_money(account_number):
    """Transfer funds from the logged-in account to another registered account."""
    print("\n" + "-" * 40)
    print("             TRANSFER MONEY")
    print("-" * 40)
    
    rec_input = input("Enter Receiver's 8-digit Account Number: ").strip()
    if not rec_input.isdigit():
        print("[!] Invalid account number format.")
        return

    receiver_acc = int(rec_input)
    if receiver_acc == account_number:
        print("[!] You cannot transfer money to your own account.")
        return

    if receiver_acc not in accounts:
        print("[!] Receiver account number not found in system.")
        return

    receiver_name = accounts[receiver_acc]["name"]
    print(f"Receiver Found: {receiver_name}")

    try:
        amount = float(input("Enter amount to transfer (Rs.): ").strip())
        if amount <= 0:
            print("[!] Transfer amount must be greater than zero.")
            return

        sender_balance = accounts[account_number]["balance"]
        if amount > sender_balance:
            print(f"[!] Transfer failed. Insufficient funds! Available balance: Rs. {sender_balance:.2f}.")
            return

        # Perform Transfer
        accounts[account_number]["balance"] -= amount
        accounts[receiver_acc]["balance"] += amount

        # Log for Sender
        record_transaction(
            account_number,
            "TRANSFER_SENT",
            amount,
            f"Transferred to {receiver_name} (Acc: {receiver_acc})"
        )
        # Log for Receiver
        record_transaction(
            receiver_acc,
            "TRANSFER_RECEIVED",
            amount,
            f"Received from {accounts[account_number]['name']} (Acc: {account_number})"
        )

        print(f"\n[SUCCESS] Successfully transferred Rs. {amount:.2f} to {receiver_name} (Acc: {receiver_acc})!")
        print(f"  Your Updated Balance: Rs. {accounts[account_number]['balance']:.2f}")
    except ValueError:
        print("[!] Invalid input. Please enter a valid numeric amount.")


def view_transaction_history(account_number):
    """Display a formatted ledger of all transactions for the account."""
    acc = accounts[account_number]
    transactions = acc["transactions"]

    print("\n" + "=" * 80)
    print(f"             TRANSACTION HISTORY FOR ACCOUNT: {account_number}")
    print("=" * 80)

    if not transactions:
        print("No transactions recorded yet.")
        print("=" * 80)
        return

    print(f"{'Date & Time':<20} | {'Type':<18} | {'Amount (Rs.)':<14} | {'Balance (Rs.)':<14} | {'Details'}")
    print("-" * 80)

    for tx in transactions:
        t_time = tx["timestamp"]
        t_type = tx["type"]
        t_amt = f"Rs. {tx['amount']:.2f}"
        t_bal = f"Rs. {tx['balance_after']:.2f}"
        t_details = tx["details"]
        print(f"{t_time:<20} | {t_type:<18} | {t_amt:<14} | {t_bal:<14} | {t_details}")

    print("=" * 80)
    print(f"Current Net Balance: Rs. {acc['balance']:.2f}")
    print("=" * 80)


def change_pin(account_number):
    """Allow user to update their 4-digit PIN after verifying the old PIN."""
    print("\n" + "-" * 40)
    print("               CHANGE PIN")
    print("-" * 40)

    old_pin = input("Enter Old 4-digit PIN: ").strip()
    if accounts[account_number]["pin"] != old_pin:
        print("[!] Incorrect Old PIN. Operation cancelled.")
        return

    new_pin = input("Enter New 4-digit PIN: ").strip()
    if not (new_pin.isdigit() and len(new_pin) == 4):
        print("[!] New PIN must be exactly 4 numeric digits.")
        return

    if new_pin == old_pin:
        print("[!] New PIN cannot be the same as the old PIN.")
        return

    confirm_new_pin = input("Confirm New 4-digit PIN: ").strip()
    if new_pin != confirm_new_pin:
        print("[!] PIN confirmation mismatch. Operation cancelled.")
        return

    accounts[account_number]["pin"] = new_pin
    print("\n[SUCCESS] PIN changed successfully! Please use your new PIN for future logins.")


def account_menu(account_number):
    """
    Sub-menu for an authenticated bank account session.
    
    Menu Options:
      1. Check Balance
      2. Deposit
      3. Withdraw
      4. Transfer
      5. Transaction History
      6. Change PIN
      7. Logout
    """
    while True:
        acc_name = accounts[account_number]["name"]
        print("\n" + "=" * 45)
        print(f"  ACCOUNT MENU | User: {acc_name} ({account_number})")
        print("=" * 45)
        print("  1. Check Balance")
        print("  2. Deposit")
        print("  3. Withdraw")
        print("  4. Transfer")
        print("  5. Transaction History")
        print("  6. Change PIN")
        print("  7. Logout")
        print("=" * 45)

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            check_balance(account_number)
        elif choice == "2":
            deposit_money(account_number)
        elif choice == "3":
            withdraw_money(account_number)
        elif choice == "4":
            transfer_money(account_number)
        elif choice == "5":
            view_transaction_history(account_number)
        elif choice == "6":
            change_pin(account_number)
        elif choice == "7":
            print(f"\n[SUCCESS] Successfully logged out from Account {account_number}. Returning to Main Menu...")
            break
        else:
            print("[!] Invalid choice. Please enter a number between 1 and 7.")


def main_menu():
    """
    Main entry point and top-level navigation loop for the Banking Application.
    """
    print("\n" + "#" * 55)
    print("   WELCOME TO PYTHON BANKING SYSTEM - MINI PROJECT   ")
    print("#" * 55)

    while True:
        print("\n" + "=" * 45)
        print("                MAIN MENU")
        print("=" * 45)
        print("  1. Create a Bank Account")
        print("  2. Login to Account")
        print("  3. Exit Application")
        print("=" * 45)

        choice = input("Select an option (1-3): ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            logged_in_acc = login()
            if logged_in_acc is not None:
                account_menu(logged_in_acc)
        elif choice == "3":
            print("\nThank you for using Python Banking System. Have a great day!\n")
            break
        else:
            print("[!] Invalid option. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main_menu()
