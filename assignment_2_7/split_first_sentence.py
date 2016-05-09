#######################################################
#
#   FileName:split_first_sentence.py
#   date:2016/4/30
#   author: Taiki Kadomae
#
#######################################################
import sys
import nltk
import gzip

jp_sent_tokenizer = nltk.RegexpTokenizer(u'[^！？。]*[！？。]?')
line = gzip.open(sys.argv[1],'rt').readline().strip()
sent = []
sent.extend(jp_sent_tokenizer.tokenize(line))
print(sent[0])
