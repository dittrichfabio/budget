import csv
import logging
import sys
import sqlite3
from AccountHelper import AccountHelper



class BudgetHelper:

    def __init__(self):
        """Creates connection to the database, checks if budget table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            logging.error("Error connecting to database!")
            raise

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='budget'")
        if (self.c.fetchone() == None):
            self.c.execute("""CREATE TABLE budget (rule_id integer primary key, budget_name text, budget_value float, account_id integer, budget_balance float)""")
        self.conn.commit()

    def save_csv(self, budget_file):
        header = ["Budget Name", "Budget Value", "Associated Account Name", "Budget Balance"]
        budgets = self.itemize()
        #budgets = [[bud[1], bud[2], bud[3], bud[4]] for bud in budgets]
        with open(budget_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(budgets)

    def load_csv(self, budget_file):
        with open(budget_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        new_budgets = [line for line in data]
        new_budgets.pop(0)

        self.c.execute("SELECT * FROM budget")
        budgets = self.c.fetchall()
        budget_names = []
        if budgets:
            budget_names = [b[1] for b in budgets]

        for nb in new_budgets:
            if nb[0].startswith("#"):
                continue
            if len(nb) != 4:
                logging.error('Error! Missing argument in line "{}"'.format(nb))
                sys.exit(1)
            if nb[0] in budget_names: #changing an existing budget
                budget_names.remove(nb[0])
                self.update_budget(*nb)
            else: #adding a new budget
                self.create(*nb)

        if budget_names: #there are budgets to be deleted
            for budget_name in budget_names:
                self.delete(budget_name)
    

    def update_budget(self, budget_name, new_budget_value, new_acc_name, new_budget_balance):
        acc = AccountHelper()
        new_acc_id = acc.get_id(new_acc_name)

        new_budget_value = float(new_budget_value)
        new_budget_balance = float(new_budget_balance)
        
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        i, _, budget_value, acc_id, budget_balance = self.c.fetchone()

        if new_budget_value != budget_value:
            self.change_budget_value(budget_name, new_budget_value)
        if new_budget_balance != budget_balance:
            self.change_budget_balance(budget_name, new_budget_balance)
        if new_acc_id != acc_id:
            self.change_budget_account(budget_name, new_acc_name)


    def create(self, budget_name, budget_value, acc_name, budget_balance):
        """Checks if budget already exists. If it doesn't, creates it."""
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            logging.error('There\'s already a budget called `{}` in the Database! Aborting!'.format(budget_name))
            sys.exit(1)

        acc = AccountHelper()
        acc_id = acc.get_id(acc_name)

        if acc_id:
            self.c.execute("INSERT INTO budget VALUES (NULL, :budget_name, :budget_value, :acc_id, :budget_balance)", {'budget_value': budget_value, 'budget_name': budget_name, 'acc_id': acc_id, 'budget_balance': budget_balance})
            #logging.info('Created budget `{}` for {} associated to account `{}` with a balance of `{}`.'.format(budget_name, budget_value, acc_name, budget_balance))
            self.conn.commit()
        else:
            logging.error('Account `{}` doesn\'t exist!'.format(acc_name))
            sys.exit(1)


    def itemize(self):
        """Lists all budgets"""
        self.c.execute("SELECT * FROM budget")
        budgets = self.c.fetchall()
        if not budgets:
            #logging.info('There are currently no budgets!')
            return None
        else:
            #print('Listing all budgets:')
            budget_list = []
            for bud in budgets:
                self.c.execute("SELECT accounts.acc_name FROM accounts WHERE acc_id=:acc_id", {'acc_id': bud[3]})
                acc = self.c.fetchone()
                #print('Budget `{}` of value {} has balance of {} and maps to account `{}`'.format(bud[1], bud[2], bud[4], acc[0]))
                budget_list.append([bud[1], bud[2], acc[0], bud[4]])
            return budget_list


    def rename(self, budget_name, new_budget_name):
        """Renames an existing budget"""
        self.c.execute("SELECT * FROM budget WHERE budget_name=:new_budget_name", {'new_budget_name': new_budget_name})
        if (self.c.fetchone()):
            logging.error('There\'s already a budget called `{}` in the Database! Aborting!'.format(new_budget_name))
            sys.exit(1)
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_name=:new_budget_name WHERE budget_name=:budget_name", {'budget_name': budget_name, 'new_budget_name': new_budget_name})
            #logging.info('Renamed budget `{}` to `{}`.'.format(budget_name, new_budget_name))
        else:
            logging.error('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def delete(self, budget_name):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
            #logging.info('Deleted budget `{}`.'.format(budget_name))
        else:
            logging.error('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_value(self, budget_name, new_budget_value):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_value=:new_budget_value WHERE budget_name=:budget_name", {'new_budget_value': new_budget_value, 'budget_name': budget_name})
            #logging.info('Set budget `{}` value to `{}`.'.format(budget_name, new_budget_value))
        else:
            logging.error('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_balance(self, budget_name, new_budget_balance):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE budget SET budget_balance=:new_budget_balance WHERE budget_name=:budget_name", {'new_budget_balance': new_budget_balance, 'budget_name': budget_name})
           #logging.info('Set budget `{}` balance to `{}`.'.format(budget_name, new_budget_balance))
        else:
            logging.error('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()

    def change_budget_account(self, budget_name, new_budget_acc):
        self.c.execute("SELECT * FROM budget WHERE budget_name=:budget_name", {'budget_name': budget_name})
        if (self.c.fetchone() != None):
            acc = AccountHelper()
            acc_id = acc.get_id(new_budget_acc)
            self.c.execute("UPDATE budget SET account_id=:acc_id WHERE budget_name=:budget_name", {'acc_id': acc_id, 'budget_name': budget_name})
            #logging.info('Set budget `{}` to account `{}`.'.format(budget_name, new_budget_acc))
        else:
            logging.error('Budget `{}` is not in the Database! Aborting!'.format(budget_name))
            sys.exit(1)
        self.conn.commit()