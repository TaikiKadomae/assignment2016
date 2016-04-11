#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import SennaChunkTagger

argvs = sys.argv
argc = len(argvs)

#引数が不適切の場合はメッセージを表示する
if (argc != 2):
        print('Usage: # python %s filename' % argvs[0])
        quit()
#タガー準備
tagger = SennaChunkTagger('/usr/share/senna-v2.0')

#文分割
openedFile = open(argvs[1]).read()
sent_tokenize_list = sent_tokenize(openedFile)
print(sent_tokenize_list[0])

#１行目の単語分割
word_tokenize_list = word_tokenize(sent_tokenize_list[0])

#タグ付け

tag_list = []
tagged_sent = tagger.tag(word_tokenize_list)

for i in range(len(tagged_sent)):
	tag_list.append(tagged_sent[i][1].split('-'))

for j in range(len(tag_list)):
	if(tag_list[j][0] == 'O'):
		if(tag_list[j - 1][0] != 'O'):
			print(tag_list[j - 1][1])
		else:
			pass	
	elif(j == 0 or tag_list[j - 1][0] == 'O'):
		print(tagged_sent[j][0], end=' ')	
	
	elif(j != 0):
		if(tag_list[j][1] == tag_list[j - 1][1]):
			print(tagged_sent[j][0], end=' ')
		else:
			print(tag_list[j - 1][1] + '\n' + tagged_sent[j][0], end=' ')
