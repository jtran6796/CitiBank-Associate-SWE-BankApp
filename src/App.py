from abc import ABC, abstractmethod

users = []


def login():
    inp = ""
    parts = inp.split()
    while(len(parts) != 2):
      print("Please enter username and password, space separated")
      inp = input()
      parts = inp.split()
    username = parts[0]
    password = parts[1]
    for user in users:
        if user._username == username and user._password == password:
            return user
    return None


def welcome():
    print("Welcome to ABC Digital Bank")


def menu(user):
    print(f"Welcome {user.get_username()}!")
    account_number = -1
    choice = -1
    while choice != 7:
        print("1) Create Account")
        print("2) View All Accounts")
        print("3) Deposit")
        print("4) Withdraw")
        print("5) Transfer")
        print("6) Close Account")
        print("7) Exit")
        choice = int(input())

        if choice == 1:
            print("1) Checking     2) Saving")
            user_input = int(input())
            new_account = Customer.create_account(user_input, user)
            new_account.print_receipt()
        elif choice == 2:
            for account in user.accounts:
                account.print_receipt()
        elif choice == 3:
            for account in user.accounts:
                account.print_receipt()
            print("Input Account Number: ", end="")
            account_number = int(input())
            print("Input the deposit amount: ", end="")
            deposit_amount = float(input())
            for account in user.accounts:
                if account.account_number == account_number:
                    account.deposit(deposit_amount)
                    account.print_receipt()
        elif choice == 4:
            for account in user.accounts:
                account.print_receipt()
            print("Input Account Number: ", end="")
            account_number = int(input())
            print("Input the withdrawal amount: ", end="")
            withdrawal_amount = float(input())
            for account in user.accounts:
                if account.account_number == account_number:
                    account.withdraw(withdrawal_amount)
                    account.print_receipt()
        elif choice == 5:
            for account in user.accounts:
                account.print_receipt()
            print("Input Source Account Number followed by Destination Account Number")
            account_numbers = input().split()
            print("Input transfer amount: ")
            transfer_amount = int(input())

            from_account = None
            to_account = None
            for account in user.accounts:
              if account == int(account_numbers[0]):
                from_account = account
              if account == int(account_numbers[1]):
                to_account = account

            if from_account and to_account:
              if from_account.withdraw(transfer_amount):
                  to_account.deposit(transfer_amount)


        elif choice == 6:
            for account in user.accounts:
                account.print_receipt()
            print("Input Account Number you wish to close: ", end="")
            account_number = int(input())
            for account in user.accounts:
                if account.account_number == account_number:
                    user.accounts.remove(account)

        elif choice == 7:
            return


def seed_database(users):
    c2 = Customer("sample", "sample123")
    users.append(c2)


class ITransaction(ABC):
    @abstractmethod
    def print_receipt(self):
        pass


class User:
    def __init__(self, username, password):
        self._username = username
        self._password = password
    
    def get_username(self):
        return self._username
    
    def set_username(self, username):
        self._username = username


class Customer(User):
    _customer_id = 0

    def __init__(self, username, password):
        super().__init__(username, password)
        self.first_name = None
        self.last_name = None
        self.accounts = []

    def set_name(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def get_name(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def create_account(account_type, account_holder):
        if account_type == 1:
            new_account = CheckingAccount(account_holder, 0)
            account_holder.accounts.append(new_account)
        elif account_type == 2:
            new_account = SavingsAccount(account_holder, 0)
            account_holder.accounts.append(new_account)
        else:
            return None
        return new_account


class Admin(User):
    def __init__(self, username, password, all_users):
        super().__init__(username, password)
        self.users = all_users


class Account(ITransaction, ABC):
    number_counter = 0

    def __init__(self, account_holder, balance):
        self.account_number = Account.number_counter
        Account.number_counter += 1
        self.account_holder = account_holder
        self.balance = balance

    def print_receipt(self):
        print(f"Receipt: {self.account_type}: {self.account_number}, balance: {self.balance}")

    def deposit(self, amount):
        self.balance += amount

    @abstractmethod
    def withdraw(self, amount):
        pass


class CheckingAccount(Account):
    account_type = "Checking Account"

    def __init__(self, account_holder, balance):
        super().__init__(account_holder, balance)
        self.overdraft_limit = None

    def withdraw(self, amount):
        self.balance -= amount


class SavingsAccount(Account):
    account_type = "Savings Account"

    def __init__(self, account_holder, balance):
        super().__init__(account_holder, balance)
        self.interest_rate = None

    def withdraw(self, amount):
        diff = self.balance - amount
        if diff <= 100:
            return
        else:
            self.balance -= amount


def main():
    seed_database(users)
    admin = Admin("admin", "admin123", users)
    users.append(admin)
    welcome()
    user = login()
    menu(user)


if __name__ == "__main__":
    main()
