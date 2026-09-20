"""
================================================================================
BANKING SYSTEM - WEB APPLICATION (FLASK)
================================================================================
A responsive, full-featured web dashboard interface for the Banking System
Mini Project built with Flask and modern Tailwind-styled HTML5/JavaScript.

Run: python web_app.py
Access via browser at: http://127.0.0.1:5000
================================================================================
"""

from flask import Flask, render_template_string, request, jsonify, session
import random
import datetime

app = Flask(__name__)
app.secret_key = "super-secret-banking-key-python-ai"

# In-memory storage for accounts
accounts = {
    10001001: {
        "name": "Zainul Abideen",
        "phone": "9876543210",
        "pin": "1234",
        "balance": 25000.0,
        "transactions": [
            {
                "timestamp": "2026-09-20 10:00:00",
                "type": "DEPOSIT",
                "amount": 25000.0,
                "details": "Opening Demo Balance",
                "balance_after": 25000.0
            }
        ]
    },
    10002002: {
        "name": "Rahul Sharma",
        "phone": "9123456780",
        "pin": "4321",
        "balance": 15000.0,
        "transactions": [
            {
                "timestamp": "2026-09-20 10:30:00",
                "type": "DEPOSIT",
                "amount": 15000.0,
                "details": "Opening Demo Balance",
                "balance_after": 15000.0
            }
        ]
    }
}


def generate_account_number():
    while True:
        acc = random.randint(10000000, 99999999)
        if acc not in accounts:
            return acc


