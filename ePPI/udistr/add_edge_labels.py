#!/usr/bin/python3

import sys
import random

ifile = sys.argv[1]
ofile = sys.argv[2]
nof_elabels = int(sys.argv[3])


random.seed(nof_elabels)

state = 0
nofe = 0
ce = 0

off = open(ofile,'w')

for line in open(ifile,'r'):
	if state == 0:
		state = 1
		off.write(line)
	elif state == 1:
		state = 2
		nofe = int(line)
		ce = 0
		off.write(line)
	elif state == 2:
		if ce == nofe:
			off.write(line)
			state = 3
		else:
			off.write(line)
			ce += 1
	else:
		off.write(line.strip()+" "+str(random.randint(0,nof_elabels-1))+"\n")

off.flush()
off.close()
