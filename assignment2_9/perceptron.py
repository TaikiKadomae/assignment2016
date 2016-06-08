#!usr/bin/env python3
#-*- coding:UTF-8 -*-

import sys,random,time,math
from optparse import OptionParser

desc = u'{0}[Args] [Options]\nDetail options -h or --help'.format(__file__)
parser = OptionParser(description = desc)
parser.add_option(
	'-s',
	type = 'int',
	default = '10',
	dest = 'updates',
	help = '更新回数'
	)
parser.add_option(
	'-b',
	type = 'int',
	default = '1',
	dest = 'bias',
	help = 'バイアス項')
parser.add_option(
	'-n',
	action = 'store_true',
	dest = 'norm',
	default = False,
	help = '正規化')
parser.add_option(
	'-m',
	dest = 'margin',
	default = '0.1',
	help = 'マージン')
parser.add_option(
	'-a',
	action = 'store_true',
	default = False,
	dest = 'is_ave',
	help = '平均化パーセプトロン')

args = parser.parse_args()

def read_instance(s,bias,is_norm):
	tupleList = [(0,float(bias))]
	splitLine = s.strip().split(' ')
	sumfv = 0.
	if(is_norm):
		for j in splitLine:
			tup = j.split(':')
			tupleList.append((int(tup[0]),float(tup[1])))
	else:
		for j in splitLine:
			if (j != splitLine[0]):
				tup = j.split(':')
				sumfv += float(tup[1])*float(tup[1])
		ave = math.sqrt(sumfv)
		for k in splitLine:
			if (k != splitLine[0]):
				tup = k.split(':')
				tupleList.append((int(tup[0]),float(tup[1])/math.sqrt(sumfv)))
	fvAndLabel = (int(splitLine[0]), tupleList)
	return fvAndLabel

def read_data(train,test,bias,is_norm):
	dataList = []
	t_dataList = []
	indexList = []

	dataList = [read_instance(i,bias,is_norm) for i in open(train)]
	indexList = [tmp[1][len(tmp[1])-1][0] for tmp in dataList]
	t_dataList = [read_instance(k,bias,is_norm) for k in open(test)]
		
	max_index = max(indexList)
	return (dataList, t_dataList, max_index)

def add_fv(ins,nup):
	for i in ins[1]:
		weight[i[0]] += i[1]
		tmp_weight[i[0]] += i[1]*nup
def sub_fv(ins,nup):
	for i in ins[1]:
		weight[i[0]] -= i[1]
		tmp_weight[i[0]] -= i[1]*nup
def mult(ins):
	sumdp = 0
	len_w = len(weight)
	for i in ins[1]:
		if (i[0] < len_w):
			sumdp += i[1] * weight[i[0]]
	return sumdp

def e_mult(ins,w):
        sumdp = 0
        len_w = len(w)
        for i in ins[1]:
                if (i[0] < len_w):
                        sumdp += i[1] * w[i[0]]
        return sumdp

def update_weight(data,nupdates,m):
	random.seed(0)
	random.shuffle(data)
	for ins in data:
		tmp = ins[0]
		mul = mult(ins)
		if (ins == data[0]):
			nupdates += 1
			if (tmp > 0):
				add_fv(ins,nupdates)
			elif (tmp < 0):
				sub_fv(ins,nupdates)
		else:
			if (tmp * mul <= 0 or mul * mul <= m):
				nupdates += 1
				if (tmp > 0):
					add_fv(ins,nupdates)
				elif (tmp < 0):
					sub_fv(ins,nupdates)
	return nupdates	
def evaluate(test_data,w):
	count = 0
	i_count = 0
	for ins in test_data:
		i_count += 1
		if (ins[0] * e_mult(ins,w) > 0):
			count += 1
	return(count, i_count, count/i_count)

def averaged_weight(nup):
	len_we = len(weight)
	a_weight =[0] * len_we
	for i in range(len_we):
		a_weight[i] = weight[i] - (tmp_weight[i]/(nup+1))

	return a_weight

def arg_option():
	desc = u'{0}[Args] [Options]\nDetail options -h or --help'.format(__file__)
	parser = OptionParser(description = desc)
	parser.add_option(
		'-s',
		type = 'int',
		default = '10',
		dest = 'updates',
		help = '更新回数'
		)
	parser.add_option(
		'-b',
		type = 'int',
		default = '1',
		dest = 'bias',
		help = 'バイアス項')
	parser.add_option(
		'-n',
		action = 'store_true',
		dest = 'norm',
		default = False,
		help = '正規化')
	parser.add_option(
		'-m',
		dest = 'margin',
		default = '0.1',
		help = 'マージン')
	parser.add_option(
		'-a',
		action = 'store_true',
		default = False,
		dest = 'is_ave',
		help = '平均化パーセプトロン')
	
	args = parser.parse_args()

	return args.updates, args.bias, args.norm, args.margin, args.is_ave

if __name__ == "__main__":
	sttime = time.time()
	updates, bias, is_norm, margin, is_ave = arg_option()
	train_data, test_data, max_index = read_data(sys.argv[1], sys.argv[2], bias, is_norm)
	weight = [0] * (max_index + 1)
	tmp_weight = [0] * len(weight)
	nupdates = 0
	for i in range(updates):
		nupdates = update_weight(train_data, nupdates, margin)
	ave_weight = averaged_weight(nupdates)
	
	if(is_ave):
		correct, instance, rate = evaluate(test_data,ave_weight)
	else:
		correct, instance, rate = evaluate(test_data,weight)
	print('イテレーション数:' + sys.argv[3])
	print('正解数       　 :' + str(correct))
	print('インスタンス数　:' + str(instance))
	print('正解率       　 :' + str(rate*100) + '%')
	print("処理時間     　 :" + str(time.time() - sttime) + '秒')
