import os
import numpy as np

step = -0.01
start = 0.14
end = 0.06
mspace = np.arange(start, end, step)

def change_in_file(newlines, filename='inlist_brown_dwarf', lines_to_change=58):
    if not isinstance(lines_to_change, tuple):
        lines_to_change = lines_to_change,
    if not isinstance(newlines, tuple):
        newlines = newlines,
    with open(filename, 'r') as fl:
        lines = fl.readlines()
    for i, line in enumerate(lines_to_change):
        lines[line] = newlines[i]
    with open(filename, 'w') as fl:
        print(''.join(lines), file=fl, end='')

termination_code = ''
for m in mspace:
	if termination_code != 'Lnuc_div_L_zams_limit':
		mstr = str(np.round(m, 2)).replace('.', '')
		os.system('./rn1 > log.out')
		fn_log = open('log.out')
		lines = fn_log.readlines()
		for line in lines[::-1]:
			if line.startswith('termination code'):
				termination_code = line.split(': ')[1].strip()
		fn_log.close()
		os.system('rm log.out')
		os.system(f'rm -rf LOGS_{mstr}')
		os.system(f'mkdir LOGS_{mstr}')
		os.system(f'mv LOGS/* LOGS_{mstr}')
		change_in_file(newlines=f'      initial_mass = {m}\n')
	else:
		break
# print(termination_code)
