from AccountHelper import AccountHelper
from BudgetHelper import BudgetHelper
from RuleHelper import RuleHelper
import click



@click.group()
@click.version_option()
def cli():
    """Budget"""

#ACCOUNTS
##################################################################
@cli.group()
def account():
    """Manages accounts"""

@account.command('create')
@click.argument('acc_number', required=True)
@click.argument('acc_name', required=True)
@click.argument('acc_balance', required=True)
def create_account(acc_number, acc_name, acc_balance):
    acc = AccountHelper()
    acc.create_account(acc_number, acc_name, acc_balance)

@account.command('list')
def list_accounts():
    acc = AccountHelper()
    acc.list_accounts()

@account.command('rename')
@click.argument('acc_name', required=True)
@click.argument('new_acc_name', required=True)
def rename_account(acc_name, new_acc_name):
    acc = AccountHelper()
    acc.rename_account(acc_name, new_acc_name)

@account.command('delete')
@click.argument('acc_name', required=True)
def delete_account(acc_name):
    acc = AccountHelper()
    acc.delete_account(acc_name)

@account.command('set_balance')
@click.argument('acc_name')
@click.argument('new_acc_balance')
def set_balance(acc_name, new_acc_balance):
    acc = AccountHelper()
    acc.set_balance(acc_name, new_acc_balance)

#@account.command('get_account_id')
#@click.argument('acc_name')
def get_account_id(acc_name):
    acc = AccountHelper()
    print(acc.get_account_id(acc_name))
##################################################################

#RULE
##################################################################
@cli.group()
def rule():
    """Budget rules management"""

@rule.command('create')
@click.argument('name', required=True)
@click.argument('description1', required=True)
@click.argument('description2', required=True)
@click.argument('acc_name', required=True)
def create_rule(name, description1, description2, acc_name):
    rul = RuleHelper()
    rul.create_rule(name, description1, description2, acc_name)

@rule.command('list')
def list_rules():
    rul = RuleHelper()
    rul.list_rules()

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
    """Budget rules management"""

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
    bud.list_budget()
    
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