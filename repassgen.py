import re
import sys


def split_vcv(word):
    """ Splits word argument into array of chunks consisting of groups Vowels-Consonants-Vowels or Consonants-Vowels
    i.e: 'bamboo' => ['ba', 'amboo']; 'umbrella' => ['umbre', 'ella']
    
    :arg:
        1. word: string
    :return:
        1. array of strings
    """
    return re.findall(r'(?=([aeiou]+[^aeiou]+[aeiou]|^[aeiou]+[aeiou]+))', word)


def update_base():
    """ Rewrites VCV data of base.txt by combining it via set with splittes to VCV chunks text data from source.txt 
    
    :arg:
        none
    :return:
        none
    """
    with open('source.txt', mode='r') as source:
        src_data = source.read()
        words = re.sub(r'[^a-zA-Z]', ' ', src_data).strip().lower().split()
        with open('base.txt', mode='r') as base:
            data = base.read()
            base_set = set(data.split())
            for word in words:
                base_set.update(split_vcv(word))
        with open('base', mode='w') as base:
            base.write(' '.join(base_set))
    print('Complete!')
    return


def load_defaults():
    """ Returns dictionary with default options for pasword generation based on data from defaults.txt
    
    :arg:
        none
    :return:
        1. dictionary
    """
    defs = {}
    with open('defaults.txt', mode='r') as default_values:
        for key, value in default_values.read().split(':'):
            defs[key] = value
    return defs


def print_defaults():
    """ Prints current defaults for password generation
    
    :arg:
        none
    :return:
        none
    """
    current_defs = load_defaults()
    print('Current defaults are: length: {0}, complexity: {1}, amount: {2}'.
          format(current_defs['length'], current_defs['complexity'], current_defs['amount']))


def change_defaults():
    """ Interactively asks for new default values for password generation and updates defaults.txt
    
    :arg:
        none
    :return:
        none
    """
    current_defs = load_defaults()
    print_defaults()
    print('Empty input = leave default value')
    new_length = input('Length: integer min 6 => ') or current_defs['length']
    new_complexity = input('Complexity: a - abcd, A - aBcD, n - a2b4, N - a2B4,'
                           ' s - a@b$, S - a@B4, f - a2b$, F - a2B$ => ') or current_defs['complexity']
    new_amount = input('Amount: integer number of passwords to generate starting with "x",'
                       ' i.e x10 => ') or current_defs['amount']
    with open('defaults.txt', mode='w') as default_values:
        default_values.write('length:{}'.format(new_length))
        default_values.write('complexity:{}'.format(new_complexity))
        default_values.write('amount:{}'.format(new_amount))
    return


def select_option(re_string, cmd_args, def_value):
    """ Return default or explicit option value depends on presence of cmd arguments
    
    :param re_string: regex string representing cmd argument for option
    :param cmd_args: args string 
    :param def_value: default value for option
    :return: option value
    """
    match_option = re.search(re_string, cmd_args)
    return match_option.group(0) if match_option else def_value


def generate(opt):
    """ Generate passwords with given options
    
    :param opt: dictionary of passwords options: length, complexity, amount
    :return: 
    """




    def generate_pass(tries):
        if tries > 1000:
            return 'Unable to generate password due to low amount of VCV chunks. \n' +\
                   'Please copy to source.txt more english texts and run "repassgen.py p"'
        next_tries = tries + 1
        err = gen()
        if err:
            generate_pass(next_tries)


    def iter_amount(generate_pass, amount, err):
        if err:
            print(err)
        elif amount > 0:
            generate_pass(0)
    iter_amount(opt['amount'])


def main():
    """ Generates readable passwords
    
    Usage: repassgen.py ( h | p | d | u | [1*] [2*] [3*])
    - h     -- print this help message
    - p     -- print defaults for password generation
    - d     -- set new defaults for passwords generation
    - u     -- update generator base (paste english text in source.txt prior to this action)
    - [1*]  -- integer (min 6) - use this length
    - [2*]  -- code of complexity:
                    a - abcd, A - aBcD, n - a2c4, N - a2C4, s - a@c$, S - a@C$, f - a2c$, F - a2C$
    - [3*]  -- x(integer) - amount of passwords to generate, i.e.: x10
    """
    args = sys.argv[1:]
    defs = load_defaults()
    if len(args) > 3:
        print('Wrong number of arguments!')
        print(main().__doc__)
    if len(args) == 1:
        if args[0] == 'h':
            print(main().__doc__)
        elif args[0] == 'd':
            change_defaults()
        elif args[0] == 'p':
            print_defaults()
    args_list = '' if len(args) == 0 else ' '.join(args)
    pass_length = select_option(r'\b\d+\b', args_list, defs['length'])
    pass_complexity = select_option(r'\b[ansfANSF]\b', args_list, defs['complexity'])
    pass_amount = select_option(r'\bx\d+\b', args_list, defs['amount'])
    options = {'length': pass_length, 'complexity': pass_complexity, 'amount': pass_amount}
    generate(options)
