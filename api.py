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

class CurrencyValidation(Validator):
    def validate(self, document):
        text = document.text.strip()

        # Handle no input
        if len(text) <= 0:
            raise ValidationError(message='Please enter a currency code.')
        
        # Handle incorrect currency entered
        if text.upper() not in currency_codes:
            raise ValidationError(message='Please enter a valid currency.', cursor_position=len(text))

def convert_currency():
    '''Recieve various inputs and then makes a call to api to convert currency'''
    html_completer = WordCompleter([c.lower() for c in currency_codes])
    text = prompt('Enter Currency: ', completer=html_completer, complete_while_typing=True, validator=CurrencyValidation(), validate_while_typing=False)
    print('You said: %s' % text)