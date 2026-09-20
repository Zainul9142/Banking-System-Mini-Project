# 🏦 Banking System – Mini Project

A Python-based menu-driven banking application that simulates real-world banking operations. It enables users to create a bank account, securely authenticate with an Account Number and PIN, check balances, deposit/withdraw money, transfer funds between accounts, view timestamped transaction history, and manage security PINs.

---

## 📌 Project Overview
The **Banking System Mini Project** combines core Python programming concepts into a unified, practical, and functional application. It replicates essential functionalities of banking portals and ATM software through an interactive command-line interface.

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
| **String Operations** | String formatting, stripping, validation, and table alignments |
| **`random` Module** | Auto-generating non-colliding 8-digit account numbers |
| **`datetime` Module** | Recording exact timestamps for each transaction record |

---

## 📁 Project Structure

```
PythonAI/
│
├── banking_system.py       # Main application source code
├── test_banking_system.py  # Unit tests covering all banking operations
└── README.md               # Project documentation and instructions
```

---

## 💻 How to Run the Project

### Prerequisites
* Python 3.8 or higher installed on your system.

### Running the Application
```bash
python banking_system.py
```

### Running Automated Unit Tests
```bash
python -m unittest test_banking_system.py
```

---

## 📋 Step-by-Step GitHub Submission Instructions

To submit this project for the **EWB Python with AI Internship**:

1. **Initialize Git & Commit:**
   ```bash
   git init
   git add .
   git commit -m "feat: complete Banking System mini project"
   ```

2. **Create a GitHub Repository:**
   * Go to [GitHub](https://github.com) -> Click **New Repository**.
   * Name your repository (e.g., `EWB-Banking-System-Mini-Project`).
   * Keep it **Public**.

3. **Push Code to GitHub:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo-name>.git
   git push -u origin main
   ```

4. **Submit Google Form:**
   * Copy your GitHub repository URL.
   * Fill out and submit the Google Form provided by the management before **25th September**.
