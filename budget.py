from AccountHelper import AccountHelper
import click



@click.group()
@click.version_option()
def cli():
    """Budget"""

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

