import os
from AccountHelper import AccountHelper
from BudgetHelper import BudgetHelper
from RuleHelper import RuleHelper
from TransactionHelper import TransactionHelper
from Calculate import CalculateHelper
import click



@click.group()
@click.version_option()
def cli():
    """Budget"""

#BOOTSTRAP
##################################################################
@cli.group()
def bootstrap():
    """Creates accounts, budgets and rules for testing"""

@bootstrap.command('run')
def run():
    if os.path.exists('/mnt/c/Users/fabio_dittrich/Documents/Budget/db/budget.db'):
        os.remove('/mnt/c/Users/fabio_dittrich/Documents/Budget/db/budget.db')
    acc = AccountHelper()
    bud = BudgetHelper()
    rul = RuleHelper()
    TransactionHelper().create('08/22/2021', 'desc11', 'MARI' , -33.33, 'groceries')
    TransactionHelper().create('09/22/2021', 'FIZZ', 'MARI' , -34.34, 'condo')
    TransactionHelper().create('10/22/2021', 'desc12', 'desc22' , -35.35, 'groceries')
    TransactionHelper().create('11/22/2021', 'FIZZ', 'FABIO' , -36.36, 'condo')
    TransactionHelper().create('12/22/2021', 'FIZZ', 'MARI' , -37.37, 'groceries')
    TransactionHelper().create('12/23/2021', 'MARI', 'FIZZ' , -38.38, 'internet')
    TransactionHelper().itemize(begin='', end='')
    TransactionHelper().itemize(begin='10/22/2021', end='')
    TransactionHelper().itemize(begin='', end='09/22/2021')
    TransactionHelper().itemize(begin='10/22/2021', end='11/22/2021')
    TransactionHelper().itemize(desc1="FABIO")
    TransactionHelper().itemize(desc1="FIZZ")
    TransactionHelper().itemize(desc1="FIZZ", desc2="MARI")
    TransactionHelper().itemize(desc1="FIZZ", desc2="MARI", begin="10/22/2021")
    TransactionHelper().itemize(anydesc='MARI')
    TransactionHelper().itemize(budget='groceriesa')
    TransactionHelper().itemize(budget='groceries')
    TransactionHelper().itemize(begin='10/22/2021', end='', budget='groceries')
    TransactionHelper().itemize(anydesc='MARI', budget='groceries')
    TransactionHelper().itemize(desc1="FIZZ", desc2="MARI", budget='groceries')
    TransactionHelper().itemize(desc1="FIZZ", desc2="MARI", begin="10/22/2021", budget='groceries')


    acc.create('1', 'chequing', 1000)
    acc.create('2', 'groceries', 1000)
    acc.create('3', 'fixed_expenses', 1000)
    bud.create('groceries', 300, 'groceries', 0)
    bud.create('condo', 50, 'fixed_expenses', 0)
    bud.create('internet', 50, 'fixed_expenses', 0)
    rul.create('internet', 'VIDEOTRON', '', 'internet')
    rul.create('condo', 'Condo Fee', '', 'condo')
    rul.create('groceries', 'PROVIGO', '', 'groceries')

#ACCOUNTS
##################################################################
@cli.group()
def account():
    """Manages Accounts"""

@account.command('create')
@click.argument('acc_number', required=True)
@click.argument('acc_name', required=True)
@click.argument('acc_balance', required=True)
def create_account(acc_number, acc_name, acc_balance):
    acc = AccountHelper()
    acc.create(acc_number, acc_name, acc_balance)

@account.command('save_csv')
@click.argument('account_csv_file', required=True)
def save_account_csv(account_csv_file):
    acc = AccountHelper()
    acc.save_csv(account_csv_file)

@account.command('load_csv')
@click.argument('account_csv_file', required=True)
def load_account_csv(account_csv_file):
    acc = AccountHelper()
    acc.load_csv(account_csv_file)

@account.command('list')
def list_accounts():
    acc = AccountHelper()
    acc.itemize()

@account.command('rename')
@click.argument('acc_number', required=True)
@click.argument('new_acc_name', required=True)
def rename_account(acc_number, new_acc_name):
    acc = AccountHelper()
    acc.rename(acc_number, new_acc_name)

@account.command('delete')
@click.argument('acc_number', required=True)
def delete_account(acc_number):
    acc = AccountHelper()
    acc.delete(acc_number)

@account.command('set_balance')
@click.argument('acc_number')
@click.argument('new_acc_balance')
def set_balance(acc_number, new_acc_balance):
    acc = AccountHelper()
    if acc.set_balance(acc_number, new_acc_balance):
        print('Set balance of account `{}` to `{}`.'.format(acc_number, new_acc_balance))
    else:
        print('Account `{}` is not in the Database! Aborting!'.format(acc_number))

#@account.command('get_account_id')
#@click.argument('acc_name')
def get_account_id(acc_name):
    acc = AccountHelper()
    print(acc.get_id(acc_name))
##################################################################

#RULE
##################################################################
@cli.group()
def rule():
    """Manages Rules"""