def record_transaction(acc_num, trans_type, amount, details=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur_bal = accounts[acc_num]["balance"]
    accounts[acc_num]["transactions"].append({
        "timestamp": now,
        "type": trans_type,
        "amount": amount,
        "details": details,
        "balance_after": cur_bal
    })


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Banking System Dashboard</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen">
  <div id="app" class="max-w-6xl mx-auto p-4 md:p-8">
    
    <!-- Navbar -->
    <header class="flex flex-wrap items-center justify-between gap-4 pb-6 mb-8 border-b border-slate-800">
      <div class="flex items-center gap-3">
        <div class="w-12 h-12 rounded-xl bg-blue-600 flex items-center justify-center text-2xl shadow-lg shadow-blue-500/20">
          🏦
        </div>
        <div>
          <h1 class="text-xl font-bold text-white tracking-tight">NextGen Banking System</h1>
          <p class="text-xs text-slate-400">EWB Python With AI • Mini Project</p>
        </div>
      </div>
      <div id="authStatus" class="flex items-center gap-3"></div>
    </header>

    <!-- Main Content Area -->
    <main id="mainView"></main>

  </div>

  <!-- Toast Notification Container -->
  <div id="toast" class="fixed bottom-5 right-5 z-50 transform transition-all duration-300 translate-y-20 opacity-0 pointer-events-none px-5 py-3 rounded-xl shadow-2xl text-sm font-semibold flex items-center gap-2"></div>

  <script>
    let currentUser = null;

    function showToast(msg, type = 'success') {
      const t = document.getElementById('toast');
      t.innerText = (type === 'success' ? '✔ ' : '✖ ') + msg;
      t.className = `fixed bottom-5 right-5 z-50 transform transition-all duration-300 translate-y-0 opacity-100 px-5 py-3 rounded-xl shadow-2xl text-sm font-semibold flex items-center gap-2 ${type === 'success' ? 'bg-emerald-600 text-white shadow-emerald-500/30' : 'bg-rose-600 text-white shadow-rose-500/30'}`;
      setTimeout(() => {
        t.className = 'fixed bottom-5 right-5 z-50 transform transition-all duration-300 translate-y-20 opacity-0 pointer-events-none px-5 py-3 rounded-xl shadow-2xl text-sm font-semibold flex items-center gap-2';
      }, 3500);
    }

    async function checkAuth() {
      const res = await fetch('/api/user');
      const data = await res.json();
      currentUser = data.user;
      renderApp();
    }

    function renderApp() {
      const authStatus = document.getElementById('authStatus');
      const mainView = document.getElementById('mainView');

      if (!currentUser) {
        authStatus.innerHTML = `
          <span class="text-xs text-amber-400 bg-amber-950/60 border border-amber-800/60 px-3 py-1.5 rounded-full font-medium">Session: Guest</span>
        `;
        renderAuthScreen(mainView);
      } else {
        authStatus.innerHTML = `
          <div class="text-right hidden sm:block">
            <p class="text-xs text-slate-400 font-medium">Logged in as</p>
            <p class="text-sm font-bold text-white">${currentUser.name} (${currentUser.account_number})</p>
          </div>
          <button onclick="handleLogout()" class="px-4 py-2 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border border-rose-500/30 rounded-lg text-xs font-bold transition">🚪 Logout</button>
        `;
        renderDashboard(mainView);
      }
    }

    function renderAuthScreen(container) {
      container.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-4xl mx-auto items-start">
          
          <!-- Login Box -->
          <div class="bg-slate-900/90 border border-slate-800 p-6 md:p-8 rounded-2xl shadow-xl backdrop-blur">
            <div class="mb-6">
              <span class="text-xs font-semibold uppercase tracking-wider text-blue-400">Existing Customer</span>
              <h2 class="text-xl font-bold text-white mt-1">Account Login</h2>
              <p class="text-xs text-slate-400 mt-1">Enter your 8-digit Account Number & 4-digit PIN</p>
            </div>
            
            <form onsubmit="handleLogin(event)" class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-slate-300 mb-1.5">Account Number</label>
                <input type="text" id="loginAcc" value="10001001" required placeholder="e.g. 10001001" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-300 mb-1.5">4-digit PIN</label>
                <input type="password" id="loginPin" value="1234" maxlength="4" required placeholder="••••" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500">
              </div>
              <button type="submit" class="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-blue-500/25 transition">🔐 Sign In</button>
              <p class="text-center text-xs text-slate-500 pt-2">Demo Account: <span class="text-slate-300 font-mono">10001001</span> | PIN: <span class="text-slate-300 font-mono">1234</span></p>
            </form>
          </div>

          <!-- Register Box -->
          <div class="bg-slate-900/90 border border-slate-800 p-6 md:p-8 rounded-2xl shadow-xl backdrop-blur">
            <div class="mb-6">
              <span class="text-xs font-semibold uppercase tracking-wider text-emerald-400">New Customer</span>
              <h2 class="text-xl font-bold text-white mt-1">Open Bank Account</h2>
              <p class="text-xs text-slate-400 mt-1">Generate your unique 8-digit account instantly</p>
            </div>
            
            <form onsubmit="handleRegister(event)" class="space-y-4">
              <div>
                <label class="block text-xs font-medium text-slate-300 mb-1.5">Full Name</label>
                <input type="text" id="regName" required placeholder="e.g. Rahul Sharma" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500">
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-300 mb-1.5">10-Digit Phone Number</label>
                <input type="tel" id="regPhone" maxlength="10" required placeholder="e.g. 9876543210" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500">
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-medium text-slate-300 mb-1.5">4-digit PIN</label>
                  <input type="password" id="regPin" maxlength="4" required placeholder="••••" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
                <div>
                  <label class="block text-xs font-medium text-slate-300 mb-1.5">Confirm PIN</label>
                  <input type="password" id="regConfPin" maxlength="4" required placeholder="••••" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500">
                </div>
              </div>
              <div>
                <label class="block text-xs font-medium text-slate-300 mb-1.5">Initial Deposit (₹)</label>
                <input type="number" id="regDeposit" min="0" value="1000" placeholder="0.00" class="w-full bg-slate-950 border border-slate-800 rounded-xl px-4 py-2 text-sm text-white focus:outline-none focus:border-emerald-500">
              </div>
              <button type="submit" class="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-sm font-bold shadow-lg shadow-emerald-500/25 transition">➕ Create Account</button>
            </form>
          </div>

        </div>
      `;
    }

    function renderDashboard(container) {
      container.innerHTML = `
        <div class="space-y-6">
          
          <!-- Top Stats Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            
            <div class="bg-gradient-to-br from-slate-900 to-slate-900/70 border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-lg">
              <div class="absolute -right-4 -bottom-4 text-7xl opacity-5">💰</div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Available Balance</p>
              <h3 class="text-3xl font-extrabold text-emerald-400 mt-2">₹${currentUser.balance.toLocaleString('en-IN', {minimumFractionDigits: 2})}</h3>
              <p class="text-xs text-slate-500 mt-1">Real-time updated balance</p>
            </div>

            <div class="bg-gradient-to-br from-slate-900 to-slate-900/70 border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-lg">
              <div class="absolute -right-4 -bottom-4 text-7xl opacity-5">💳</div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Account Details</p>
              <h3 class="text-2xl font-bold text-white mt-2 font-mono">${currentUser.account_number}</h3>
              <p class="text-xs text-slate-400 mt-1">Holder: <span class="text-slate-200">${currentUser.name}</span></p>
            </div>

            <div class="bg-gradient-to-br from-slate-900 to-slate-900/70 border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-lg">
              <div class="absolute -right-4 -bottom-4 text-7xl opacity-5">📱</div>
              <p class="text-xs font-semibold uppercase tracking-wider text-slate-400">Registered Phone</p>
              <h3 class="text-2xl font-bold text-white mt-2 font-mono">+91 ${currentUser.phone}</h3>
              <p class="text-xs text-emerald-400 mt-1">✔ Verified Account</p>
            </div>

          </div>

          <!-- Quick Action Buttons -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <button onclick="promptDeposit()" class="p-4 bg-emerald-950/40 hover:bg-emerald-900/50 border border-emerald-800/60 rounded-xl text-left transition group">
              <span class="text-2xl block mb-1">➕</span>
              <p class="font-bold text-sm text-emerald-300">Deposit</p>
              <p class="text-[11px] text-slate-400">Add funds instantly</p>
            </button>

            <button onclick="promptWithdraw()" class="p-4 bg-amber-950/40 hover:bg-amber-900/50 border border-amber-800/60 rounded-xl text-left transition group">
              <span class="text-2xl block mb-1">➖</span>
              <p class="font-bold text-sm text-amber-300">Withdraw</p>
              <p class="text-[11px] text-slate-400">Deduct balance</p>
            </button>

            <button onclick="promptTransfer()" class="p-4 bg-blue-950/40 hover:bg-blue-900/50 border border-blue-800/60 rounded-xl text-left transition group">
              <span class="text-2xl block mb-1">🔁</span>
              <p class="font-bold text-sm text-blue-300">Transfer</p>
              <p class="text-[11px] text-slate-400">Send to another acc</p>
            </button>

            <button onclick="promptChangePin()" class="p-4 bg-purple-950/40 hover:bg-purple-900/50 border border-purple-800/60 rounded-xl text-left transition group">
              <span class="text-2xl block mb-1">🔑</span>
              <p class="font-bold text-sm text-purple-300">Change PIN</p>
              <p class="text-[11px] text-slate-400">Update security code</p>
            </button>
          </div>

          <!-- Transaction Ledger Table -->
          <div class="bg-slate-900/90 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
            <div class="p-5 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h3 class="font-bold text-base text-white">📜 Transaction History Ledger</h3>
                <p class="text-xs text-slate-400">Live timestamped record of all banking activities</p>
              </div>
              <button onclick="checkAuth()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-xs font-semibold rounded-lg text-slate-300 transition">🔄 Refresh</button>
            </div>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs">
                <thead class="bg-slate-950/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                  <tr>
                    <th class="py-3 px-4">Date & Time</th>
                    <th class="py-3 px-4">Type</th>
                    <th class="py-3 px-4 text-right">Amount</th>
                    <th class="py-3 px-4 text-right">Balance After</th>
                    <th class="py-3 px-4">Details</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-800/60 font-mono">
                  ${currentUser.transactions.length === 0 ? `
                    <tr><td colspan="5" class="py-8 text-center text-slate-500 font-sans">No transactions recorded yet.</td></tr>
                  ` : currentUser.transactions.slice().reverse().map(tx => `
                    <tr class="hover:bg-slate-800/40 transition">
                      <td class="py-3 px-4 text-slate-300">${tx.timestamp}</td>
                      <td class="py-3 px-4">
                        <span class="px-2 py-0.5 rounded-full text-[10px] font-bold ${
                          tx.type.includes('DEPOSIT') || tx.type.includes('RECEIVED') ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        }">${tx.type}</span>
                      </td>
                      <td class="py-3 px-4 text-right font-bold ${tx.type.includes('DEPOSIT') || tx.type.includes('RECEIVED') ? 'text-emerald-400' : 'text-rose-400'}">
                        ${tx.type.includes('DEPOSIT') || tx.type.includes('RECEIVED') ? '+' : '-'}₹${tx.amount.toLocaleString('en-IN', {minimumFractionDigits: 2})}
                      </td>
                      <td class="py-3 px-4 text-right text-slate-200">₹${tx.balance_after.toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
                      <td class="py-3 px-4 font-sans text-slate-400">${tx.details}</td>
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      `;
    }

    // Handlers
    async function handleLogin(e) {
      e.preventDefault();
      const acc = document.getElementById('loginAcc').value.trim();
      const pin = document.getElementById('loginPin').value.trim();

      const res = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({account_number: acc, pin})
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Welcome back, ${data.user.name}!`);
        currentUser = data.user;
        renderApp();
      } else {
        showToast(data.message, 'error');
      }
    }

    async function handleRegister(e) {
      e.preventDefault();
      const name = document.getElementById('regName').value.trim();
      const phone = document.getElementById('regPhone').value.trim();
      const pin = document.getElementById('regPin').value.trim();
      const confPin = document.getElementById('regConfPin').value.trim();
      const dep = document.getElementById('regDeposit').value.trim();

      if (pin !== confPin) {
        showToast('PINs do not match!', 'error');
        return;
      }

      const res = await fetch('/api/register', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({name, phone, pin, initial_deposit: dep})
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Account created! Acc No: ${data.account_number}`);
        currentUser = data.user;
        renderApp();
      } else {
        showToast(data.message, 'error');
      }
    }

    async function handleLogout() {
      await fetch('/api/logout', {method: 'POST'});
      currentUser = null;
      showToast('Logged out successfully');
      renderApp();
    }

    async function promptDeposit() {
      const val = prompt("Enter amount to deposit (₹):", "1000");
      if (!val) return;
      const res = await fetch('/api/deposit', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: parseFloat(val)})
      });
      const data = await res.json();
      if (data.success) {
        showToast(`₹${parseFloat(val).toFixed(2)} deposited successfully!`);
        currentUser = data.user;
        renderApp();
      } else {
        showToast(data.message, 'error');
      }
    }

    async function promptWithdraw() {
      const val = prompt("Enter amount to withdraw (₹):", "500");
      if (!val) return;
      const res = await fetch('/api/withdraw', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({amount: parseFloat(val)})
      });
      const data = await res.json();
      if (data.success) {
        showToast(`₹${parseFloat(val).toFixed(2)} withdrawn successfully!`);
        currentUser = data.user;
        renderApp();
      } else {
        showToast(data.message, 'error');
      }
    }

    async function promptTransfer() {
      const recAcc = prompt("Enter Receiver's 8-digit Account Number (e.g. 10002002):");
      if (!recAcc) return;
      const amt = prompt(`Enter amount to transfer to ${recAcc} (₹):`, "500");
      if (!amt) return;

      const res = await fetch('/api/transfer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({receiver_account: recAcc, amount: parseFloat(amt)})
      });
      const data = await res.json();
      if (data.success) {
        showToast(`Successfully transferred ₹${parseFloat(amt).toFixed(2)}!`);
        currentUser = data.user;
        renderApp();
      } else {
        showToast(data.message, 'error');
      }
    }

    async function promptChangePin() {
      const oldPin = prompt("Enter Old 4-digit PIN:");
      if (!oldPin) return;
      const newPin = prompt("Enter New 4-digit PIN:");
      if (!newPin) return;
      const confPin = prompt("Confirm New 4-digit PIN:");
      if (!confPin) return;

      if (newPin !== confPin) {
        showToast("New PIN confirmation mismatch", "error");
        return;
      }

      const res = await fetch('/api/change_pin', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({old_pin: oldPin, new_pin: newPin})
      });
      const data = await res.json();
      if (data.success) {
        showToast("PIN changed successfully!");
      } else {
        showToast(data.message, 'error');
      }
    }

    // Initial check
    checkAuth();
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/api/user")
def get_user():
    acc_num = session.get("account_number")
    if acc_num and acc_num in accounts:
        user_data = dict(accounts[acc_num])
        user_data["account_number"] = acc_num
        user_data.pop("pin", None)
        return jsonify({"user": user_data})
    return jsonify({"user": None})


