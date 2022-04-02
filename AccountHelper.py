import csv
import logging
import sys
import sqlite3



class AccountHelper:

    def __init__(self):
        """Creates connection to the database, checks if accounts table exists and creates in case it doesn't"""
        try:
            self.conn = sqlite3.connect('db/budget.db')
            self.c = self.conn.cursor()
        except sqlite3.Error as e:
            logging.error("Error connecting to database!")
            raise

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='accounts'")
        if (self.c.fetchone() == None):
            self.c.execute("""CREATE TABLE accounts (acc_id integer primary key, acc_number text, acc_name text, acc_balance float)""")
        self.conn.commit()

    def get_account(self, acc_number):
        self.c.execute("SELECT accounts.acc_id FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        return self.c.fetchone()

    def get_name(self, acc_id):
        self.c.execute("SELECT accounts.acc_name FROM accounts WHERE acc_id=:acc_id", {'acc_id': acc_id})
        return self.c.fetchone()

    def get_id(self, acc_name):
        self.c.execute("SELECT accounts.acc_id FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        acc_id = self.c.fetchone()
        if (acc_id == None):
            return None
        else:
            return acc_id[0]

    def save_csv(self, account_file):
        header = ["Account Number", "Account Name", "Account Balance"]
        accounts = self.itemize()
        with open(account_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(accounts)

    def load_csv(self, account_file):
        with open(account_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        new_accounts = [line for line in data]
        new_accounts.pop(0)

        accounts = self.itemize()
        account_numbers = []
        if accounts:
            account_numbers = [b[0] for b in accounts]

        for na in new_accounts:
            if na[0].startswith("#"):
                continue
            if len(na) != 3:
                logging.error('Error! Missing argument in line "{}"'.format(na))
                sys.exit(1)
            if int(na[0]) in account_numbers: #changing an existing account
                account_numbers.remove(int(na[0]))
                self.update_account(na[0], na[1], na[2])
            else: #adding a new account
                self.create(na[0], na[1], na[2])

        if account_numbers: #there are accounts to be deleted
            for acc_number in account_numbers:
                self.delete(acc_number)
    
    def update_account(self, acc_number, new_acc_name, new_acc_balance):
        new_acc_balance = float(new_acc_balance)
        
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        _, acc_number, acc_name, acc_balance = self.c.fetchone()
        if new_acc_name != acc_name:
            self.rename(acc_name, new_acc_name)
        if acc_balance != new_acc_balance:
            self.set_balance(new_acc_name, new_acc_balance)

    def create(self, acc_number, acc_name, acc_balance):
        """Checks if account already exists (account number and name). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        if (self.c.fetchone() != None):
            logging.error('There\'s already an account with number `{}` in the Database! Aborting!'.format(acc_number))
            sys.exit(1)

        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            logging.error('There\'s already an account called `{}` in the Database! Aborting!'.format(acc_name))
            sys.exit(1)

        self.c.execute("INSERT INTO accounts VALUES (NULL, :acc_number, :acc_name, :acc_balance)", {'acc_number': acc_number, 'acc_name': acc_name, 'acc_balance': acc_balance})
        logging.info('Created account `{}` with the account number `{}` with a balance of `{}`.'.format(acc_name, acc_number, acc_balance))

        self.conn.commit()

    def rename(self, acc_name, new_acc_name):
        """Renames an existing account"""
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:new_acc_name", {'new_acc_name': new_acc_name})
        if (self.c.fetchone()):
            logging.error('There\'s already an account called `{}` in the Database! Aborting!'.format(new_acc_name))
            sys.exit(1)
        self.c.execute("SELECT * FROM accounts WHERE acc_name=:acc_name", {'acc_name': acc_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE accounts SET acc_name=:new_acc_name WHERE acc_name=:acc_name", {'acc_name': acc_name, 'new_acc_name': new_acc_name})
            logging.info('Renamed account `{}` to `{}`.'.format(acc_name, new_acc_name))
        else:
            logging.error('Account `{}` is not in the Database! Aborting!'.format(acc_name))
            sys.exit(1)
        self.conn.commit()

    def itemize(self):
        """Lists all accounts"""
        self.c.execute("SELECT * FROM accounts")
        accounts = self.c.fetchall()
        field_names = [i[0] for i in self.c.description]
        if not accounts:
            logging.info('There are currently no accounts!')
            return False
        else:
            #print('Listing all accounts:')
            #print(field_names)
            #for acc in accounts:
            #    print('Account `{}` with number `{}` has a balance of `{}`'.format(acc[2], acc[1], acc[3]))
            return [[acc[1], acc[2], acc[3]] for acc in accounts]

    def delete(self, acc_number):
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
            logging.info('Deleted account `{}`.'.format(acc_number))
        else:
            logging.error('Account `{}` is not in the Database! Aborting!'.format(acc_number))
            sys.exit(1)
        self.conn.commit()

    def set_balance(self, acc_number, new_acc_balance):
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE accounts SET acc_balance=:new_acc_balance WHERE acc_number=:acc_number", {'new_acc_balance': new_acc_balance, 'acc_number': acc_number})
            self.conn.commit()
            return True
        else:
            return False
        
    def increase_balance_by(self, acc_number, value):
        self.c.execute("SELECT * FROM accounts WHERE acc_number=:acc_number", {'acc_number': acc_number})
        account = self.c.fetchone()
        if (account != None):
            new_acc_balance = int(account[4]) + value
            self.c.execute("UPDATE accounts SET acc_balance=:new_acc_balance WHERE acc_number=:acc_number", {'new_acc_balance': new_acc_balance, 'acc_number': acc_number})
        self.conn.commit()
