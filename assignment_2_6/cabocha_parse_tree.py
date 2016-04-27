#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import CaboCha

cabo = CaboCha.Parser()

sent = '豊工に行っています。'

print(cabo.parseToString(sent))
