import os
import json
# Current Environment
Environment = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Saved Account Document
SAVED_ACCOUNT_DOCUMENT = Environment + "/saved_accounts.json"

class Account(object):
    accounts = {}       # Holds all the accounts created
    total_accounts = 0  # Total number of accounts created so far to create new ids for new accounts
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.account_open = False
        self.total_wins = 0
        self.total_losses = 0
        self.id = 0

    @classmethod
    def log_in(cls, username, password):
        """Checks if the account exists first in the accounts dictionary before creating an instance of Account"""
        cls.load_data()
        if username in Account.accounts and Account.accounts[username][0] == password:
            print("Logged in")      # Used for testing purposes
            return True
        else:
            print("Wrong Username & Password")  # Used for testing purposes
            # self.account_open = False
            return False

    def sign_out(self):
        if self.account_open:
            self.account_open = False

    def reset_password(self, new_pass):
        """Resets the password of the current account"""
        if self.account_open:
            self.password = new_pass

    @classmethod
    def load_data(cls): #Loads all accounts
        with open(SAVED_ACCOUNT_DOCUMENT) as file:
            data = json.load(file)
            # add all accounts to the set from the account json file
            count = 0   # used to remember the id for each account
            for username, details in data["accounts"].items():
                Account.accounts[details["username"]] = (details["password"], count, details["wins"], details["losses"])
                count += 1
                # total number of accounts used to create new ids for new accounts
        Account.total_accounts = len(Account.accounts)



    def create_account(self): #Adds new account to files
        Account.accounts[self.username] = (self.password, Account.total_accounts, self.total_wins, self.total_losses)
        Account.total_accounts += 1
        with open(SAVED_ACCOUNT_DOCUMENT, "w") as file:
            json.dump({"accounts": {str(details[1]): {"username": username, "password": details[0], "wins": details[2],
                       "losses": details[3]} for username, details in Account.accounts.items()}}, file, indent=4)



if __name__ == "__main__":
    test = Account.log_in("testuser", "testpassword")
    if test:
        user = Account("testuser", "testpassword")
        print(user.username)
    Account.log_in("sydney", "mypassword")
