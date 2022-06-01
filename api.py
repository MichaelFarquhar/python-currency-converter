from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
import requests
from requests.structures import CaseInsensitiveDict
from tabulate import tabulate
import os

def get_status():
    url = "https://api.currencyapi.com/v3/status"

    headers = CaseInsensitiveDict()
    headers["apikey"] = os.environ['API_KEY']

    resp = requests.get(url, headers=headers)
    data = resp.json()
    print(resp.status_code)
    print(data)

    # Style and print table title
    table_title = FormattedText([
        ('#00c7ff bold', '\nAPI QUOTAS')
    ])
    print_formatted_text(table_title)
    
    # Style and print table
    table_headers = ['Total', 'Used', 'Remaining']
    table = [[str(x) for x in data['quotas']['month'].values()]]
    print(tabulate(table, table_headers, tablefmt="pretty"))