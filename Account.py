import os
import json
import Constants as C


class Account(object):
    accounts = {}       # Holds all the accounts created
    total_accounts = 0  # Total number of accounts created so far to create new ids for new accounts

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.total_wins = 0
        self.total_losses = 0
        self.id = 0
        Account.load_data()  # Load all accounts into the accounts dictionary
        # Assigns the values from the accounts dictionary to the instance variables
        if username in Account.accounts:
            self.password, self.id, self.total_wins, self.total_losses = Account.accounts[username]

    @classmethod
    def log_in(cls, username, password):
        """Checks if the account exists first in the accounts dictionary before creating an instance of Account"""
        cls.load_data()
        if username in Account.accounts and Account.accounts[username][0] == password:
            return True
        else:
            return False

    def reset_password(self, new_pass):
        """Resets the password of the current account"""
        self.password = new_pass
        # Update the account dictionary with the new password
        with open(C.SAVED_ACCOUNT_DOCUMENT, 'r') as file:
            data = json.load(file)
        for account in data['accounts'].values():
            if account['username'] == self.username:
                account['password'] = self.password
        with open(C.SAVED_ACCOUNT_DOCUMENT, 'w') as file:
            json.dump(data, file, indent=4)
        Account.accounts[self.username] = (self.password, self.id, self.total_wins, self.total_losses)

    @classmethod
    def load_data(cls):  # Loads all accounts
        with open(C.SAVED_ACCOUNT_DOCUMENT) as file:
            data = json.load(file)
            # add all accounts to the set from the account json file
            count = 0   # used to remember the id for each account
            for username, details in data["accounts"].items():
                Account.accounts[details["username"]] = (details["password"], count, details["wins"], details["losses"])
                count += 1
                # total number of accounts used to create new ids for new accounts
        Account.total_accounts = len(Account.accounts)

    def update_win_loss(self, win):
        if win:
            self.total_wins += 1
        else:
            self.total_losses += 1
        # Update the account dictionary with the new win and loss
        with open(C.SAVED_ACCOUNT_DOCUMENT, 'r') as file:
            data = json.load(file)
        for account in data['accounts'].values():
            if account['username'] == self.username:
                account['wins'] = self.total_wins
                account['losses'] = self.total_losses
        with open(C.SAVED_ACCOUNT_DOCUMENT, 'w') as file:
            json.dump(data, file, indent=4)
        Account.accounts[self.username] = (self.password, self.id, self.total_wins, self.total_losses)

    def delete_game(self, game_name):
        """Delete a saved game"""
        file_path = C.GAME_FOLDER + self.username + "/" + game_name
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False

    def create_account(self):  # Adds new account to files
        Account.accounts[self.username] = (self.password, Account.total_accounts, self.total_wins, self.total_losses)
        Account.total_accounts += 1
        with open(C.SAVED_ACCOUNT_DOCUMENT, "w") as file:
            json.dump({"accounts": {str(details[1]): {"username": username, "password": details[0], "wins": details[2],
                       "losses": details[3]} for username, details in Account.accounts.items()}}, file, indent=4)


if __name__ == "__main__":
    test = Account.log_in("testuser", "testpassword")
    if test:
        user = Account("testuser", "testpassword")
    Account.log_in("sydney", "mypassword")
