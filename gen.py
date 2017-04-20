import random


def fn_mods(style):
    if style == 'caps':
        return lambda letter: letter.upper()
    elif style == 'nums':
        return lambda letter: str(random.choice([2, 3, 4, 6, 7, 8, 9]))
    elif style == 'syms':
        return lambda letter: random.choice(['!', '@', '#', '$', '%', '&', '?'])
    else:
        return lambda letter: ''


def refine(sequence):
    better_letters = {'l': 'nm', 'S': 'HF', 'I': 'AEU', 'O': 'AEU'}
    refined_sequence = [random.choice(list(better_letters[letter])) for
                        letter in sequence if letter in better_letters.keys()]
    return {'err': '', 'dat': refined_sequence}


def complexify(sequence, code):
    distortion_power = 0.1
    min_distortions = 1
    distortions = max(int(len(sequence)*distortion_power), min_distortions)
    fun_sequence = []
    if code in 'ASNF':
        fun_sequence.append(fn_mods('caps'))
    if code in 'nNfF':
        fun_sequence.append(fn_mods('nums'))
    if code in 'sSfF':
        fun_sequence.append(fn_mods('syms'))
    mod_sequence = modify(sequence, fun_sequence, distortions)
    if mod_sequence['err']:
        return mod_sequence
    return refine(mod_sequence)


def modify(sequence, fun_sequence, distortions):
    splitted_sequence = [('um', value) for value in sequence]

    def mod_iter(cur_sequence, head_funs, tail_funs, runs_left):
        if not head_funs:
            return {'err': '', 'dat': [value for state, value in cur_sequence]}
        if runs_left == 0:
            next_head_funs = tail_funs[0] if len(tail_funs) > 0 else []
            next_tail_funs = tail_funs[1:] if len(tail_funs) > 1 else []
            return mod_iter(cur_sequence, next_head_funs, next_tail_funs, runs_left)
        unmod_sym_indexes = [index for index, value in enumerate(cur_sequence) if value[0] == 'um']
        unmod_index = random.choice(unmod_sym_indexes)
        unmod_symbol = cur_sequence[unmod_index][1]
        mod_sequence = cur_sequence[:]
        mod_sequence[unmod_index] = ('mo', head_funs(unmod_symbol))
        return mod_iter(mod_sequence, head_funs, tail_funs, runs_left - 1)
    if len(fun_sequence) > 0:
        next_tail = fun_sequence[1:]
        return mod_iter(splitted_sequence, fun_sequence[0], next_tail, distortions)
    return {'err': '', 'dat': sequence}


def build_sequence(data):
    head = random.choice(list(data.keys()))
    content = random.choice(list(data[head]))
    starting_head = head if head[0] != '_' else head[1:]
    body, tail = content
    return starting_head + body + tail


def generate(structure, options):
    length = options['length']
    if (length < 6) or (not isinstance(length,  int)):
        return {'err': 'Password length must be an integer number of 6 or more', 'dat': ''}
    complexity = options['complexity']
    if complexity not in 'aAnNsSfF':
        return {'err': 'Password comlexity code must be one of: a A n N s S f F', 'dat': ''}
    amount = options['amount']
    if (amount < 1) or (not isinstance(amount, int)):
        return {'err': 'Passwords amount must be an integer number of 1 or more', 'dat': ''}
    tries = 100

    def gen_iter(sequence, tail, tries_left):
        if tries_left == 0:
            return {'err': 'Unable to generate password. The base is too small.', 'dat': ''}
        current_sequence = sequence or build_sequence(structure)
        if tail not in structure.keys():
            return gen_iter('', '', tries_left - 1)
        next_body, next_tail = random.choice(list(structure[tail]))
        next_sequence = current_sequence + next_body + next_tail
        if len(next_sequence) >= length:
            return {'err': '', 'dat': next_sequence[:length]}
        return gen_iter(next_sequence, next_tail, tries_left)
    gen_result = gen_iter('', '', tries)
    if gen_result['err']:
        return gen_result
    mod_result = complexify(gen_result['dat'], complexity)
    return mod_result
