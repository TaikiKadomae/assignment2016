#######################################################
#
#   FileName:binarize.py
#   date:2016/4/29
#   author: Taiki Kadomae
#
#######################################################
import sys

for label in open(sys.argv[1]):
	if int(label, 10) >= 4:
		print("1")
	else:
		print("-1") 
