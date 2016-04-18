#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os 
import glob
import shelve
from collections import OrderedDict
from nltk.tokenize import sent_tokenize, word_tokenize


argvs = sys.argv

#ディレクトリからファイルを取り出す
fileList = []
for txtFile in glob.glob(argvs[1]+ '/*.txt'):
	if os.path.isfile(txtFile):
		 fileList.append(txtFile)
fileList.sort()

#各ファイルに対して特徴ベクトルの生成とインデックス付け
for txt in fileList:
	#文分割
	openedFile = open(txt).read()
	sent_tokenize_list = sent_tokenize(openedFile)

	#単語分割
	word_tokenize_list = []
	for j in sent_tokenize_list:
		word_tokenize_list.extend(word_tokenize(j))

	#辞書に追加
	count = OrderedDict()
	index = shelve.open('freq_to_index_shelve.db')

	try:
		countOfIndex = len(index)
		for k in range(len(word_tokenize_list)):
			if word_tokenize_list[k] in count:
				count[word_tokenize_list[k]] += 1
			else:
				count[word_tokenize_list[k]] = 1
				if not word_tokenize_list[k] in index:
					index[word_tokenize_list[k]] = countOfIndex + 1
					countOfIndex += 1
		#特徴ベクトルの生成
		fv = [0] * len(index)
		for key, value in count.items():
			fv[index[key] - 1] = value
		
	#何があっても.dbは閉じる
	finally:
		index.close()
	#ラベルとインデックスと出現回数を印字
	print(argvs[2], end=' ')
	for l in range(len(fv)):
		if(fv[l] != 0)
			print (str(l + 1) + ':' + str(fv[l]), end=' ')
	print('')	
