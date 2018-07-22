import sys
import sqlite3
import Rule
from AccountHelper import AccountHelper



class RuleHelper:

    def __init__(self):
        """Creates connection to the database, checks if rules table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rules'")
        if (self.c.fetchone() == None):
            print('Creating rules table')
            self.c.execute("""CREATE TABLE rules (rule_id integer primary key, description1 text, description2 text, account_id integer)""")
        else:
            print('rules table already exists')
        self.conn.commit()

    def create_rule(self, description1, description2, acc_name):
        """Checks if rule already exists (both descriptions). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM rules WHERE description1=:description1 and description2=:description2", {'description1': description1, 'description2': description2})
        if (self.c.fetchone() != None):
            print('Rule already in the Database! Aborting!')
            sys.exit(1)

        acc = AccountHelper()
        acc_id = acc.get_account_id(acc_name)

        if acc_id:
            self.c.execute("INSERT INTO rules VALUES (NULL, :description1, :description2, :acc_id)", {'description1': description1, 'description2': description2, 'acc_id': acc_id})
            print('Created rule: description1 = `{}`, description2 = `{}` that maps to account `{}`.'.format(description1, description2, acc_name))
        else:
            print('Account `{}` doesn\'t exist!'.format(acc_name))
            sys.exit(1)

        self.conn.commit()

    def list_rules(self):
        """Lists all accounts"""
        self.c.execute("SELECT * FROM rules")
        print('Listing all rules:')
        for rul in self.c.fetchall():
            self.c.execute("SELECT accounts.acc_name FROM accounts WHERE acc_id=:acc_id", {'acc_id': rul[3]})
            acc = self.c.fetchone()
            print('Rule: description1 = `{}`, description2 = `{}` that maps to account `{}`'.format(rul[1], rul[2], acc[0]))





    def rename_account(self, acc_name, new_acc_name):
        """Renames an existing account (account number)"""
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE accounts SET acc_name=:new_acc_name WHERE acc_name=:acc_name", {'acc_name': acc_name, 'new_acc_name': new_acc_name})
            print('Renamed account `{}` to `{}`.'.format(acc_name, new_acc_name))
        else:
            print('Account `{}` is not in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        self.conn.commit()


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