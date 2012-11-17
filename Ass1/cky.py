import sys
from collections import defaultdict

rulesRL = defaultdict(set)
rulesLR = defaultdict(set)
sentences = []

class item():
    def __init__(self, node, prob):
        self.node = node
        self.prob = prob

def initialize_threedlist(value):
    list=[]
    for row in range(value):
        list.append([]*value)
        for col in range(value):
        	list[row].append([])
    return list

def readPCFG():
	for line in open("output.txt", "r"):
		values = line.split(" ")
		if len(values) == 5:
			rulesRL[(values[2],values[3])] = dict()
			rulesRL[(values[2],values[3])][values[1]] = values[4]
			rulesLR[values[1]] = dict()
			rulesLR[values[1]][(values[2],values[3])] = values[4]
		else:
			rulesRL[values[2]] = dict()
			rulesRL[values[2]][values[1]] = values[3]
			rulesLR[values[1]] = dict()
			rulesLR[values[1]][values[2]] = values[3]

def readSentences():
	for line in open("testSentences.txt", "r"):
		items = line.split(" ")
		temp = []
		for item in items:
			if item == '':
				break
			temp.append(item)
		sentences.append(temp)

def itarateSentences():
	i = 0
	for s in sentences:
		print "Sentence in line ", i, " is: ",
		ChartInitialization(s)
		i += 1

def ChartInitialization(s):
	CKYtable = initialize_threedlist(len(s)+1)
	for i in range(len(s)):
		for key, value in rulesRL[s[i]].iteritems():
			CKYtable[i][i+1].append(item(key,value))
	n = len(s)+1
	for span in range(2,n):
		for begin in range(n-span):
			end = begin + span
			for split in range(begin+1,end):
				A = CKYtable[begin][split]
				B = CKYtable[split][end]
				for x in A:
					for y in B:
						if (x.node,y.node) in rulesRL:
							for key, value in rulesRL[(x.node,y.node)].iteritems():	
								CKYtable[begin][end].append(item(key,value))
	printCKYtable(CKYtable)

def printCKYtable(CKYtable):
	pass
	for a in CKYtable:
		print a

