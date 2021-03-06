#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import shelve
from collections import OrderedDict
from nltk.tokenize import sent_tokenize, word_tokenize


argvs = sys.argv
argc = len(argvs)

#文分割
openedFile = open(argvs[1]).read()
sent_tokenize_list = sent_tokenize(openedFile)
print(sent_tokenize_list)

#単語分割
word_tokenize_list = []
for i in sent_tokenize_list:
	word_tokenize_list.extend(word_tokenize(i))

#辞書に追加
count = OrderedDict()
index = shelve.open('freq_to_index_shelve.db')
try:
	countOfIndex = 1
	for i in range(len(word_tokenize_list)):
		if word_tokenize_list[i] in count:
			count[word_tokenize_list[i]] += 1
		else:
			count[word_tokenize_list[i]] = 1
			index[word_tokenize_list[i]] = countOfIndex
			countOfIndex += 1
finally:
	index.close()


