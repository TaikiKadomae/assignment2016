#!usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys

def read_instance(s):
	tupleList = []
	splitLine = s.strip().split(' ')
	for j in splitLine:
		if (j != splitLine[0]):
			tup = j.split(':')
			tupleList.append((int(tup[0]),int(tup[1])))
	fvAndLabel = (int(splitLine[0]), tupleList)
	return fvAndLabel

def read_data(train,test):
	dataList = []
	t_dataList = []
	indexList = []
	for i in open(train).readlines():
		tup = read_instance(i)
		dataList.append(tup)

	for j in dataList:
		indexList.append(j[1][len(j[1])-1][0])

	for k in open(test).readlines():
		t_tup = read_instance(k)
		t_dataList.append(t_tup)
		
	max_index = max(indexList)
	return (dataList, t_dataList, max_index)

def add_fv(ins):
	for i in ins[1]:
		weight[i[0]] += i[1]

def sub_fv(ins):
	for i in ins[1]:
		weight[i[0]] -= i[1]

def mult(ins):
	sumdp = 0
	for i in ins[1]:
		if (i[0] < len(weight)):
			sumdp += (i[1] * weight[i[0]])
	return sumdp

def update_weight(data):
	for ins in data:
		if (ins == data[0]):
			if (ins[0] == 1):
				add_fv(ins)
			elif (ins[0] == -1):
				sub_fv(ins)
		else:
			if (ins[0] * mult(ins) <= 0):
				if (ins[0] == 1):
					add_fv(ins)
				elif (ins[0] == -1):
					sub_fv(ins)
				
def evaluate(test_data):
	count = 0
	i_count = 0
	for ins in test_data:
		i_count += 1
		if (ins[0] * mult(ins) > 0):
			count += 1
	return(count, i_count, count/i_count)
	
if __name__ == "__main__":
	train_data, test_data, max_index = read_data(sys.argv[1], sys.argv[2])
	weight = [0] * (max_index + 1)
	for i in range(int(sys.argv[3])):
		update_weight(train_data)
	correct, instance, rate = evaluate(test_data)
	print('正解数         ' + str(correct))
	print('インスタンス数 ' + str(instance))
	print('正解率         ' + str(rate*100) + '%')