@rule.command('create')
@click.argument('name', required=True)
@click.argument('description1', required=True)
@click.argument('description2', required=True)
@click.argument('budget', required=True)
def create_rule(name, description1, description2, budget):
    rul = RuleHelper()
    rul.create(name, description1, description2, budget)

@rule.command('save_csv')
@click.argument('rule_csv_file', required=True)
def save_rule_csv(rule_csv_file):
    rul = RuleHelper()
    rul.save_csv(rule_csv_file)

@rule.command('load_csv')
@click.argument('rule_csv_file', required=True)
def load_rule_csv(rule_csv_file):
    rul = RuleHelper()
    rul.load_csv(rule_csv_file)

@rule.command('list')
def list_rules():
    rul = RuleHelper()
    rules = rul.itemize()
    if rules:
        print('Listing all rules:')
        for rule in rules:
                print('Rule `{}`: rule_description1 = `{}`, rule_description2 = `{}` that maps to budget `{}`'.format(rule[0], rule[1], rule[2], rule[3]))
    else:
        print('There are currently no rules!')


@rule.command('rename')
@click.argument('rule_name', required=True)
@click.argument('new_rule_name', required=True)
def rename_rule(rule_name, new_rule_name):
    rul = RuleHelper()
    rul.rename(rule_name, new_rule_name)

@rule.command('delete')
@click.argument('rule_name', required=True)
def delete_rule(rule_name):
    rul = RuleHelper()
    rul.delete(rule_name)
##################################################################

#BUDGET
##################################################################
@cli.group()
def budget():
    """Manages Budgets"""

@budget.command('create')
@click.argument('budget_name', required=True)
@click.argument('budget_value', required=True)
@click.argument('acc_name', required=True)
def create_budget(budget_name, budget_value, acc_name):
    bud = BudgetHelper()
    bud.create(budget_name, budget_value, acc_name)
    
@budget.command('save_csv')
@click.argument('budget_csv_file', required=True)
def save_budget_csv(budget_csv_file):
    bud = BudgetHelper()
    bud.save_csv(budget_csv_file)

@budget.command('load_csv')
@click.argument('budget_csv_file', required=True)
def load_budget_csv(budget_csv_file):
    bud = BudgetHelper()
    bud.load_csv(budget_csv_file)

@budget.command('list')
def list_budgets():
    bud = BudgetHelper()
    budgets = bud.itemize()
    if budgets:
        print('Listing all budgets:')
        for budget in budgets:
            print('Budget `{}` of value {} maps to account `{}` and has a balance of `{}`'.format(budget[0], budget[1], budget[2], budget[3]))
    else:
        print('There are currently no budgets!')

@budget.command('rename')
@click.argument('budget_name', required=True)
@click.argument('new_budget_name', required=True)
def rename_budget(budget_name, new_budget_name):
    bud = BudgetHelper()
    bud.rename(budget_name, new_budget_name)

@budget.command('delete')
@click.argument('budget_name', required=True)
def delete_budget(budget_name):
    bud = BudgetHelper()
    bud.delete(budget_name)
    
@budget.command('change_value')
@click.argument('budget_name', required=True)
@click.argument('new_budget_value', required=True)
def change_budget_value(budget_name, new_budget_value):
    bud = BudgetHelper()
    bud.change_budget_value(budget_name, new_budget_value)

@budget.command('change_balance')
@click.argument('budget_name', required=True)
@click.argument('new_budget_balance', required=True)
def change_budget_balance(budget_name, new_budget_balance):
    bud = BudgetHelper()
    bud.change_budget_balance(budget_name, new_budget_balance)

@budget.command('change_account')
@click.argument('budget_name', required=True)
@click.argument('new_budget_account', required=True)
def change_budget_value(budget_name, new_budget_account):
    bud = BudgetHelper()
    bud.change_budget_account(budget_name, new_budget_account)
##################################################################

#EXECUTE
##################################################################
@cli.group()
def calculate():
    """Calculate budget"""

@calculate.command('load_csv')
@click.argument('csv_file', required=True)
def load_csv(csv_file):
    cal = CalculateHelper()
    cal.load_csv(csv_file)

#TODO: create wrapper function that runs load_budget_csv, load_account_csv and load_rule_csv. At the end, check if there are any old budgets without account and delete them
#TODO: implement load_budget_csv, load_account_csv, load_rule_csv (update)
#TODO: implement save_budget_csv, save_account_csv, save_rule_csv
#TODO: bootstrap with a simplified version of our actual budget
#TODO: load_csv function
    #goes over each entry in the csv and applies the rules
    #whatever entries are not covered, get manual input
    #gets a trigger to create the transactions in the DB, apply budget values, calculate how much money goes from one account to another and update accounts/budgets
    #prints that info to screen and commits to DB


##################################################################

if __name__ == "__main__":
    #run()
    #load_budget_csv(["budgets.csv"])
    #load_account_csv(["accounts.csv"])
    #load_rule_csv(["rules.csv"])
    #save_budget_csv(["budgets2.csv"])
    #save_account_csv(["accounts2.csv"])
    save_rule_csv(["rules2.csv"])