# main.py
# main.py

# IMPORT THE BANK CLASS FROM THE OTHER FILE
from bank import Bank 

# Initialize the Bank system
my_bank = Bank()

def main_menu():
    print("\n\n=== Welcome to the Python Bank Management System ===")
    print("1. Create New Account")
    print("2. Login to Account")
    print("3. Exit and Save System")
    choice = input("Enter your choice (1-3): ")
    return choice

def account_menu(account):
    while True:
        print(f"\n--- Account Menu: {account._name} ({account._account_number}) ---")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Funds")
        print("5. View Transaction History")
        print("6. Logout")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == '1':
            print(f"Your current balance is: **{account.get_balance()}**")
            
        elif choice == '2':
            try:
                amount = float(input("Enter deposit amount: "))
                if account.deposit(amount):
                    my_bank.save_data()
            except ValueError:
                print("❌ Invalid input. Please enter a number.")
                
        elif choice == '3':
            try:
                amount = float(input("Enter withdrawal amount: "))
                if account.withdraw(amount):
                    my_bank.save_data()
            except ValueError:
                print("❌ Invalid input. Please enter a number.")

        elif choice == '4':
            try:
                receiver_acc_num = input("Enter receiver's Account Number: ")
                amount = float(input("Enter transfer amount: "))
                my_bank.transfer_funds(account, receiver_acc_num, amount)
            except ValueError:
                print("❌ Invalid input. Please enter a number for the amount.")
                
        elif choice == '5':
            account.view_transactions()

        elif choice == '6':
            print("Logging out...")
            break
        
        else:
            print("❌ Invalid choice. Please try again.")


# --- Main Execution Loop ---
if __name__ == "__main__":
    while True:
        main_choice = main_menu()
        
        if main_choice == '1':
            print("\n--- New Account Creation ---")
            name = input("Enter your full name: ")
            try:
                deposit = float(input("Enter initial deposit amount (min 0): "))
                pin = input("Set a 4-digit PIN: ")
                acc_type = input("Account type (Savings/Current) [Default: Savings]: ") or "Savings"
                
                if len(pin) == 4 and pin.isdigit():
                    my_bank.create_account(name, deposit, pin, acc_type)
                else:
                    print("❌ Invalid PIN format. Must be a 4-digit number.")
            except ValueError:
                print("❌ Invalid deposit amount.")
                
        elif main_choice == '2':
            print("\n--- Account Login ---")
            acc_num = input("Enter Account Number: ")
            pin = input("Enter PIN: ")
            
            logged_in_account = my_bank.authenticate_account(acc_num, pin)
            
            if logged_in_account:
                account_menu(logged_in_account)
                
        elif main_choice == '3':
            my_bank.save_data() # Final save before exiting
            print("\nThank you for using the Python Bank Management System. Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

# End of main.py