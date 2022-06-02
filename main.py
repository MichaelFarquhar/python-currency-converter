from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError

import sys
import api
import style

def quit_program():
    '''Quits program while printing a message'''
    print('\nQuitting...')
    sys.exit()

class MainMenuValidator(Validator):
    '''Validator for Main Menu - Only allow the user to select options 1, 2 or 3'''
    def validate(self, document):
        options = {'1','2','3'}
        text = document.text

        if text.strip() not in options:
            raise ValidationError(message='Please enter a valid option.')

def main():
    # Main Menu
    # Loop endless until the users pick the quit option from the main menu
    while True:
        # Menu title
        style.print_title('Main Menu')

        # Menu options and input
        print("[1] Convert Currency\n[2] See Api Status\n[3] Quit\n")
        menu_selection = prompt('Enter number: ', validator=MainMenuValidator())

        # [1] Start currency conversion
        if int(menu_selection) == 1:
            api.convert_currency()
        # [2] See the current api quota
        elif int(menu_selection) == 2:
            api.get_status()
        # [3] Quit program
        elif int(menu_selection) == 3:
            quit_program()


if __name__ == "__main__":
    main()