"""
================================================================================
BANKING SYSTEM - DESKTOP GUI APPLICATION
================================================================================
A modern graphical user interface (GUI) built with Python's Tkinter & TTK.
Provides visual account creation, secure login, real-time balance tracking,
instant deposits/withdrawals, fund transfers, interactive transaction ledgers,
and PIN management.

Author: EWB Python with AI Internship Student
================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import random
import datetime

# In-memory storage for bank accounts
accounts = {}


def generate_account_number():
    """Generate a unique 8-digit bank account number."""
    while True:
        acc_num = random.randint(10000000, 99999999)
        if acc_num not in accounts:
            return acc_num


def record_transaction(account_number, trans_type, amount, details=""):
    """Record a timestamped transaction in the account's ledger."""
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


class BankingGUIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🏦 NextGen Banking System")
        self.geometry("900x650")
        self.minsize(850, 600)
        self.configure(bg="#0f172a")  # Slate-900 dark background

        self.current_user = None  # Holds logged-in account number

        self.setup_styles()
        self.create_widgets()

        # Seed sample demo account for immediate testing if empty
        self.seed_demo_accounts()

    def setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Configure colors
        self.style.configure(".", background="#0f172a", foreground="#f8fafc")
        self.style.configure("TFrame", background="#0f172a")
        self.style.configure("Card.TFrame", background="#1e293b", relief="flat")
        
        # Labels
        self.style.configure("TLabel", background="#0f172a", foreground="#f8fafc", font=("Segoe UI", 10))
        self.style.configure("Card.TLabel", background="#1e293b", foreground="#f8fafc", font=("Segoe UI", 10))
        self.style.configure("CardHeader.TLabel", background="#1e293b", foreground="#38bdf8", font=("Segoe UI", 12, "bold"))
        self.style.configure("CardValue.TLabel", background="#1e293b", foreground="#22c55e", font=("Segoe UI", 18, "bold"))
        self.style.configure("Title.TLabel", background="#0f172a", foreground="#38bdf8", font=("Segoe UI", 18, "bold"))
        self.style.configure("Subtitle.TLabel", background="#0f172a", foreground="#94a3b8", font=("Segoe UI", 10))

        # Buttons
        self.style.configure(
            "Primary.TButton",
            background="#2563eb",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0
        )
        self.style.map("Primary.TButton", background=[("active", "#1d4ed8")])

        self.style.configure(
            "Success.TButton",
            background="#16a34a",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0
        )
        self.style.map("Success.TButton", background=[("active", "#15803d")])

        self.style.configure(
            "Warning.TButton",
            background="#d97706",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0
        )
        self.style.map("Warning.TButton", background=[("active", "#b45309")])

        self.style.configure(
            "Danger.TButton",
            background="#dc2626",
            foreground="#ffffff",
            font=("Segoe UI", 10, "bold"),
            padding=8,
            borderwidth=0
        )
        self.style.map("Danger.TButton", background=[("active", "#b91c1c")])

        # Treeview (Ledger table)
        self.style.configure(
            "Treeview",
            background="#1e293b",
            foreground="#f8fafc",
            fieldbackground="#1e293b",
            rowheight=28,
            font=("Segoe UI", 9)
        )
        self.style.configure(
            "Treeview.Heading",
            background="#334155",
            foreground="#38bdf8",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )
        self.style.map("Treeview", background=[("selected", "#2563eb")])

    def seed_demo_accounts(self):
        """Seed demo account so user can immediately test or create their own."""
        demo_acc = 10001001
        accounts[demo_acc] = {
            "name": "Zainul Abideen",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 25000.0,
            "transactions": []
        }
        record_transaction(demo_acc, "DEPOSIT", 25000.0, "Opening Demo Balance")

        demo_acc_2 = 10002002
        accounts[demo_acc_2] = {
            "name": "Rahul Sharma",
            "phone": "9123456780",
            "pin": "4321",
            "balance": 15000.0,
            "transactions": []
        }
        record_transaction(demo_acc_2, "DEPOSIT", 15000.0, "Opening Demo Balance")

    def create_widgets(self):
        # Container frame
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Build Auth Screen and Dashboard Screen
        self.auth_frame = ttk.Frame(self.container)
        self.dashboard_frame = ttk.Frame(self.container)

        self.build_auth_screen()
        self.build_dashboard_screen()

        # Show Auth Screen initially
        self.show_auth_screen()

    # =========================================================================
    # AUTH SCREEN (LOGIN & CREATE ACCOUNT)
    # =========================================================================
    def build_auth_screen(self):
        # Title section
        header_frame = ttk.Frame(self.auth_frame)
        header_frame.pack(pady=(20, 30))

        ttk.Label(header_frame, text="🏦 NextGen Banking System", style="Title.TLabel").pack()
        ttk.Label(header_frame, text="Secure, Fast & Menu-Driven Digital Banking", style="Subtitle.TLabel").pack(pady=4)

        # Card container with two tabs/cards: Login & Create Account
        cards_row = ttk.Frame(self.auth_frame)
        cards_row.pack(fill="both", expand=True, padx=40)

        # --- LOGIN CARD ---
        login_card = ttk.Frame(cards_row, style="Card.TFrame", padding=25)
        login_card.pack(side="left", fill="both", expand=True, padx=(0, 15))

        ttk.Label(login_card, text="Account Login", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 15))

        ttk.Label(login_card, text="Account Number", style="Card.TLabel").pack(anchor="w", pady=(5, 2))
        self.login_acc_entry = tk.Entry(login_card, font=("Segoe UI", 11), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=5)
        self.login_acc_entry.pack(fill="x", pady=(0, 10))
        self.login_acc_entry.insert(0, "10001001")  # Demo pre-fill

        ttk.Label(login_card, text="4-digit Security PIN", style="Card.TLabel").pack(anchor="w", pady=(5, 2))
        self.login_pin_entry = tk.Entry(login_card, font=("Segoe UI", 11), show="•", bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=5)
        self.login_pin_entry.pack(fill="x", pady=(0, 20))
        self.login_pin_entry.insert(0, "1234")  # Demo pre-fill

        ttk.Button(login_card, text="🔐 Login to Account", style="Primary.TButton", command=self.handle_login).pack(fill="x", pady=5)
        ttk.Label(login_card, text="(Demo: Acc: 10001001 / PIN: 1234)", style="Subtitle.TLabel").pack(pady=5)

        # --- CREATE ACCOUNT CARD ---
        register_card = ttk.Frame(cards_row, style="Card.TFrame", padding=25)
        register_card.pack(side="right", fill="both", expand=True, padx=(15, 0))

        ttk.Label(register_card, text="Create New Account", style="CardHeader.TLabel").pack(anchor="w", pady=(0, 15))

        ttk.Label(register_card, text="Full Name", style="Card.TLabel").pack(anchor="w", pady=(2, 2))
        self.reg_name_entry = tk.Entry(register_card, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=4)
        self.reg_name_entry.pack(fill="x", pady=(0, 8))

        ttk.Label(register_card, text="10-digit Phone Number", style="Card.TLabel").pack(anchor="w", pady=(2, 2))
        self.reg_phone_entry = tk.Entry(register_card, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=4)
        self.reg_phone_entry.pack(fill="x", pady=(0, 8))

        # PIN & Confirm PIN side by side
        pin_row = ttk.Frame(register_card, style="Card.TFrame")
        pin_row.pack(fill="x", pady=(0, 8))

        p_left = ttk.Frame(pin_row, style="Card.TFrame")
        p_left.pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Label(p_left, text="4-digit PIN", style="Card.TLabel").pack(anchor="w")
        self.reg_pin_entry = tk.Entry(p_left, font=("Segoe UI", 10), show="•", bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=4)
        self.reg_pin_entry.pack(fill="x")

        p_right = ttk.Frame(pin_row, style="Card.TFrame")
        p_right.pack(side="right", fill="x", expand=True, padx=(5, 0))
        ttk.Label(p_right, text="Confirm PIN", style="Card.TLabel").pack(anchor="w")
        self.reg_conf_pin_entry = tk.Entry(p_right, font=("Segoe UI", 10), show="•", bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=4)
        self.reg_conf_pin_entry.pack(fill="x")

        ttk.Label(register_card, text="Initial Deposit (Rs., optional)", style="Card.TLabel").pack(anchor="w", pady=(2, 2))
        self.reg_deposit_entry = tk.Entry(register_card, font=("Segoe UI", 10), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", bd=4)
        self.reg_deposit_entry.pack(fill="x", pady=(0, 15))

        ttk.Button(register_card, text="➕ Create Account", style="Success.TButton", command=self.handle_register).pack(fill="x", pady=5)

    def handle_login(self):
        acc_str = self.login_acc_entry.get().strip()
        pin = self.login_pin_entry.get().strip()

        if not acc_str.isdigit():
            messagebox.showerror("Error", "Please enter a valid numeric Account Number.")
            return

        acc_num = int(acc_str)
        if acc_num not in accounts:
            messagebox.showerror("Error", f"Account Number {acc_num} not found!")
            return

        if accounts[acc_num]["pin"] != pin:
            messagebox.showerror("Authentication Failed", "Incorrect 4-digit PIN! Please try again.")
            return

        self.current_user = acc_num
        messagebox.showinfo("Login Success", f"Welcome back, {accounts[acc_num]['name']}!")
        self.show_dashboard_screen()

    def handle_register(self):
        name = self.reg_name_entry.get().strip()
        phone = self.reg_phone_entry.get().strip()
        pin = self.reg_pin_entry.get().strip()
        conf_pin = self.reg_conf_pin_entry.get().strip()
        dep_str = self.reg_deposit_entry.get().strip()

        # Validations
        if len(name) < 2 or not all(part.isalpha() for part in name.split()):
            messagebox.showerror("Validation Error", "Full Name must contain only alphabetic characters.")
            return

        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Validation Error", "Phone number must be exactly 10 digits.")
            return

        if not (pin.isdigit() and len(pin) == 4):
            messagebox.showerror("Validation Error", "PIN must be exactly 4 numeric digits.")
            return

        if pin != conf_pin:
            messagebox.showerror("Validation Error", "PIN and Confirm PIN do not match.")
            return

        initial_deposit = 0.0
        if dep_str:
            try:
                val = float(dep_str)
                if val < 0:
                    messagebox.showerror("Validation Error", "Initial deposit cannot be negative.")
                    return
                initial_deposit = val
            except ValueError:
                messagebox.showerror("Validation Error", "Initial deposit must be a valid number.")
                return

        # Generate Account Number
        acc_num = generate_account_number()
        accounts[acc_num] = {
            "name": name,
            "phone": phone,
            "pin": pin,
            "balance": initial_deposit,
            "transactions": []
        }

        if initial_deposit > 0:
            record_transaction(acc_num, "DEPOSIT", initial_deposit, "Initial Account Opening Deposit")

        messagebox.showinfo(
            "Account Created Successfully",
            f"🎉 Congratulations, {name}!\n\n"
            f"Your New Account Number : {acc_num}\n"
            f"Registered Phone        : {phone}\n"
            f"Opening Balance         : Rs. {initial_deposit:.2f}\n\n"
            f"Please remember your Account Number and PIN to log in."
        )

        # Clear inputs and switch to login
        self.reg_name_entry.delete(0, tk.END)
        self.reg_phone_entry.delete(0, tk.END)
        self.reg_pin_entry.delete(0, tk.END)
        self.reg_conf_pin_entry.delete(0, tk.END)
        self.reg_deposit_entry.delete(0, tk.END)

        self.login_acc_entry.delete(0, tk.END)
        self.login_acc_entry.insert(0, str(acc_num))
        self.login_pin_entry.delete(0, tk.END)
        self.login_pin_entry.insert(0, pin)

    # =========================================================================
    # DASHBOARD SCREEN
    # =========================================================================
    def build_dashboard_screen(self):
        # Top Header Bar (User info + Logout)
        top_bar = ttk.Frame(self.dashboard_frame)
        top_bar.pack(fill="x", pady=(0, 15))

        self.user_greeting_label = ttk.Label(top_bar, text="Welcome, User", style="Title.TLabel")
        self.user_greeting_label.pack(side="left")

        ttk.Button(top_bar, text="🚪 Logout", style="Danger.TButton", command=self.handle_logout).pack(side="right")

        # Stats Cards Row (Balance, Account Number, Phone)
        stats_row = ttk.Frame(self.dashboard_frame)
        stats_row.pack(fill="x", pady=(0, 15))

        # Balance Card
        bal_card = ttk.Frame(stats_row, style="Card.TFrame", padding=15)
        bal_card.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ttk.Label(bal_card, text="AVAILABLE BALANCE", style="Subtitle.TLabel").pack(anchor="w")
        self.balance_val_label = ttk.Label(bal_card, text="Rs. 0.00", style="CardValue.TLabel")
        self.balance_val_label.pack(anchor="w", pady=(5, 0))

        # Account No Card
        acc_card = ttk.Frame(stats_row, style="Card.TFrame", padding=15)
        acc_card.pack(side="left", fill="both", expand=True, padx=5)
        ttk.Label(acc_card, text="ACCOUNT NUMBER", style="Subtitle.TLabel").pack(anchor="w")
        self.acc_val_label = ttk.Label(acc_card, text="--------", style="CardHeader.TLabel")
        self.acc_val_label.pack(anchor="w", pady=(5, 0))

        # Phone Card
        phone_card = ttk.Frame(stats_row, style="Card.TFrame", padding=15)
        phone_card.pack(side="left", fill="both", expand=True, padx=(10, 0))
        ttk.Label(phone_card, text="REGISTERED PHONE", style="Subtitle.TLabel").pack(anchor="w")
        self.phone_val_label = ttk.Label(phone_card, text="----------", style="CardHeader.TLabel")
        self.phone_val_label.pack(anchor="w", pady=(5, 0))

        # Quick Action Buttons Bar
        action_bar = ttk.Frame(self.dashboard_frame)
        action_bar.pack(fill="x", pady=(0, 15))

        ttk.Button(action_bar, text="➕ Deposit Money", style="Success.TButton", command=self.gui_deposit).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(action_bar, text="➖ Withdraw Money", style="Warning.TButton", command=self.gui_withdraw).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(action_bar, text="🔁 Transfer Funds", style="Primary.TButton", command=self.gui_transfer).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(action_bar, text="🔑 Change PIN", style="Primary.TButton", command=self.gui_change_pin).pack(side="left", fill="x", expand=True, padx=(5, 0))

        # Ledger & Transaction History Table
        history_header = ttk.Frame(self.dashboard_frame)
        history_header.pack(fill="x", pady=(5, 5))
        ttk.Label(history_header, text="📜 Transaction History Ledger", style="CardHeader.TLabel").pack(side="left")
        ttk.Button(history_header, text="🔄 Refresh", style="Primary.TButton", command=self.refresh_dashboard).pack(side="right")

        # Table Frame with Scrollbar
        table_frame = ttk.Frame(self.dashboard_frame)
        table_frame.pack(fill="both", expand=True)

        columns = ("timestamp", "type", "amount", "balance", "details")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("timestamp", text="Date & Time")
        self.tree.heading("type", text="Type")
        self.tree.heading("amount", text="Amount (Rs.)")
        self.tree.heading("balance", text="Balance (Rs.)")
        self.tree.heading("details", text="Transaction Details")

        self.tree.column("timestamp", width=160, anchor="center")
        self.tree.column("type", width=140, anchor="center")
        self.tree.column("amount", width=120, anchor="e")
        self.tree.column("balance", width=120, anchor="e")
        self.tree.column("details", width=260, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_dashboard(self):
        if not self.current_user or self.current_user not in accounts:
            return

        user_data = accounts[self.current_user]
        self.user_greeting_label.config(text=f"Welcome, {user_data['name']}!")
        self.balance_val_label.config(text=f"Rs. {user_data['balance']:,.2f}")
        self.acc_val_label.config(text=str(self.current_user))
        self.phone_val_label.config(text=user_data['phone'])

        # Populate transaction treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for tx in reversed(user_data["transactions"]):
            self.tree.insert(
                "",
                "end",
                values=(
                    tx["timestamp"],
                    tx["type"],
                    f"Rs. {tx['amount']:,.2f}",
                    f"Rs. {tx['balance_after']:,.2f}",
                    tx["details"]
                )
            )

    # --- Banking Operations via GUI Dialogs ---
    def gui_deposit(self):
        amt_str = simpledialog.askstring("Deposit Money", "Enter amount to deposit (Rs.):", parent=self)
        if amt_str is None:
            return
        try:
            amt = float(amt_str.strip())
            if amt <= 0:
                messagebox.showerror("Error", "Deposit amount must be greater than zero.", parent=self)
                return
            accounts[self.current_user]["balance"] += amt
            record_transaction(self.current_user, "DEPOSIT", amt, "Cash Deposit")
            self.refresh_dashboard()
            messagebox.showinfo("Success", f"Rs. {amt:,.2f} deposited successfully!", parent=self)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.", parent=self)

    def gui_withdraw(self):
        amt_str = simpledialog.askstring("Withdraw Money", "Enter amount to withdraw (Rs.):", parent=self)
        if amt_str is None:
            return
        try:
            amt = float(amt_str.strip())
            if amt <= 0:
                messagebox.showerror("Error", "Withdrawal amount must be greater than zero.", parent=self)
                return
            current_bal = accounts[self.current_user]["balance"]
            if amt > current_bal:
                messagebox.showerror("Insufficient Funds", f"Cannot withdraw Rs. {amt:,.2f}. Available balance: Rs. {current_bal:,.2f}.", parent=self)
                return

            accounts[self.current_user]["balance"] -= amt
            record_transaction(self.current_user, "WITHDRAWAL", amt, "Cash Withdrawal")
            self.refresh_dashboard()
            messagebox.showinfo("Success", f"Rs. {amt:,.2f} withdrawn successfully!", parent=self)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.", parent=self)

    def gui_transfer(self):
        rec_str = simpledialog.askstring("Transfer Funds", "Enter Receiver's 8-digit Account Number:", parent=self)
        if rec_str is None:
            return
        if not rec_str.isdigit():
            messagebox.showerror("Error", "Invalid Account Number format.", parent=self)
            return
        receiver_acc = int(rec_str)

        if receiver_acc == self.current_user:
            messagebox.showerror("Error", "You cannot transfer funds to your own account.", parent=self)
            return

        if receiver_acc not in accounts:
            messagebox.showerror("Error", f"Receiver Account {receiver_acc} does not exist in the system.", parent=self)
            return

        receiver_name = accounts[receiver_acc]["name"]
        amt_str = simpledialog.askstring("Transfer Funds", f"Receiver: {receiver_name}\nEnter amount to transfer (Rs.):", parent=self)
        if amt_str is None:
            return

        try:
            amt = float(amt_str.strip())
            if amt <= 0:
                messagebox.showerror("Error", "Transfer amount must be greater than zero.", parent=self)
                return

            sender_bal = accounts[self.current_user]["balance"]
            if amt > sender_bal:
                messagebox.showerror("Insufficient Funds", f"Transfer failed. Available balance: Rs. {sender_bal:,.2f}.", parent=self)
                return

            # Perform Transfer
            accounts[self.current_user]["balance"] -= amt
            accounts[receiver_acc]["balance"] += amt

            # Dual records
            record_transaction(self.current_user, "TRANSFER_SENT", amt, f"Transferred to {receiver_name} (Acc: {receiver_acc})")
            record_transaction(receiver_acc, "TRANSFER_RECEIVED", amt, f"Received from {accounts[self.current_user]['name']} (Acc: {self.current_user})")

            self.refresh_dashboard()
            messagebox.showinfo("Transfer Successful", f"Successfully transferred Rs. {amt:,.2f} to {receiver_name} (Acc: {receiver_acc})!", parent=self)
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.", parent=self)

    def gui_change_pin(self):
        old_pin = simpledialog.askstring("Change PIN", "Enter Old 4-digit PIN:", show="•", parent=self)
        if old_pin is None:
            return
        if accounts[self.current_user]["pin"] != old_pin.strip():
            messagebox.showerror("Error", "Incorrect Old PIN.", parent=self)
            return

        new_pin = simpledialog.askstring("Change PIN", "Enter New 4-digit PIN:", show="•", parent=self)
        if new_pin is None:
            return
        new_pin = new_pin.strip()
        if not (new_pin.isdigit() and len(new_pin) == 4):
            messagebox.showerror("Error", "New PIN must be exactly 4 numeric digits.", parent=self)
            return

        if new_pin == old_pin:
            messagebox.showerror("Error", "New PIN cannot be the same as the old PIN.", parent=self)
            return

        conf_pin = simpledialog.askstring("Change PIN", "Confirm New 4-digit PIN:", show="•", parent=self)
        if conf_pin is None:
            return
        if new_pin != conf_pin.strip():
            messagebox.showerror("Error", "PIN confirmation mismatch.", parent=self)
            return

        accounts[self.current_user]["pin"] = new_pin
        messagebox.showinfo("Success", "PIN updated successfully! Use your new PIN for next login.", parent=self)

    def handle_logout(self):
        self.current_user = None
        self.show_auth_screen()

    # --- Screen Navigation ---
    def show_auth_screen(self):
        self.dashboard_frame.pack_forget()
        self.auth_frame.pack(fill="both", expand=True)

    def show_dashboard_screen(self):
        self.auth_frame.pack_forget()
        self.dashboard_frame.pack(fill="both", expand=True)
        self.refresh_dashboard()


if __name__ == "__main__":
    app = BankingGUIApp()
    app.mainloop()
