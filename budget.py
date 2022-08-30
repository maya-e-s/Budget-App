class Category:
    def __init__(self, cat):
        self.cat = cat # category such as food, clothing, entertainment
        self.ledger = list() # list of dict in format of {"amount": amount, "description": description}
        self.funds = 0.0
    
    # Format how the budget object is printed
    def __str__(self):
        ret = self.cat.center(30, '*') + "\n"
        for item in self.ledger:
            amount = "{:.2f}".format(item.get('amount'))
            line = (item.get('description'))[:23].ljust(23, ' ') + amount.rjust(7, ' ')
            ret += line + '\n'
        ret += "Total: " + "{:.2f}".format(self.funds)
        return ret

    def deposit(self, amount, desc=''):
        self.ledger.append({'amount':amount, 'description':desc})
        self.funds += amount

    # return True if the withdrawal took place, and False otherwise
    def withdraw(self, amount, desc=''):
        if self.check_funds(amount): # if there are not enough funds, nothing should be added to the ledger
            self.ledger.append({'amount':-1*amount, 'description':desc})
            self.funds -= amount
            return True
        else: return False

    # return True if the transfer took place, and False otherwise
    def transfer(self, amount, category_inst):
        desc1 = "Transfer to " + category_inst.cat
        desc2 = "Transfer from " + self.cat
        if self.withdraw(amount, desc1): # if there are not enough funds, nothing should be added to either ledgers
            category_inst.deposit(amount, desc2)
            return True
        return False

    # returns False if the amount is greater than the balance of the budget category and returns True otherwise
    def check_funds(self, amount): 
        if amount > self.funds: return False
        return True 

    def get_balance(self):
        return self.funds

# input: list of Category objects 
# output: string that is a bar chart showing the percentage spent (only withdraws) in each category
def create_spend_chart(categories):
    # calculate spending per category and total spending
    sum = 0.0
    cat_title = list()
    spending = list()
    for category in categories:
        # sum withdrawals
        withdraws = 0.0
        for item in category.ledger:
            if item.get('amount') < 0: 
                withdraws += item.get('amount')
                sum += item.get('amount')
        # add to lists
        cat_title.append(category.cat)
        spending.append(withdraws)
    # calculate percent per category
    for i in range(len(spending)):
        spending[i] = int(spending[i]/sum*10)*10 # calculate percent and round down to the nearest 10   
    # format bar chart as a string
    chart = 'Percentage spent by category\n'
    for val in range(100,-1,-10):
        line = str(val).rjust(3,' ') + '| '
        for s in spending:
            if s>=val: line+='o  '
            else: line+='   '
        chart += line + '\n'
    chart += '    -' + '---'*len(spending)
    # add chart labels 
    for i in range(len(max(cat_title, key=len))):
        line = '\n     '
        for c in cat_title:
            if len(c) > i: line += c[i] + '  '
            else: line += '   '
        chart += line
    print(chart) 
    return chart