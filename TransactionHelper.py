import sqlite3
from datetime import datetime

class TransactionHelper:
    FORMAT = "%m/%d/%Y"

    def __init__(self):
        """Creates connection to the database, checks if transaction table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database!")

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        if (self.c.fetchone() == None):
            self.c.execute("""CREATE TABLE transactions (exp_id integer primary key, date timestamp, desc1 text, desc2 text, amount float, budget text)""")
        self.conn.commit()

    #def get_id(self, desc1):
    #    self.c.execute("SELECT transactions.exp_id FROM transactions WHERE desc1=:desc1", {'desc1': desc1})
    #    exp_id = self.c.fetchone()
    #    if (exp_id == None):
    #        return None
    #    else:
    #        return exp_id[0]

    def create(self, date, desc1, desc2, amount, budget):
        """Creates a new transaction with its date, desc1, desc2 and amount."""
        self.c.execute("INSERT INTO transactions VALUES (NULL, :date, :desc1, :desc2, :amount, :budget)", {'date': datetime.strptime(date, self.FORMAT), 'desc1': desc1, 'desc2': desc2, 'amount': amount, 'budget':budget})
        self.conn.commit()

    def itemize(self, begin='', end='', desc1='', desc2='', anydesc='', budget=''):
        """Lists all transactions"""
        budget_query = desc_query = ""
        if budget:
            budget_query = "budget='{}'".format(budget)
        if anydesc and (desc1 or desc2):
            print('anydesc is mutually exclusive with desc1/desc2!')
            return False

        if anydesc:
            desc_query = "(desc1='{}' or desc2='{}')".format(anydesc, anydesc)
        if desc1:
            desc_query += "desc1='{}'".format(desc1)
        if desc2:
            if desc_query:
                desc_query += " and "
            desc_query += "desc2='{}'".format(desc2)
            
        if desc_query and budget_query:
            desc_query = budget_query + " and " + desc_query
        if not desc_query and budget_query:
            desc_query = budget_query
        
        if not begin and not end:
            if desc_query:
                desc_query = "WHERE " + desc_query
            self.c.execute("SELECT * FROM transactions {}".format(desc_query))
        elif begin and not end:
            if desc_query:
                desc_query += " and "
            self.c.execute("SELECT * FROM transactions WHERE {} date BETWEEN '{}' and '{}'".format(desc_query, datetime.strptime(begin, self.FORMAT), datetime.now()))
        elif not begin and end:
            if desc_query:
                desc_query += " and "
            self.c.execute("SELECT * FROM transactions WHERE {} date BETWEEN '{}' and '{}'".format(desc_query, datetime.strptime("01/01/2020", self.FORMAT), datetime.strptime(end, self.FORMAT)))
        elif begin and end:
            if desc_query:
                desc_query += " and "
            self.c.execute("SELECT * FROM transactions WHERE {} date BETWEEN '{}' and '{}'".format(desc_query, datetime.strptime(begin, self.FORMAT), datetime.strptime(end, self.FORMAT)))
        transactions = self.c.fetchall()
        if not transactions:
            print('There are no transactions that match the requirements!')
            return False
        else:
            print('Listing all transactions:')
            for tra in transactions:
                print(tra)
            return transactions
