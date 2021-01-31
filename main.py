import os
from AccountHelper import AccountHelper
from BudgetHelper import BudgetHelper
from RuleHelper import RuleHelper
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
    #bud = BudgetHelper()
    #rul = RuleHelper()
    #acc.create('1', 'chequing', 'main', 1000)
    #acc.create('2', 'groceries', 'budget', 1000)
    #acc.create('3', 'fixed_expenses', 'budget', 1000)
    #acc.create('4', 'restaurantes', 'budget', 1000)
    #acc.create('5', 'mastercard', 'credit', 0)
    #bud.create_budget('groceries', 300, 'groceries')
    #bud.create_budget('restaurantes', 50, 'restaurantes')
    #bud.create_budget('videotron', 50, 'fixed_expenses')
    #rul.create_rule('videotron', 'VIDEOTRON', '', 'fixed_expenses')
    #rul.create_rule('3 Brasseurs', '3 BRASSEURS', '', 'restaurantes')

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

@account.command('list')
def list_accounts():
    acc = AccountHelper()
    acc.itemize()

@account.command('rename')
@click.argument('acc_name', required=True)
@click.argument('new_acc_name', required=True)
def rename_account(acc_name, new_acc_name):
    acc = AccountHelper()
    acc.rename(acc_name, new_acc_name)

@account.command('delete')
@click.argument('acc_name', required=True)
def delete_account(acc_name):
    acc = AccountHelper()
    acc.delete(acc_name)

@account.command('set_balance')
@click.argument('acc_name')
@click.argument('new_acc_balance')
def set_balance(acc_name, new_acc_balance):
    acc = AccountHelper()
    if acc.set_balance(acc_name, new_acc_balance):
        print('Set balance of account `{}` to `{}`.'.format(acc_name, new_acc_balance))
    else:
        print('Account `{}` is not in the Database! Aborting!'.format(acc_name))

#@account.command('associate_budget')
#@click.argument('acc_name')
#@click.argument('budget_name')
def associate_budget(acc_name, budget_name):
    acc = AccountHelper()
    acc.associate_budget(acc_name, budget_name)

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
    rul.create_rule(name, description1, description2, budget)

@rule.command('list')
def list_rules():
    rul = RuleHelper()
    rules = rul.list_rules()
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
    rul.rename_rule(rule_name, new_rule_name)

@rule.command('delete')
@click.argument('rule_name', required=True)
def delete_rule(rule_name):
    rul = RuleHelper()
    rul.delete_rule(rule_name)
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
    bud.create_budget(budget_name, budget_value, acc_name)
    
@budget.command('list')
def list_budgets():
    bud = BudgetHelper()
    budgets = bud.list_budgets()
    if budgets:
        print('Listing all budgets:')
        for budget in budgets:
            print('Budget `{}` of value {} maps to account `{}`'.format(budget[0], budget[1], budget[2]))
    else:
        print('There are currently no budgets!')

@budget.command('rename')
@click.argument('budget_name', required=True)
@click.argument('new_budget_name', required=True)
def rename_budget(budget_name, new_budget_name):
    bud = BudgetHelper()
    bud.rename_budget(budget_name, new_budget_name)

@budget.command('delete')
@click.argument('budget_name', required=True)
def delete_budget(budget_name):
    bud = BudgetHelper()
    bud.delete_budget(budget_name)
    
@budget.command('change_value')
@click.argument('budget_name', required=True)
@click.argument('new_budget_value', required=True)
def change_budget_value(budget_name, new_budget_value):
    bud = BudgetHelper()
    bud.change_budget_value(budget_name, new_budget_value)

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

##################################################################