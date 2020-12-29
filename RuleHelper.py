import sys
import sqlite3
import Rule
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

    def create_rule(self, rule_name, rule_description1, rule_description2, rule_budget):
        """Checks if rule already exists (both descriptions). If it doesn't, creates it."""
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if (self.c.fetchone() != None):
            print('There\'s already a rule called `{}` in the Database! Aborting!'.format(rule_name))
            sys.exit(1)

        bud = BudgetHelper()
        budgets = bud.list_budgets()
        budgets = [i[0] for i in budgets]

        if rule_budget in budgets:
            self.c.execute("INSERT INTO rules VALUES (NULL, :rule_name, :rule_description1, :rule_description2, :rule_budget)", {'rule_name': rule_name, 'rule_description1': rule_description1, 'rule_description2': rule_description2, 'rule_budget': rule_budget})
            print('Created rule {}: description1 = `{}`, description2 = `{}` that maps to budget `{}`.'.format(rule_name, rule_description1, rule_description2, rule_budget))
        else:
            print('Budget `{}` doesn\'t exist!'.format(rule_budget))
            sys.exit(1)

        self.conn.commit()

    def list_rules(self):
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
            return rule_list

    def rename_rule(self, rule_name, new_rule_name):
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

    def delete_rule(self, rule_name):
        self.c.execute("SELECT * FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
        if (self.c.fetchone() != None):
            self.c.execute("DELETE FROM rules WHERE rule_name=:rule_name", {'rule_name': rule_name})
            print('Deleted rule `{}`.'.format(rule_name))
        else:
            print('Rule `{}` is not in the Database! Aborting!'.format(rule_name))
            sys.exit(1)
        self.conn.commit()
