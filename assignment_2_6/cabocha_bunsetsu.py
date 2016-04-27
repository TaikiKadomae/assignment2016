#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import CaboCha
import re
cabo = CaboCha.Parser("--charset=UTF-8")

sent = '豊工に行っています。'

s = re.split('-|\n', cabo.parse(sent).toString(CaboCha.FORMAT_TREE).strip())
for i in range(len(s)):
	if not re.match('[A-Z]+', s[i]):
		print(s[i].strip())
