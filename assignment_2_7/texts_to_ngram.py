#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import nltk 
import gzip
import shelve
import MeCab
from collections import OrderedDict
n = sys.argv[2]
jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^！？。]*[！？。]?')
tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')

line = gzip.open(sys.argv[1], 'rt').readlines()

#各行に対して特徴ベクトルの生成とインデックス付け
for txt in line:
	
	#文分割
	sentList = []
	sentList.extend(jp_sent_tokenizer.tokenize(txt.strip()))
	
	#単語分割
	wordList = []
	for j in sentList:
		
		node = tagger.parseToNode(j.strip())
		
		while node:
			wordList.append(node.surface)
			node = node.next

		while '' in wordList:
			wordList.remove('')

		phraseList = []
		for i in range(len(wordList)):
			if (n == '2') and (i != len(wordList) - 1):
				phraseList.append(str(wordList[i]) + str(wordList[i + 1]))
			elif (n == '3') and (i != len(wordList) - 2) and (i != len(wordList) - 1):
				phraseList.append(str(wordList[i]) + str(wordList[i + 1]) + str(wordList[i + 2]))
			else:					
				phraseList.append(str(wordList[i]))
		
	#辞書に追加
	count = OrderedDict()
	if (n == '1'):
		index = shelve.open('jp_index.db')
	elif (n == '2'):
		index = shelve.open('jp_index_bigram.db')
	elif (n =='3'):
		index = shelve.open('jp_index_trigram.db')
	countOfIndex = len(index) + 1
	try:
		countOfIndex = len(index) + 1
		for k in range(len(phraseList)):
			if phraseList[k] in count:
				count[phraseList[k]] += 1
			else:
				count[phraseList[k]] = 1
				if not phraseList[k] in index:
					index[phraseList[k]] = countOfIndex
					countOfIndex += 1
		#特徴ベクトルの生成
		fv = [0] * (len(index) + 1)
		for key, value in count.items():
			fv[index[key]] = value
		
	#何があっても.dbは閉じる
	finally:
		index.close()

	for l in range(len(fv)):
		
		if fv[l] != 0:
			print (str(l) + ':' + str(fv[l]), end=' ')
	print('')
