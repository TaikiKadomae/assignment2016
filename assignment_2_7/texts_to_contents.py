#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import nltk 
import gzip
import shelve
import MeCab
from collections import OrderedDict

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
			if node.feature.split(',')[0] in {u'名詞', u'動詞', u'形容詞', u'形容動詞', u'副詞'}:
				wordList.append(node.surface)
			node = node.next
	
	#辞書に追加
	count = OrderedDict()
	index = shelve.open('jp_index.db')
	countOfIndex = len(index) + 1
	try:
		countOfIndex = len(index) + 1
		for k in range(len(wordList)):
			if wordList[k] in count:
				count[wordList[k]] += 1
			else:
				count[wordList[k]] = 1
				if not wordList[k] in index:
					index[wordList[k]] = countOfIndex
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
