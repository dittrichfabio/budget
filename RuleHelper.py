import csv
import sys
import sqlite3
from BudgetHelper import BudgetHelper



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
            self.c.execute("""CREATE TABLE rules (rule_id integer primary key, rule_name text, rule_description1 text, rule_description2 text, rule_budget text)""")
        self.conn.commit()

    def save_csv(self, rule_file):
        header = ["Rule Name", "Description 1", "Description 2", "Budget Name"]
        rules = self.itemize()
        with open(rule_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            writer.writerows(rules)

    def load_csv(self, rule_file):
        with open(rule_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        new_rules = [line for line in data]
        new_rules.pop(0)

        rules = self.itemize()
        if rules:
            rules_names = [b[0] for b in rules]

        self.itemize()
        print('\n')
        for nr in new_rules:
            if nr[0] in rules_names: #changing an existing rules
                rules_names.remove(nr[0])
                self.update_rule(*nr)
            else: #adding a new rule
                self.create(*nr)
            self.itemize()
            print('\n')

        if rules_names: #there are accounts to be deleted
            for rule_name in rules_names:
                self.delete(rule_name)
        self.itemize()
    
    def update_rule(self, rule_name, new_desc1, new_desc2, new_budget):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        _, _, desc1, desc2, budget = self.c.fetchone()
        if new_desc1 != desc1:
            self.change_desc1(rule_name, new_desc1)
        if new_desc2 != desc2:
            self.change_desc2(rule_name, new_desc2)
        if new_budget != budget:
            self.change_budget(rule_name, new_budget)

    def create(self, rule_name, rule_description1, rule_description2, rule_budget):
        """Checks if rule already exists (both descriptions). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if (self.c.fetchone() != None):
            print('There\'s already a rule called `{}` in the Database! Aborting!'.format(rule_name))
            sys.exit(1)

        bud = BudgetHelper()
        budgets = bud.itemize()
        budgets = [i[0] for i in budgets]

        if rule_budget in budgets:
            self.c.execute("INSERT INTO rules VALUES (NULL, :rule_name, :rule_description1, :rule_description2, :rule_budget)", {'rule_name': rule_name, 'rule_description1': rule_description1, 'rule_description2': rule_description2, 'rule_budget': rule_budget})
            print('Created rule {}: description1 = `{}`, description2 = `{}` that maps to budget `{}`.'.format(rule_name, rule_description1, rule_description2, rule_budget))
        else:
            print('Budget `{}` doesn\'t exist!'.format(rule_budget))
            sys.exit(1)

        self.conn.commit()

    def change_desc1(self, rule_name, new_desc1):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if self.c.fetchone() == None:
            print('There\'s no rule called `{}` in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        
        self.c.execute("UPDATE rules SET rule_description1=:new_desc1 WHERE rule_name=:rule_name", {'rule_name': rule_name, 'new_desc1': new_desc1})
        self.conn.commit()

    def change_desc2(self, rule_name, new_desc2):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if self.c.fetchone() == None:
            print('There\'s no rule called `{}` in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        
        self.c.execute("UPDATE rules SET rule_description2=:new_desc2 WHERE rule_name=:rule_name", {'rule_name': rule_name, 'new_desc1': new_desc2})
        self.conn.commit()

    def change_budget(self, rule_name, new_budget):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if self.c.fetchone() == None:
            print('There\'s no rule called `{}` in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        
        self.c.execute("UPDATE rules SET rule_budget=:new_budget WHERE rule_name=:rule_name", {'rule_name': rule_name, 'new_budget': new_budget})
        self.conn.commit()

    def itemize(self):
        """Lists all rules"""
        self.c.execute("SELECT * FROM rules")
        rules = self.c.fetchall()
        if not rules:
            #print('There are currently no rules!')
            return None
        else:
            rule_list = []
            for rul in rules:
                rule_list.append([rul[1], rul[2], rul[3], rul[4]])
                print(rul)
            return rule_list

    def rename(self, rule_name, new_rule_name):
        """Renames an existing rule"""
        self.c.execute("SELECT * FROM rules WHERE rule_name=:new_rule_name", {'new_rule_name': new_rule_name})
        if (self.c.fetchone()):
            print('There\'s already a rule called `{}` in the Database! Aborting!'.format(new_rule_name))
            sys.exit(1)
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if (self.c.fetchone() != None):
            self.c.execute("UPDATE rules SET rule_name=:new_rule_name WHERE rule_name=:rule_name", {'rule_name': rule_name, 'new_rule_name': new_rule_name})
            print('Renamed rule `{}` to `{}`.'.format(rule_name, new_rule_name))
        else:
            print('Rule `{}` is not in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        self.conn.commit()

    def delete(self, rule_name):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
            print('Deleted rule `{}`.'.format(rule_name))
        else:
            print('Rule `{}` is not in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        self.conn.commit()
