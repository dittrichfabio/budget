import re
import sys
import csv
from AccountHelper import AccountHelper
from BudgetHelper import BudgetHelper
from RuleHelper import RuleHelper

#CSV file has these fields (2/23/19):
#['Account Type', 'Account Number', 'Transaction Date', 'Cheque Number', 'Description 1', 'Description 2', 'CAD$', 'USD$']
#We are only interested in 'Account Number', 'Description1', 'Description2' and 'CAD$', therefore we filter by [1, 4, 5, 6]
CSV_FILTER = [1, 4, 5, 6]

class CalculateHelper:

    def __init__(self):
        pass

    def load_csv(self, csv_file):
        with open(csv_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            data = list(reader)
        filtered_data = [[line[i] for i in CSV_FILTER] for line in data]
        
        #remove header
        filtered_data.pop(0)

        r = RuleHelper()
        rules = r.itemize()
        for rul in rules:
            print(rul)

        resolved_list = []
        unresolved_list = []

        for line in filtered_data:
            #positive transactions, i.e. incoming money
            if float(line[3]) > 0:
                continue
                #TODO:we might want to change this in the future
            found_match = False
            for rule in rules:
                #print('rule', rule)
                if rule[1] and not rule[2]:
                    #print('r1')
                    match_desc1 = re.search(rule[1], line[1])
                    if match_desc1:
                        found_match = True
                        #print('r1 match')
                        break
                elif rule[2] and not rule[1]:
                    #print('r2')
                    match_desc2 = re.search(rule[2], line[2])
                    if match_desc2:
                        found_match = True
                        #print('r2 match')
                        break
                else:
                    #print('r1&2')
                    match_desc1 = re.search(rule[1], line[1])
                    match_desc2 = re.search(rule[2], line[2])
                    if match_desc1 and match_desc2:
                        found_match = True
                        #print('r1&2 match')
                        break
            #print('\n\n')
            if found_match:
                #print("Line {0} matches rule {1}".format(line, rule))
                resolved_list.append([line, rule[3]])
            else:
                #print("Line {0} does not match any rules".format(line))
                unresolved_list.append(line)

        
        print('The lines presented below have been already associated to a budget based on the rules:')
        for i in resolved_list:
            print(i)
        print('\n\n')
        
        print(len(resolved_list))
        print(resolved_list, '\n\n')
        print(len(unresolved_list))
        print(unresolved_list, '\n\n\n\n\n\n')
        expenses_by_budget, resolved = self.get_manual_input(unresolved_list)
        resolved_list.extend(resolved)

        print('\n\n', expenses_by_budget, '\n\n')
        print('\n\n', resolved_list, '\n\n')

        #print('\n\n')
        #for i in resolved_list:
            #print(i)
        #print('\n\n')
        #go over list of things to resolve and allow user to input resolution
        #add resolutions to list of resolved
        #go over resolved list, compute values and show as output
        #expenses_by_budget = {}
        for i in resolved_list:
            expenses_by_budget[i[1]] += float(i[0][3])

        print('\nSum of expenses for each budget:')
        for i in sorted(expenses_by_budget):
            print(i, expenses_by_budget[i])

        bud = BudgetHelper()
        budgets = bud.itemize()
        budget_values = {}
        budget_accounts = {}
        for bname, bvalue, bacc, _ in budgets:
            budget_values[bname] = bvalue
            budget_accounts[bname] = bacc

        print('\n\nBudget values for each budget:')
        for i in sorted(budget_values):
            print(i, budget_values[i])

        budget_balance = {}
        for i in expenses_by_budget:
            budget_balance[i] = round(expenses_by_budget[i] + budget_values[i],2)

        print('\n\nBudget balances for each budget:')
        for i in sorted(budget_balance):
            print(i, f"\t\t{budget_balance[i]}")

        acc = AccountHelper()
        accounts_names = [a[1] for a in acc.itemize()]

        print('\n\n\n')
        #account['Acc'] = [spendings, sum of all budgets for account, balance]
        accounts = {}
        for i in accounts_names:
            accounts[i] = [0.0, 0.0, 0.0]

        for i in budget_balance:
            print("Budget ", i)
            associated_acc = budget_accounts[i]
            print('\taccount ', associated_acc)
            #if associated_acc not in account_balances:
            #    account_balances[associated_acc] = budget_balance[i]
            #else:
            accounts[associated_acc][0] += expenses_by_budget[i]
            accounts[associated_acc][1] += budget_values[i]
            accounts[associated_acc][2] += budget_balance[i]

        print('\nAccount balances:')
        for i in sorted(accounts):
            print(i.replace(' ', '_'), '\t', accounts[i][0], '\t', accounts[i][1], '\t', accounts[i][2])

        #self.apply_budget()

    def get_manual_input(self, unresolved_list):
        bud = BudgetHelper()
        budgets = bud.itemize()
        budgets = [i[0] for i in budgets]
        print(sorted(budgets))
        expenses_by_budget = {}
        for i in budgets:
            expenses_by_budget[i] = 0
        print('Please provide the associated budget to each of the lines presented below:')
        resolved_list = []
        for i in unresolved_list:
            b = ''
            while b not in budgets:
                b = input("{0}:\n".format(i))
            resolved_list.append([i, b])
        return expenses_by_budget, resolved_list

    def apply_budget(self):
        acc = AccountHelper()
        bud = BudgetHelper()
        budgets = bud.itemize()
        for bname, bvalue, bacc in budgets:
            acc.increase_balance_by(bacc, bvalue)
            