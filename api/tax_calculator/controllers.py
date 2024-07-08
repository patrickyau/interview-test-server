import random, json
from api.utils import naptime
from .tax_brackets import get_tax_brackets


def get_reliable_brackets():
    return get_tax_brackets()


def get_unreliable_brackets(tax_year):
    naptime()

    # be evil
    roulette = random.randint(1, 4)
    print(f'Database roulette {roulette}')
    # if roulette == 3:
    #     raise Exception("Database not found!")

    return get_tax_brackets(tax_year)
    
def calculate_tax_amount(tax_year, income):
    brackets = get_tax_brackets(tax_year)
    taxPerBracket = []

    tax_amount = 0
    for bracket in brackets:
        if income > bracket['min']:
            leftover = income
            if 'max' in bracket.keys():
                leftover = min(income, bracket['max'])
            taxable_income = leftover - bracket['min']
            tax = taxable_income * bracket['rate']
            tax_amount += tax
            bracket['tax_owed'] = round(tax, 2)
            taxPerBracket.append(bracket)

    return round(tax_amount, 2), json.dumps(taxPerBracket) # Convert the list to a string to be returned in the response body