#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re
import difflib
from collections import OrderedDict

#コマンドライン引数使用
argvs = sys.argv
argc = len(argvs)

#引数が足りない場合はメッセージ表示
if (argc == 1):
	print('Usage: # python %s filename' % argvs[0])
	quit()

#辞書の中に単語があれば値を+1
#なければ辞書に追加
count = OrderedDict()
for line in open(argvs[1], 'r'):
	line = line.strip('\n')
	sp = re.split(' +', line)
	for i in range(len(sp)):
		if sp[i] in count:
			count[sp[i]] += 1
		else:
			count[sp[i]] = 1

#辞書から改行を削除
del count[""]

#辞書を値順にソートして表示
countOfLoop = 0
top10 = []
for k, v in sorted(count.items(), key = lambda x:x[1]):
	countOfLoop += 1
	if (countOfLoop > len(count) - 10):
		top10.append(str(v) + " " + k)
	print(v, k)
#比較する
if (argc == 3):
	diff = difflib.unified_diff(top10, open(argvs[2], 'r').read().strip().split('\n'))
	for j in diff:
		print(j)
