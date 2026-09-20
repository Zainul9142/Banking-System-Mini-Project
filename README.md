# 🏦 Banking System – Mini Project

A comprehensive Python-based banking application that simulates real-world banking operations. It provides **three interactive interfaces**:
1. 🖥️ **Desktop GUI Application (`gui_app.py`)** — Built with Python's Tkinter & TTK.
2. 🌐 **Modern Web Application (`web_app.py`)** — Built with Flask and Tailwind CSS.
3. ⚡ **Command-Line Interface (`banking_system.py`)** — Menu-driven console interface.

---

## 📌 Project Overview
The **Banking System Mini Project** combines core Python programming concepts into a unified, practical, and functional application. It replicates essential functionalities of banking portals and ATM software through both graphical and command-line interfaces.

---

## 🚀 Key Features

* 👤 **Create a Bank Account:**
  * Collects customer full name, 10-digit phone number, and a 4-digit PIN.
  * Automatically generates a unique 8-digit account number using Python's `random` module.
  * Allows an optional initial deposit.
* 🔐 **Secure Login Authentication:**
  * Login using unique Account Number and 4-digit PIN.
* 💰 **Check Account Balance:**
  * Displays the real-time account balance with currency formatting.
* ➕ **Deposit Money:**
  * Validates positive deposit amounts, updates current balance, and records a timestamped transaction.
* ➖ **Withdraw Money:**
  * Checks available balance before withdrawal to prevent overdrafts.
* 🔁 **Transfer Money Between Accounts:**
  * Validates receiver's account existence.
  * Checks sender's sufficient balance.
  * Performs atomic transfer (deducts from sender and credits receiver).
  * Records dual transaction records (Sender: `TRANSFER_SENT`, Receiver: `TRANSFER_RECEIVED`).
* 📜 **Transaction History Ledger:**
  * Tabular ledger showing `Date & Time` (via `datetime`), `Transaction Type`, `Amount`, `Post-Transaction Balance`, and `Details`.
* 🔑 **Change PIN:**
  * Validates old PIN before setting and confirming a new PIN.
* 🚪 **Session Management & Logout:**
  * Securely terminates the authenticated session and returns to the Main Menu.

---

## 🏗️ Application Workflow & Architecture

```
                       ┌─────────────────────────┐
                       │        MAIN MENU        │
                       │ 1. Create Bank Account  │
                       │ 2. Login to Account     │
                       │ 3. Exit Application     │
                       └────────────┬────────────┘
                                    │ (After Login)
                                    ▼
                       ┌─────────────────────────┐
                       │      ACCOUNT MENU       │
                       ├─────────────────────────┤
                       │ 1. Check Balance        │
                       │ 2. Deposit Money        │
                       │ 3. Withdraw Money       │
                       │ 4. Transfer Money       │
                       │ 5. Transaction History  │
                       │ 6. Change PIN           │
                       │ 7. Logout               │
                       └────────────┬────────────┘
                                    │ (On Logout)
                                    ▼
                       ┌─────────────────────────┐
                       │    Return to Main Menu  │
                       └─────────────────────────┘
```

---

## 🐍 Python Concepts & Modules Used

| Concept / Module | Implementation in Project |
| :--- | :--- |
| **Variables & Data Types** | Integers, Floats, Strings, Booleans for user details, account balances, and status flags |
| **Conditional Statements** | `if`, `elif`, `else` for PIN authentication, input validation, and balance checks |
| **Loops** | `while` loops for menu persistence and re-prompting on invalid inputs |
| **Functions** | Modular function design (`create_account`, `login`, `deposit_money`, `withdraw_money`, `transfer_money`, etc.) |
| **Data Structures** | Nested **Dictionaries** for account storage and **Lists** for transaction logs |
| **GUI & Web Frameworks** | **Tkinter / TTK** for desktop interface, **Flask** for web dashboard |
| **`random` Module** | Auto-generating non-colliding 8-digit account numbers |
| **`datetime` Module** | Recording exact timestamps for each transaction record |

---

## 📁 Project Structure

```
PythonAI/
│
├── gui_app.py              # 🖥️ Desktop GUI Application (Tkinter)
├── web_app.py              # 🌐 Modern Web Portal (Flask + Tailwind CSS)
├── banking_system.py       # ⚡ Console / Terminal CLI Application
├── test_banking_system.py  # 🧪 Unit test suite covering all banking operations
├── run_gui.bat             # 🚀 1-Click Desktop App Launcher (Windows)
├── run_web.bat             # 🚀 1-Click Web App Launcher (Windows)
├── .gitignore              # 🙈 Git ignore configuration
└── README.md               # 📖 Project documentation and instructions
```

---

## 💻 How to Run

### 1. Launch Desktop GUI (Recommended)
Double-click `run_gui.bat` or run:
```bash
python gui_app.py
```

### 2. Launch Web Dashboard
Double-click `run_web.bat` or run:
```bash
python web_app.py
```
Then open your browser at: `http://127.0.0.1:5000`

### 3. Launch Console / CLI App
```bash
python banking_system.py
```

### 4. Run Automated Unit Tests
```bash
python -m unittest test_banking_system.py
```

---

## 📋 Step-by-Step GitHub Submission Instructions

To submit this project for the **EWB Python with AI Internship**:

1. **Push Changes to GitHub:**
   ```bash
   git add .
   git commit -m "feat: add Desktop GUI and Web Dashboard interfaces"
   git push origin main
   ```

2. **Submit Google Form:**
   * URL: `https://github.com/Zainul9142/Banking-System-Mini-Project`
   * Submit through the Google Form provided by the management before **25th September**.
