import sys
from nltk.tokenize import sent_tokenize, word_tokenize


argvs = sys.argv
argc = len(argvs)

openedFile = open(argvs[1]).read()
sent_tokenize_list = sent_tokenize(openedFile)
print(sent_tokenize_list)


