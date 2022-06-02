from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText

def print_title(title: str):
    '''Print out a stylish blue title given a string'''
    menu_title = FormattedText([
        ('#00c7ff bold', f'\n{title.upper()}')
    ])
    print_formatted_text(menu_title)