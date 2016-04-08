import sys
import re
argvs = sys.argv
argc = len(argvs)

if (argc != 2):
	print('Usage: # python %s filename' % argvs[0])
	quit()


for line in open(argvs[1], 'r'):
	line = line.strip('\n')
	sp = re.split(' +', line)
	for i in range(len(sp)):
		if (i == len(sp)):
			print(sp[i],end='')
		else:
			print(sp[i])
