def load():
	defs = {}
	with open('defaults.txt', mode='r') as default_values:
		for default_value in default_values:
			[key, value] = default_value.split(':')
			defs[key] = value
	return defs

def change():
	old_defs = load();
	print('Current defaults are: length: {0}, complexity: {1}, repetions: {2}'
		.format(defs['length'], defs['complexity'], defs['repetions']))
	print('Length: integer min 6')
	print('Complexity: a - abcd, A - aBcD, n - a2b4, N - a2B4, s - a@b$, S - a@B4, f - a2b$, F - a2B$')
	print('Repetions: integer number of passwords to generate starting with "x", i.e x10')
	new_params = ('Input new defaults in format [length complexity repetions], or type "q" to exit:\n')
	if new_params == 'q':
		return
	new_params_arr = new_params.split()
	new_length = int(new_params_arr[0])
	new_complexity = new_params_arr[1]
	new_repetions = int(new_params_arr[2].slice(1:))
	with open('defaults.txt', mode='w') as default_values:
		default_values.write('length:{}'.format(new_length))
		default_values.write('complexity:{}'.format(new_complexity))
		default_values.write('repetions:{}'.format(new_repetions))
	return

