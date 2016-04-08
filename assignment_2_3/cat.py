import sys

argvs = sys.argv
argc = len(argvs)

if (argc != 2):
    print('Usage: # python %s filename' % argvs[0]) 
    quit()

print('The content of %s ...n' % argvs[1])
for line in open(argvs[1]):
    print(line.strip('\n'))
open(argvs[1]).close
