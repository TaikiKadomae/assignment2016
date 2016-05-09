#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import shelve
import nltk
import gzip
import MeCab
from collections import OrderedDict

jp_sent_tokenizer = nltk.RegexpTokenizer('u[^！？。]*[！？。]?')
tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')

#文分割
openedFile =gzip.open(sys.argv[1]).readlines()
sent_tokenize_list = jp_sent_tokenizer.tokenize(opendFile)

#単語分割と辞書登録
count = OrderedDict()
index = shelve.open('jp_index.db')
countOfIndex = len(index) + 1
try:
	for i in sent_tokenize_list:
		node = tagger.parseToNode(i)
		while node:
			if node.surface in count:
				count[node.surface] += 1
			else:
				count[node.surface] = 1
				if not node.surface in index:
					index[node.surface] = countOfIndex
					countOfIndex += 1s
		node.next
	fv = [0] * len(index)
	for key, value in count.items():
		fv[index[key] - 1] = value

finally:
	index.close()
try:
	countOfIndex = len(index) + 1
	for i in range(len(word_tokenize_list)):
		if word_tokenize_list[i] in count:
			count[word_tokenize_list[i]] += 1
		else:
	
for j in range(len(feature_vector)):
	if feature_vector[j] != 0:
		print (str(j + 1) + ':' + str(feature_vector[j]), end=' ')
print('')
