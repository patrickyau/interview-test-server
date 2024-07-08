from flask import jsonify, render_template, redirect, request
from app import app
from . import controllers
import json

@app.route('/tax-calculator/')
def tax_calculator_instructions():
    return jsonify({
        'tax_brackets': controllers.get_reliable_brackets()
    })


@app.route('/tax-calculator/tax-year')
def default_brackets():
    return redirect('/')


@app.route('/tax-calculator/tax-year/<tax_year>')
def tax_year_brackets(tax_year):
    return jsonify({
        'tax_brackets': controllers.get_unreliable_brackets(tax_year)
    })

# Add a POST route to calculate tax. POST is used to allow future expansion to include other criteria to calculate tax
@app.route('/tax-calculator/tax-year/<tax_year>', methods=['POST'])
def calculate_tax(tax_year):

    if not request.data: # Check if request body is empty
        return jsonify({
            'error': 'No request body is found'
        }), 400

    body = request.json
    if not 'salary' in body.keys(): # Check if 'salary' field is in the request body
        return jsonify({
            'error': 'No \'salary\' field is found in the request body'
        }), 400
    salary = body['salary']

    # Perform tax calculation logic here
    tax_amount, taxPerBracket = controllers.calculate_tax_amount(tax_year, salary)
    print(f'taxPerBracket2: {taxPerBracket}')
    effective_rate = tax_amount / salary
    return jsonify({
        'year': tax_year,
        'salary': salary,
        'tax_owed_per_band': json.loads(taxPerBracket),
        'total_tax_owed': tax_amount,
        'effective_tax_rate': f'{round(effective_rate * 100, 2)}%'
    })