@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json or {}
    try:
        acc_num = int(data.get("account_number", 0))
    except ValueError:
        return jsonify({"success": False, "message": "Invalid account number."})

    pin = str(data.get("pin", "")).strip()

    if acc_num not in accounts:
        return jsonify({"success": False, "message": "Account number not found."})

    if accounts[acc_num]["pin"] != pin:
        return jsonify({"success": False, "message": "Incorrect 4-digit PIN."})

    session["account_number"] = acc_num
    user_data = dict(accounts[acc_num])
    user_data["account_number"] = acc_num
    user_data.pop("pin", None)
    return jsonify({"success": True, "user": user_data})


@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.json or {}
    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    pin = str(data.get("pin", "")).strip()
    dep_val = float(data.get("initial_deposit", 0.0) or 0.0)

    if not name or len(phone) != 10 or len(pin) != 4:
        return jsonify({"success": False, "message": "Please fill all fields correctly."})

    acc_num = generate_account_number()
    accounts[acc_num] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": dep_val,
        "transactions": []
    }

    if dep_val > 0:
        record_transaction(acc_num, "DEPOSIT", dep_val, "Initial Account Opening Deposit")

    session["account_number"] = acc_num
    user_data = dict(accounts[acc_num])
    user_data["account_number"] = acc_num
    user_data.pop("pin", None)
    return jsonify({"success": True, "account_number": acc_num, "user": user_data})


