# Updated expense.py

# Income and Expenditure tracking support

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.income = []

    def add_expense(self, amount, category):
        self.expenses.append({'amount': amount, 'category': category})

    def add_income(self, amount, source):
        self.income.append({'amount': amount, 'source': source})

    def get_total_expenses(self):
        return sum(exp['amount'] for exp in self.expenses)

    def get_total_income(self):
        return sum(inc['amount'] for inc in self.income)

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()