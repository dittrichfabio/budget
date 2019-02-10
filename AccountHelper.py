import sys
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
            self.c.execute("""CREATE TABLE accounts (acc_id integer primary key, acc_number text, acc_name text, acc_balance integer)""")
        self.conn.commit()

    def get_account_id(self, acc_name):
        self.c.execute("SELECT accounts.acc_id FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        acc_id = self.c.fetchone()
        if (acc_id == None):
            return None
        else:
            return acc_id[0]

    def create_account(self, acc_number, acc_name, acc_balance):
        """Checks if account already exists (account number). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        if (self.c.fetchone() != None):
            print('There\'s already an account with number `{}` in the Database! Aborting!'.format(acc_number))
            sys.exit(1)

        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            print('There\'s already an account called `{}` in the Database! Aborting!'.format(acc_name))
            sys.exit(1)

        self.c.execute("INSERT INTO accounts VALUES (NULL, :acc_number, :acc_name, :acc_balance)", {'acc_number': acc_number, 'acc_name': acc_name, 'acc_balance': acc_balance})
        print('Created account `{}` with the account number `{}` and balance `{}`.'.format(acc_name, acc_number, acc_balance))

        self.conn.commit()

    def rename_account(self, acc_name, new_acc_name):
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

    def list_accounts(self):
        """Lists all accounts"""
        self.c.execute("SELECT * FROM accounts")
        accounts = self.c.fetchall()
        if not accounts:
            print('There are currently no accounts!')
        else:
            print('Listing all accounts:')
            for acc in accounts:
                print('Account `{}` with number `{}` has a balance of `{}`'.format(acc[2], acc[1], acc[3]))

    def delete_account(self, acc_name):
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
            print('Set balance of account `{}` to `{}`.'.format(acc_name, new_acc_balance))
        else:
            print('Account `{}` is not in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        self.conn.commit()