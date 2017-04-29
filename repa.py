import sys
from base import Base
from gen import generate

ARGS = sys.argv[1:]
SOURCE_FILE = 'repassgen_data/source'
BASE_FILE = 'repassgen_data/base'


def collect_new_defaults():
    new_default_length = int(input('Enter new default value for passwords length (min 6): => '))
    if not (isinstance(new_default_length, int) and new_default_length > 5):
        return {'err': 'Length must be an integer value (min 6)!', 'dat': ''}
    new_default_complexity = input('Enter new default passwords complexity code (one of: a, A, n, N, s, S, f, F): => ')
    if new_default_complexity not in list('aAnNsSfF'):
        return {'err': 'Complexity code must be one of: a, A, n, N, s, S, f, F', 'dat': ''}
    new_default_amount = int(input('Enter new default value for passwords amount (min 1): => '))
    if not (isinstance(new_default_amount, int) and new_default_amount > 0):
        return {'err': 'Length must be an integer value (min 6)!', 'dat': ''}
    return {'err': '', 'dat': [new_default_length, new_default_complexity, new_default_amount]}


def main():
    """Name: repassgen.py - python3 script which generates readable passwords resembling english words. 
    
    Usage: python3 repassgen.py [ h \ p \ d \ u \[length] [complexity] [amount]]
    
    Keys descritpion:
    no keys     -   Runs script with default parameters of length, complexity and amount.
    h           -   Prints this message.
    p           -   Prints current default parameters.
    d           -   Interactively set new default parameters.
    u           -   Updates base with text provided in source file.
    length      -   Length of passwords to gererate: integer number (min 6)
    complexity  -   Complexity code: single character from [ a A n N s S f F ] which represents following patterns:
                        a - 'abcd', A - 'aBcD', n - 'a2c4', N - 'a2C4', s - 'a@c$', S - 'a@C$', f - 'a2c$', F - 'a2C$'
    amount      -   Amount of passwords to generete: integer number (min 1) preceeded by 'x', i.e. 'x10' 
    """
    base = Base(SOURCE_FILE, BASE_FILE)
    if len(ARGS) > 3:
        print('Error: Wrong number of passed arguments!')
        print(main.__doc__)
    if len(ARGS) == 1:
        if ARGS[0] == 'h':
            print(main.__doc__)
        elif ARGS[0] == 'p':
            get_defaults_result = base.get_defaults()
            if get_defaults_result['err']:
                print(get_defaults_result['err'])
            else:
                defs = get_defaults_result['dat']
                print('Current defaults are: length: {}, complexity: {}, amount: {}'.format(defs[0], defs[1], defs[2]))
        elif ARGS[0] == 'd':
            get_defaults_result = base.get_defaults()
            if get_defaults_result['err']:
                print(get_defaults_result['err'])
            else:
                print(get_defaults_result['dat'])
                new_defaults_res = collect_new_defaults()
                if new_defaults_res['err']:
                    print(new_defaults_res['err'])
                else:
                    set_defaults_res = base.set_defaults(new_defaults_res['dat'])
                    if set_defaults_res['err']:
                        print(set_defaults_res['err'])
                    else:
                        print(set_defaults_res['dat'])
        elif ARGS[0] == 'u':
            update_res = base.update()
            if update_res['err']:
                print(update_res['err'])
            else:
                print(update_res['dat'])
        else:
            pass
    args_list = list(ARGS)



