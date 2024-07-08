import os
import json

brackets_dir = os.path.join(os.path.dirname(__file__), 'fixtures')

def _get_brackets(tax_year):
  
    filename = f'tax-brackets--{tax_year}.json'
    file_with_path = os.path.join(brackets_dir, filename)

    with open(file_with_path) as config_file:
        json_contents = json.load(config_file)
        config_file.close()

    return json_contents


def test_basic_route(client): 
  resp = client.get('/tax-calculator/')
  brackets = _get_brackets('2022')
  assert resp.json == {'tax_brackets': brackets}


# Test the new route that returns the tax brackets for a specific year
def test_calculate_tax_amount(client):
    salary = 1234567
    tax_year = '2022'
    brackets = _get_brackets(tax_year)
    for bracket in brackets:
        if income > bracket['min']:
            taxable_income = min(income, bracket['max']) - bracket['min']
            tax_amount += taxable_income * bracket['tax']
    
    brackets = get_tax_brackets(tax_year)
    taxPerBracket = []

    # Calculate the tax amount based on the income and tax brackets
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
    effective_rate = tax_amount / salary

    # Make a POST request to calculate tax
    resp = client.post('/tax-calculator/tax-year/2022', json={'salary': income})
\
    assert resp.json == {
        'year': tax_year,
        'salary': salary,
        'tax_owed_per_band': taxPerBracket, # Convert the string to a JSON object
        'total_tax_owed': tax_amount,
        'effective_tax_rate': f'{round(effective_rate * 100, 2)}%'
    }
