#bank.py

import json
import os
# IMPORT THE ACCOUNT CLASS FROM THE OTHER FILE
from account import Account 

class Bank:
    """Manages all accounts, data persistence, and central bank operations."""
    
    DATA_FILE = "bank_data.json"
    
    def __init__(self):
        self.all_accounts = {}
        self.next_account_number = 1001
        self.load_data() # Load data upon startup

    # --- Data Persistence Functions ---
    def save_data(self):
        """Saves all accounts and the next account number to a JSON file."""
        data_to_save = {
            "next_account_number": self.next_account_number,
            "accounts": {acc_num: acc.to_dict() for acc_num, acc in self.all_accounts.items()}
        }
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump(data_to_save, f, indent=4)
            print(f"\n[System] Data successfully saved to {self.DATA_FILE}")
        except Exception as e:
            print(f"\n[System] Error saving data: {e}")

    def load_data(self):
        """Loads all accounts from the JSON file and recreates Account objects."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.next_account_number = data.get("next_account_number", 1001)
                    
                    # Use the Account.from_dict() class method to reconstruct objects
                    for acc_num, acc_data in data["accounts"].items():
                        self.all_accounts[acc_num] = Account.from_dict(acc_data)
                    print(f"[System] Data loaded successfully from {self.DATA_FILE} (Total Accounts: {len(self.all_accounts)})")
            except Exception as e:
                print(f"[System] Error loading data. Starting with a fresh bank: {e}")
                self.all_accounts = {}
        else:
            print(f"[System] No data file ({self.DATA_FILE}) found. Starting fresh.")
            
    # --- Account Management Functions ---
    def create_account(self, name, initial_deposit, pin, acc_type):
        """Creates a new unique account and saves the data."""
        if initial_deposit < 0:
            print("❌ Initial deposit cannot be negative.")
            return None
            
        new_acc_num = str(self.next_account_number)
        new_account = Account(new_acc_num, name, initial_deposit, pin, acc_type)
        self.all_accounts[new_acc_num] = new_account
        self.next_account_number += 1
        self.save_data()
        
        print(f"\n✅ Account created successfully! Account Number: **{new_acc_num}**")
        return new_acc_num

    def authenticate_account(self, acc_num, pin):
        """Checks account number and PIN for login."""
        if acc_num in self.all_accounts:
            account = self.all_accounts[acc_num]
            if account._pin == pin: 
                return account # Returns the Account object on success
            else:
                print("❌ Authentication failed: Incorrect PIN.")
        else:
            print("❌ Authentication failed: Account not found.")
        return None

    # --- Transfer Function ---
    def transfer_funds(self, sender_account, receiver_acc_num, amount):
        """Transfers funds from the sender (authenticated) to a receiver account."""
        if receiver_acc_num not in self.all_accounts:
            print("❌ Transfer failed: Receiver account number not found.")
            return False
            
        receiver_account = self.all_accounts[receiver_acc_num]
        
        if sender_account._account_number == receiver_acc_num:
            print("❌ Transfer failed: Cannot transfer to the same account.")
            return False

        if amount <= 0:
            print("❌ Transfer amount must be positive.")
            return False

        # 1. Attempt secure withdrawal
        withdrawal_type = f"Transfer to {receiver_acc_num}"
        if sender_account.withdraw(amount, transaction_type=withdrawal_type):
            # 2. Deposit into receiver
            receiver_account.deposit(amount)
            # 3. Record specific transaction for receiver
            receiver_account._add_transaction(f"Transfer from {sender_account._account_number}", amount, sender_account._account_number)
            
            # 4. Save new state
            self.save_data()
            print(f"\n✅ **TRANSFER SUCCESSFUL!** Transferred {amount} to {receiver_acc_num}.")
            return True
        else:
            # Withdrawal failed (handled by Account.withdraw)
            return False
            
# End of bank.py