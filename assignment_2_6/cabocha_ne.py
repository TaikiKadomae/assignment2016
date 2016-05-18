#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import CaboCha

parser = CaboCha.Parser('-n1')

sent = '豊工に行っています。'

tree = parser.parse(sent)
print(tree.toString(CaboCha.FORMAT_LATTICE))
for i in range(tree.token_size()):
	token = tree.token(i)
	print('Surface:' + str(token.surface))
	print('NE:' + str(token.ne))
