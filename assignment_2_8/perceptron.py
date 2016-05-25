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

def read_data(train,test):
	line = open(train).readlines()
	line2 = open(test).readlines()
	dataList = []
	tdataList = []
	indexList = []
	for i in line:
		tup = read_instance(i)
		dataList.append(tup)

	for j in dataList:
		indexList.append(int(j[1][len(j[1])-1][0]))

	for k in line2:
		tup2 = read_instance(k)
		tdataList.append(tup2)
		
	max_index = max(indexList)
	return (dataList, tdataList, max_index)

def add_fv(fv, weight):
	for i in fv[1]:
		weight[int(i[0])] += int(i[1])
	return weight

def sub_fv(fv, weight):
	for i in fv[1]:
		weight[int(i[0])] -= int(i[1])
	return weight

def mult(fv, weight):
	sumdp = 0
	for i in fv[1]:
		if int(i[0]) < len(weight):
			sumdp += int(i[1]) * weight[int(i[0])]
		
	return sumdp

def update_weight(data, weight):
	w = weight
	for ins in data:
		if ins == data[0]:
			if int(ins[0]) > 0:
				w = add_fv(ins, w)
			else:
				w = sub_fv(ins, w)
		else:
			if int(ins[0]) * mult(ins, w) < 0:
				if int(ins[0]) > 0:
					w = add_fv(ins, w)
				elif int(ins[0]) < 0:
					w = sub_fv(ins, w)
				else:
					pass
			else:
				pass
				
	return w
def evaluate(test_data, w):
	count = 0
	inscount = 0
	for ins in test_data:
		inscount += 1
		if int(ins[0]) * mult(ins, w) > 0:
			count += 1
	return(count, inscount, count/inscount)
	
if __name__ == "__main__":
	train_data, test_data, max_index = read_data(sys.argv[1], sys.argv[2])

	weight = [0] * (max_index + 1)
	for i in range(int(sys.argv[3])):
		weight = update_weight(train_data, weight)
	correct, instance, rate = evaluate(test_data, weight)
	print(correct, instance, rate)
	
