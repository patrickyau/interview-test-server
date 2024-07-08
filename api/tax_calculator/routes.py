from flask import jsonify, render_template, redirect, request
from app import app
from . import controllers
import json
from api.error_handlers import format_error

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
        print(f'No request body is found for year {tax_year}')
        return jsonify({
            'errors': format_error(
                'No request body is found for tax year ' + tax_year,
                code='BAD_REQUEST'
            )
        }), 400

    body = request.json
    if not 'salary' in body.keys(): # Check if 'salary' field is in the request body
        print('No \'salary\' field is found in the request body')
        return jsonify({
            'errors': format_error(
                'No \'salary\' field is found in the request body',
                field='salary',
                code='BAD_REQUEST'
            )
        }), 400
    salary = body['salary']
    if salary < 0: # Check if 'salary' field is less than zero
        print('The \'salary\' value should be greater than or equal to 0')
        return jsonify({
            'errors': format_error(
                'The \'salary\' value should be greater than or equal to 0',
                field='salary',
                code='BAD_REQUEST'
            )
        }), 400

    # Perform tax calculation logic here
    tax_amount, taxPerBracket = controllers.calculate_tax_amount(tax_year, salary)
    effective_rate = tax_amount / salary
    return jsonify({
        'year': tax_year,
        'salary': salary,
        'tax_owed_per_band': json.loads(taxPerBracket), # Convert the string to a JSON object
        'total_tax_owed': tax_amount,
        'effective_tax_rate': f'{round(effective_rate * 100, 2)}%'
    })
