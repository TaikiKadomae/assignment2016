#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import SennaTagger

argvs = sys.argv
argc = len(argvs)

#引数が不正の場合はメッセージを表示する
if (argc != 2):
	print('Usage: # python %s filename' % argvs[0])
	quit()
 
#タガー準備
tagger = SennaTagger('/usr/share/senna-v2.0')

#文分割
openedFile = open(argvs[1]).read()
sent_tokenize_list = sent_tokenize(openedFile)

#１行目の単語分割
word_tokenize_list = word_tokenize(sent_tokenize_list[0])

#タグ付け
for w, t in tagger.tag(word_tokenize_list):
	print(w, t)
