
import sys
import json
import sqlite3
import Account



class AccountHelper:

    def __init__(self):
        """Creates connection to the database, checks if accounts table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
        if (self.c.fetchone() == None):
            self.c.execute("""CREATE TABLE accounts (acc_id integer primary key, acc_number text, acc_name text, acc_balance float, acc_associated_budgets text)""")
        self.conn.commit()

    def get_id(self, acc_name):
        self.c.execute("SELECT accounts.acc_id FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        acc_id = self.c.fetchone()
        if (acc_id == None):
            return None
        else:
            return acc_id[0]

    def create(self, acc_number, acc_name, acc_balance):
        """Checks if account already exists (account number and name). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        if (self.c.fetchone() != None):
            print('There\'s already an account with number `{}` in the Database! Aborting!'.format(acc_number))
            sys.exit(1)

        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            print('There\'s already an account called `{}` in the Database! Aborting!'.format(acc_name))
            sys.exit(1)

        self.c.execute("INSERT INTO accounts VALUES (NULL, :acc_number, :acc_name, :acc_balance, :acc_associated_budgets)", {'acc_number': acc_number, 'acc_name': acc_name, 'acc_balance': acc_balance, 'acc_associated_budgets': '[]'})
        print('Created account `{}` with the account number `{}` with a balance of `{}`.'.format(acc_name, acc_number, acc_balance))

        self.conn.commit()

    def rename(self, acc_name, new_acc_name):
        """Renames an existing account"""
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:new_acc_name", {'new_acc_name': new_acc_name})
        if (self.c.fetchone()):
            print('There\'s already an account called `{}` in the Database! Aborting!'.format(new_acc_name))
            sys.exit(1)
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE accounts SET acc_name=:new_acc_name WHERE acc_name=:acc_name", {'acc_name': acc_name, 'new_acc_name': new_acc_name})
            print('Renamed account `{}` to `{}`.'.format(acc_name, new_acc_name))
        else:
            print('Account `{}` is not in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        self.conn.commit()

    def itemize(self):
        """Lists all accounts"""
        self.c.execute("SELECT * FROM accounts")
        accounts = self.c.fetchall()
        if not accounts:
            print('There are currently no accounts!')
        else:
            print('Listing all accounts:')
            for acc in accounts:
                if json.loads(acc[4]):
                    print('Account `{}` with number `{}` has a balance of `{}` and it\'s associated to the budget(s) `{}`'.format(acc[2], acc[1], acc[3], ', '.join(json.loads(acc[4]))))
                else:
                    print('Account `{}` with number `{}` has a balance of `{}` and it hasn\'t been associated to any budgets'.format(acc[2], acc[1], acc[3]))

    def delete(self, acc_name):
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
            print('Deleted account `{}`.'.format(acc_name))
        else:
            print('Account `{}` is not in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        self.conn.commit()

    def set_balance(self, acc_name, new_acc_balance):
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE accounts SET acc_balance=:new_acc_balance WHERE acc_name=:acc_name", {'new_acc_balance': new_acc_balance, 'acc_name': acc_name})
            self.conn.commit()
            return True
        else:
            return False
        
    def increase_balance_by(self, acc_name, value):
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        account = self.c.fetchone()
        if (account != None):
            new_acc_balance = int(account[4]) + value
            self.c.execute("UPDATE accounts SET acc_balance=:new_acc_balance WHERE acc_name=:acc_name", {'new_acc_balance': new_acc_balance, 'acc_name': acc_name})
        self.conn.commit()

    def associate_budget(self, acc_name, budget_name):
        #self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        #if (self.c.fetchone() == None):
        #    print('There\'s no budget with name `{}` in the Database! Aborting!'.format(budget_name))
        #    sys.exit(1)

        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        account = self.c.fetchone()
        if (account == None):
            print('There\'s no account with name `{}` in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        else:
            current_budgets = json.loads(account[4])
            if budget_name in current_budgets:
                print('Budget {} is already associated to account {}! Aborting!'.format(budget_name, acc_name))
                sys.exit(1)
            current_budgets.append(budget_name)
            current_budgets_string = json.dumps(current_budgets)
            self.c.execute("UPDATE accounts SET acc_associated_budgets=:new_associated_budgets WHERE acc_name=:acc_name", {'new_associated_budgets': current_budgets_string, 'acc_name': acc_name})
            self.conn.commit()