@app.route("/api/logout", methods=["POST"])
def api_logout():
    session.pop("account_number", None)
    return jsonify({"success": True})


@app.route("/api/deposit", methods=["POST"])
def api_deposit():
    acc_num = session.get("account_number")
    if not acc_num or acc_num not in accounts:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    amt = float((request.json or {}).get("amount", 0))
    if amt <= 0:
        return jsonify({"success": False, "message": "Amount must be positive."})

    accounts[acc_num]["balance"] += amt
    record_transaction(acc_num, "DEPOSIT", amt, "Cash Deposit via Web Portal")

    user_data = dict(accounts[acc_num])
    user_data["account_number"] = acc_num
    user_data.pop("pin", None)
    return jsonify({"success": True, "user": user_data})


@app.route("/api/withdraw", methods=["POST"])
def api_withdraw():
    acc_num = session.get("account_number")
    if not acc_num or acc_num not in accounts:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    amt = float((request.json or {}).get("amount", 0))
    if amt <= 0:
        return jsonify({"success": False, "message": "Amount must be positive."})

    cur_bal = accounts[acc_num]["balance"]
    if amt > cur_bal:
        return jsonify({"success": False, "message": f"Insufficient funds! Available: ₹{cur_bal:,.2f}"})

    accounts[acc_num]["balance"] -= amt
    record_transaction(acc_num, "WITHDRAWAL", amt, "Cash Withdrawal via Web Portal")

    user_data = dict(accounts[acc_num])
    user_data["account_number"] = acc_num
    user_data.pop("pin", None)
    return jsonify({"success": True, "user": user_data})


