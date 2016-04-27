#!/usr/bin/env python 
#-*- coding: UTF-8 -*-

import sys
import MeCab
#タグ準備
tagger = MeCab.Tagger('-Ochasen')
tagger.parse('') #これをしておかないとpython3では動かない

node = tagger.parseToNode(open(sys.argv[1]).read())

while node:
	feature = node.feature.split(',')
	#feature:[品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用形,活用型,原形,読み,発音]
	
	print(node.surface, feature[0], feature[6])
	node = node.next

