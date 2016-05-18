#!usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys
import numpy as np
def read_instance(s):
	tupleList = []
	splitLine = s.strip().split(' ')
	for j in splitLine:
		if (j != splitLine[0]):
			tup = j.split(':')
			tupleList.append(tuple(tup))
	fvAndLabel = (splitLine[0], tupleList)
	return fvAndLabel

def read_data(s):
	line = open(s).readlines()
	dataList = []
	lenList = []
	for i in line:
		tup = read_instance(i)
		dataList.append(tup)
		lenList.append(len(tup[1]))
	return (dataList, max(lenList))

def add_fv(fv):
	zero = [0] * (len(weight) - len(fv))
	npfv = np.array(fv.extend(zero))
	npw = np.array(weight)
	return npw + npfv

def sub_fv(fv):
	zero = [0] * (len(weight) - len(fv))
	npfv = np.array(fv.extand(zero))
	npw = np.array(weight)
	return npw - npfv

def mult(fv):
	if not len(weight) < len(fv)
		zero = [0] *(len(weight) - len(fv)) 
		npfv = np.array(fv.extend(zero))
		npw = n.array(weight)
		return sum(npw * npfv)

def update_weight(data):
	for i in data:
		

if __name__ == "__main__":
	train_data, max_index = read_data(sys.argv[1])
	weight =[0] * (max_index + 1)
	