@app.route("/api/transfer", methods=["POST"])
def api_transfer():
    acc_num = session.get("account_number")
    if not acc_num or acc_num not in accounts:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json or {}
    try:
        rec_acc = int(data.get("receiver_account", 0))
    except ValueError:
        return jsonify({"success": False, "message": "Invalid receiver account number."})

    amt = float(data.get("amount", 0))
    if amt <= 0:
        return jsonify({"success": False, "message": "Amount must be positive."})

    if rec_acc == acc_num:
        return jsonify({"success": False, "message": "Cannot transfer funds to your own account."})

    if rec_acc not in accounts:
        return jsonify({"success": False, "message": f"Receiver account {rec_acc} does not exist."})

    sender_bal = accounts[acc_num]["balance"]
    if amt > sender_bal:
        return jsonify({"success": False, "message": f"Insufficient funds! Available: ₹{sender_bal:,.2f}"})

    receiver_name = accounts[rec_acc]["name"]
    sender_name = accounts[acc_num]["name"]

    accounts[acc_num]["balance"] -= amt
    accounts[rec_acc]["balance"] += amt

    record_transaction(acc_num, "TRANSFER_SENT", amt, f"Transferred to {receiver_name} (Acc: {rec_acc})")
    record_transaction(rec_acc, "TRANSFER_RECEIVED", amt, f"Received from {sender_name} (Acc: {acc_num})")

    user_data = dict(accounts[acc_num])
    user_data["account_number"] = acc_num
    user_data.pop("pin", None)
    return jsonify({"success": True, "user": user_data})


@app.route("/api/change_pin", methods=["POST"])
def api_change_pin():
    acc_num = session.get("account_number")
    if not acc_num or acc_num not in accounts:
        return jsonify({"success": False, "message": "Unauthorized"}), 401

    data = request.json or {}
    old_pin = str(data.get("old_pin", "")).strip()
    new_pin = str(data.get("new_pin", "")).strip()

    if accounts[acc_num]["pin"] != old_pin:
        return jsonify({"success": False, "message": "Incorrect Old PIN."})

    if len(new_pin) != 4 or not new_pin.isdigit():
        return jsonify({"success": False, "message": "New PIN must be exactly 4 numeric digits."})

    accounts[acc_num]["pin"] = new_pin
    return jsonify({"success": True})


if __name__ == "__main__":
    print("[*] NextGen Banking Web Portal is running at: http://localhost:5000")
    print("[*] Access in your browser at: http://localhost:5000 or http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

