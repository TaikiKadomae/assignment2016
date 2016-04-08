import sys
import re

argvs = sys.argv
argc = len(argvs)

if (argc != 3 ):
	print('Usage: # python %s filename' % argvs[0])
	quit()

for line in open(argvs[1]):
	if (re.compile(argvs[2]).search(line)):
		print(line,)
open(argvs[1]).close

		
