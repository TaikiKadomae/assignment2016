#!/usr/bin/env python 
#-*- coding: UTF-8 -*-

import sys
import MeCab

nm = MeCab.Tagger()
print(nm.parse(open(sys.argv[1]).read()))
