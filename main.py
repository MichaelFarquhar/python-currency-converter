from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError

import sys
import api

def quit_program():
    print('\nQuitting...')
    sys.exit()

class NumberValidator(Validator):
    def validate(self, document):
        currency_list = {'cad', 'usd'}
        text = document.text

        # If q is entered, quit
        if text.lower() == 'q':
            quit_program()

        # Handle no input
        if len(text.strip()) <= 0:
            raise ValidationError(message='Please enter a currency code.')
        
        # Handle incorrect currency entered
        if text.lower() not in currency_list:
            raise ValidationError(message='Please enter a valid currency.', cursor_position=len(text))

def main():
    print('\nCURRENCY CONVERTER')
    print('─' * 18)
    print('[TAB] - See full list of currencies')
    print('[Q] - Quit')
    print("")
    api.get_status()
    # html_completer = WordCompleter(['usd', 'cad', 'jap', 'aus'])
    # text = prompt('Enter Currency: ', completer=html_completer, complete_while_typing=True, validator=NumberValidator(), validate_while_typing=False)
    # print('You said: %s' % text)

if __name__ == "__main__":
    main()