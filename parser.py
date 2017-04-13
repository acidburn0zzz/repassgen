import re
import defaults

def parse(args):
	defs = defaults.load()
	if len(args) > 3:
		return {'error': 'Too many arguments', 'action': 'show_help', 'options': {}}
	if len(args) == 1: 
		if args[0] == 'h':
			return {'error': '', 'action': 'show_help', 'options': {}}
		if args[0] == 'd':
			return {'error': '', 'action': 'set_defaults', 'options': {}}
		if args[0] == 'p':
			return {'error': '', 'action': 'populate', 'options': {}}
	args_list = '' if len(args) == 0 else ' '.join(args)
	match_length = re.search(r'\b\d+\b', args_list)
	pass_length = match_length.group(0) if match_length else defs['length']
	match_complexity = re.search(r'\b[ansfANSF]\b', args_list)
	pass_complexity = match_complexity.group(0) if match_complexity else defs['complexity']
	match_repetions = re.search(r'\bx\d+\b', args_list)
	pass_repetions = match_repetions.group(0) if match_repetions else defs['repetions']
	return {'err': '', 'action': 'run', 'options': {
		'length': pass_length, 
		'complexity': pass_complexity, 
		'repetance': pass_repetions}}