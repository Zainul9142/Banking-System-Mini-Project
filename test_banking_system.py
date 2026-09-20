"""
Automated unit & functional tests for Banking System Mini-Project
"""

import unittest
from unittest.mock import patch
import banking_system


class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        # Reset accounts dictionary before each test
        banking_system.accounts.clear()

    def test_account_creation_and_deposit(self):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice Smith",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.record_transaction(acc_num, "DEPOSIT", 1000.0, "Initial Deposit")
        
        self.assertEqual(banking_system.accounts[acc_num]["balance"], 1000.0)
        self.assertEqual(len(banking_system.accounts[acc_num]["transactions"]), 1)
        self.assertEqual(banking_system.accounts[acc_num]["transactions"][0]["type"], "DEPOSIT")

    @patch('builtins.input', side_effect=['John Doe', '9876543210', '1234', '1234', '500'])
    def test_create_account_interactive(self, mock_input):
        banking_system.create_account()
        self.assertEqual(len(banking_system.accounts), 1)
        acc_num = list(banking_system.accounts.keys())[0]
        self.assertEqual(banking_system.accounts[acc_num]["name"], "John Doe")
        self.assertEqual(banking_system.accounts[acc_num]["balance"], 500.0)
        self.assertEqual(banking_system.accounts[acc_num]["pin"], "1234")

    @patch('builtins.input', side_effect=['12345678', '1234'])
    def test_login_success(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        res = banking_system.login()
        self.assertEqual(res, 12345678)

    @patch('builtins.input', side_effect=['12345678', '0000'])
    def test_login_wrong_pin(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        res = banking_system.login()
        self.assertIsNone(res)

    @patch('builtins.input', side_effect=['500'])
    def test_deposit_money(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice Smith",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.deposit_money(acc_num)
        self.assertEqual(banking_system.accounts[acc_num]["balance"], 1500.0)
        self.assertEqual(len(banking_system.accounts[acc_num]["transactions"]), 1)

    @patch('builtins.input', side_effect=['300'])
    def test_withdraw_money_success(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice Smith",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.withdraw_money(acc_num)
        self.assertEqual(banking_system.accounts[acc_num]["balance"], 700.0)
        self.assertEqual(len(banking_system.accounts[acc_num]["transactions"]), 1)
        self.assertEqual(banking_system.accounts[acc_num]["transactions"][0]["type"], "WITHDRAWAL")

    @patch('builtins.input', side_effect=['1500'])
    def test_withdraw_money_insufficient_funds(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice Smith",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.withdraw_money(acc_num)
        self.assertEqual(banking_system.accounts[acc_num]["balance"], 1000.0)
        self.assertEqual(len(banking_system.accounts[acc_num]["transactions"]), 0)

    @patch('builtins.input', side_effect=['87654321', '400'])
    def test_transfer_money_success(self, mock_input):
        acc1 = 12345678
        acc2 = 87654321
        banking_system.accounts[acc1] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.accounts[acc2] = {
            "name": "Bob",
            "phone": "9123456780",
            "pin": "4321",
            "balance": 500.0,
            "transactions": []
        }

        banking_system.transfer_money(acc1)
        self.assertEqual(banking_system.accounts[acc1]["balance"], 600.0)
        self.assertEqual(banking_system.accounts[acc2]["balance"], 900.0)
        self.assertEqual(len(banking_system.accounts[acc1]["transactions"]), 1)
        self.assertEqual(len(banking_system.accounts[acc2]["transactions"]), 1)
        self.assertEqual(banking_system.accounts[acc1]["transactions"][0]["type"], "TRANSFER_SENT")
        self.assertEqual(banking_system.accounts[acc2]["transactions"][0]["type"], "TRANSFER_RECEIVED")

    @patch('builtins.input', side_effect=['12345678'])
    def test_transfer_money_to_self(self, mock_input):
        acc1 = 12345678
        banking_system.accounts[acc1] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.transfer_money(acc1)
        self.assertEqual(banking_system.accounts[acc1]["balance"], 1000.0)

    @patch('builtins.input', side_effect=['1234', '9999', '9999'])
    def test_change_pin_success(self, mock_input):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.change_pin(acc_num)
        self.assertEqual(banking_system.accounts[acc_num]["pin"], "9999")

    def test_transaction_history_display(self):
        acc_num = 12345678
        banking_system.accounts[acc_num] = {
            "name": "Alice",
            "phone": "9876543210",
            "pin": "1234",
            "balance": 1000.0,
            "transactions": []
        }
        banking_system.record_transaction(acc_num, "DEPOSIT", 1000.0, "Initial Deposit")
        banking_system.view_transaction_history(acc_num)


if __name__ == "__main__":
    unittest.main()
