import sys

argvs = sys.argv #コマンドライン引数のリスト
argc = len(argvs) 

# 引数が足りない場合はメッセージを出す
if (argc != 3):
	print('Usage: # python %s filename' % argvs[0])
	quit()

f = open(argvs[2], 'w')
for line in open(argvs[1]):
	f.write(line.strip('\n'))
open(argvs[1]).close
f.close

