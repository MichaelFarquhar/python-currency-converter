import requests
from requests.structures import CaseInsensitiveDict

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

from tabulate import tabulate
import os
import style
from currency_codes import get_currency_codes

currency_codes = get_currency_codes()

def start_request(endpoint: str):
    '''Make a request to a specified endpoint'''
    url = f"https://api.currencyapi.com/v3/{endpoint}"

    headers = CaseInsensitiveDict()
    headers["apikey"] = os.environ['API_KEY']

    try:
        return requests.get(url, headers=headers)
    except requests.RequestException as e:
        print(f'Error: {e}')

def get_status():
    '''Make a get request to the status endpoint and print out the data'''
    resp = start_request('status')
    data = resp.json()

    # Print table title
    style.print_title('Api Quotas')
    
    # Style and print table
    table_headers = ['Total', 'Used', 'Remaining']
    table = [[str(x) for x in data['quotas']['month'].values()]]
    print(tabulate(table, table_headers, tablefmt="pretty"))

class NumberValidation(Validator):
    def validate(self, document):
        text = document.text.strip()
        
        # Handle error for non-numeric
        if not text.isdigit():
            raise ValidationError(message='Please enter a valid number.', cursor_position=len(text))

class CurrencyValidation(Validator):
    def validate(self, document):
        text = document.text.strip()

        # Handle no input
        if len(text) <= 0:
            raise ValidationError(message='Please enter a currency code.')
        
        # Handle incorrect currency entered
        if text.upper() not in currency_codes:
            raise ValidationError(message='Please enter a valid currency.', cursor_position=len(text))

def get_convertion(base: str, conversion: str, amount: float):
    '''Receives a base and conversion currency. Makes call to api to get the conversion rate'''
    # Make request to api 'latest' endpoint
    resp = start_request("latest?apikey={}&currencies={}&base_currency={}".format(os.environ['API_KEY'], conversion, base))
    data = resp.json()

    # Calculate Amount
    converted_amount = amount * float(data['data'][conversion]['value'])

    # Print out amount in a pretty table format
    print("")
    table_headers = ["Conversion Complete"]
    table = [[f"\n{base} ${amount} -> {conversion} ${round(converted_amount, 2)}"]]
    print(tabulate(table, table_headers, tablefmt="pretty"))


def convert_currency():
    '''Recieve various inputs and then makes a call to api to convert currency'''

    style.print_title('Convert Currency')
    print("[TAB] -> See all currency options\n")

    # Base currency prompt
    html_completer = WordCompleter([c.lower() for c in currency_codes])
    base_currency = prompt('Enter Base Currency: ', completer=html_completer, complete_while_typing=True, validator=CurrencyValidation(), validate_while_typing=False)

    # Conversion to convert to prompt
    conversion_currency = prompt('Enter Conversion Currency: ', completer=html_completer, complete_while_typing=True, validator=CurrencyValidation(), validate_while_typing=False)

    # Enter amount prompt
    amount = prompt('Enter Amount: ', validator=NumberValidation(), validate_while_typing=True)

    get_convertion(base_currency.upper(), conversion_currency.upper(), float(amount))