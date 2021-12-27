import sys
import json
import sqlite3
#import Budget
from AccountHelper import AccountHelper



class BudgetHelper:

    def __init__(self):
        """Creates connection to the database, checks if budget table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='budget'")
        if (self.c.fetchone() == None):
            self.c.execute("""CREATE TABLE budget (rule_id integer primary key, budget_name text, budget_value float, account_id integer, budget_balance float)""")
        self.conn.commit()

    def create_budget(self, budget_name, budget_value, acc_name, budget_balance):
        """Checks if budget already exists. If it doesn't, creates it."""
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            print('There\'s already a budget called `{}` in the Database! Aborting!'.format(budget_name))
            sys.exit(1)

        acc = AccountHelper()
        acc_id = acc.get_id(acc_name)

        if acc_id:
            self.c.execute("INSERT INTO budget VALUES (NULL, :budget_name, :budget_value, :acc_id, :budget_balance)", {'budget_value': budget_value, 'budget_name': budget_name, 'acc_id': acc_id, 'budget_balance': budget_balance})
            print('Created budget `{}` for {} associated to account `{}` with a balance of `{}`.'.format(budget_name, budget_value, acc_name, budget_balance))
            self.conn.commit()
            acc.associate_budget(acc_name, budget_name)
        else:
            print('Account `{}` doesn\'t exist!'.format(acc_name))
            sys.exit(1)


    def list_budgets(self):
        """Lists all budgets"""
        self.c.execute("SELECT * FROM budget")
        budgets = self.c.fetchall()
        if not budgets:
            #print('There are currently no budgets!')
            return None
        else:
            #print('Listing all budgets:')
            budget_list = []
            for bud in budgets:
                self.c.execute("SELECT accounts.acc_name FROM accounts WHERE acc_id=:acc_id", {'acc_id': bud[3]})
                acc = self.c.fetchone()
                #print('Budget `{}` of value {} maps to account `{}`'.format(bud[1], bud[2], acc[0]))
                budget_list.append([bud[1], bud[2], acc[0], bud[3]])
            return budget_list


    def rename_budget(self, budget_name, new_budget_name):
        """Renames an existing budget"""
        self.c.execute("SELECT * FROM budget WHERE budget_name=:new_budget_name", {'new_budget_name': new_budget_name})
        if (self.c.fetchone()):
            print('There\'s already a budget called `{}` in the Database! Aborting!'.format(new_budget_name))
            sys.exit(1)
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_name=:new_budget_name WHERE budget_name=:budget_name", {'budget_name': budget_name, 'new_budget_name': new_budget_name})
            print('Renamed budget `{}` to `{}`.'.format(budget_name, new_budget_name))
        else:
            print('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def delete_budget(self, budget_name):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
            print('Deleted budget `{}`.'.format(budget_name))
        else:
            print('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_value(self, budget_name, new_budget_value):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_value=:new_budget_value WHERE budget_name=:budget_name", {'new_budget_value': new_budget_value, 'budget_name': budget_name})
            print('Set budget `{}` value to `{}`.'.format(budget_name, new_budget_value))
        else:
            print('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_balance(self, budget_name, new_budget_balance):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_balance=:new_budget_balance WHERE budget_name=:budget_name", {'new_budget_balance': new_budget_balance, 'budget_name': budget_name})
            print('Set budget `{}` balance to `{}`.'.format(budget_name, new_budget_balance))
        else:
            print('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_account(self, budget_name, new_budget_acc):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            acc = AccountHelper()
            acc_id = acc.get_id(new_budget_acc)
            self.c.execute("UPDATE budget SET account_id=:acc_id WHERE budget_name=:budget_name", {'acc_id': acc_id, 'budget_name': budget_name})
            print('Set budget `{}` to account `{}`.'.format(budget_name, new_budget_acc))
        else:
            print('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()