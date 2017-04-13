import re
import sys
import populate
import parser
import defaults

args = sys.argv[1:]
settings = parser.parse(args)
if settings['err'] != '':
	print(settings['err'])
	print('run "repassgen.py h" for help')
elif settings['action'] == 'show_help':
	print('usage:')
	print('"repassgen.py"				run with default settings')
	print('"repassgen.py h"				show this message')
	print('"repassgen.py p" 			populate repassgen base from english text written in source.txt file')
	print('"repassgen.py d"  			set new defaults')
	print('"repassgen.py [1] [2] [3]"	run with manual parameters, where:')
	print('									[1] - password length: integer (min 6)')
	print('									[2] - complexity code letter from this list:')
	print('										  a - abcd, A - aBcD, n - a2c4, N - a2C4')
	print('										  s - a@c$, S - a@C$, f - a2c$, F - a2C$')
	print('									[3] - repetions: number of passwords to generate')
elif settings['action'] == 'set_defaults':
	defaults.change()
elif settings['action'] == 'populate':
	populate.update()
else:
	generator.gen(settings['options'])