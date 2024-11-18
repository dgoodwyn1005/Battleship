import os
import json
import random

# Current Environment
Environment = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Saved Account Document
SAVED_ACCOUNT_DOCUMENT = Environment + "\SavedAccounts"

class Account():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = -1
        self.account_open = False

        self.un_list = []
        self.pw_list = []

    def log_in(self):
        self.load_data()

        if self.username in self.un_list and self.password in self.pw_list:
            self.account_open = True
            data = []
            with open(SAVED_ACCOUNT_DOCUMENT) as file:
                data = json.load(file)
            
            self.id = {i for i in data if data[i["Username"]] == self.username &
                        data[i["Password"]] == self.password}
        else:
            print("Wrong Username & Password")
            self.account_open = False

    def sign_out(self):
        if self.account_open:
            self.account_open = False

    def reset_password(self, new_pass):
        if self.account_open:
            password = new_pass

    def load_data(self): #Loads all accounts
        data = []
        with open(SAVED_ACCOUNT_DOCUMENT) as file:
            data = json.load(file)

        self.un_list = []
        self.pw_list = []
        for i in data: #i = current account id
            self.un_list.append(i["Username"])
            self.pw_list.append(i["Password"])


    def new_account_data(self): #Adds new account to files
        self.id = random.randint(1, 99999)
        new_account = {}
        u_and_p = []
        u_and_p.append({"Username":self.username})
        u_and_p.append({"Password":self.password})

        new_account.update({self.id:u_and_p})

        with open(SAVED_ACCOUNT_DOCUMENT) as file:
            file.write(json.dumps(new_account))
