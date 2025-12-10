# account.py

from datetime import datetime

class Account:
    """Represents a single bank account with core transaction methods and history."""
    
    def __init__(self, acc_number, name, balance, pin, acc_type="Savings", transactions=None):
        self._account_number = acc_number
        self._name = name
        self._balance = balance
        self._pin = pin
        self._account_type = acc_type
        # Initialize transactions list
        self._transactions = transactions if transactions is not None else []
        if not transactions: # Only add 'Opening Balance' if it's a brand new account initialization
             self._add_transaction("Opening Balance", balance)

    def _add_transaction(self, type_desc, amount, receiver_acc=None):
        """Internal helper to record a transaction."""
        transaction = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_desc,
            "amount": amount,
            "receiver": receiver_acc, # Used for transfers
            "balance_after": self._balance
        }
        self._transactions.append(transaction)

    def get_balance(self):
        """Returns the current account balance."""
        return self._balance

    def deposit(self, amount):
        """Adds money to the account."""
        if amount > 0:
            self._balance += amount
            self._add_transaction("Deposit", amount)
            print(f"✅ Deposit successful. New balance: {self._balance}")
            return True
        print("❌ Deposit amount must be positive.")
        return False

    def withdraw(self, amount, transaction_type="Withdrawal"):
        """Subtracts money from the account, checking for funds."""
        if amount > 0 and self._balance >= amount:
            self._balance -= amount
            # Use negative amount to signify outflow in transaction history
            self._add_transaction(transaction_type, -amount) 
            print(f"✅ Withdrawal successful. New balance: {self._balance}")
            return True
        elif self._balance < amount:
            print("❌ Withdrawal failed. Insufficient funds.")
        else:
            print("❌ Withdrawal amount must be positive.")
        return False
    
    def view_transactions(self):
        """Prints the detailed transaction history."""
        print("\n--- Transaction History ---")
        if not self._transactions:
            print("No transactions recorded.")
            return

        # Formatting the output table
        print("{:<20} {:<15} {:<10} {:<20} {:<15}".format(
              "Date/Time", "Type", "Amount", "Balance After", "To/From Account"))

        for t in self._transactions:
            # Format amount: show negative for outflows
            amount_display = f"{t['amount']}" if t['amount'] >= 0 else f"({abs(t['amount'])})"
            receiver_str = t['receiver'] if t['receiver'] else "N/A"
            print("{:<20} {:<15} {:<10} {:<20} {:<15}".format(
                  t['timestamp'], t['type'], amount_display, t['balance_after'], receiver_str))

    # --- Persistence Methods (for serialization) ---
    def to_dict(self):
        """Converts Account object to a dictionary for saving (JSON)."""
        return {
            "account_number": self._account_number,
            "name": self._name,
            "balance": self._balance,
            "pin": self._pin,
            "account_type": self._account_type,
            "transactions": self._transactions
        }

    @classmethod
    def from_dict(cls, data):
        """Creates an Account object from a dictionary (JSON loading)."""
        return cls(
            data["account_number"],
            data["name"],
            data["balance"],
            data["pin"],
            data["account_type"],
            data["transactions"]
        )

# End of account.py