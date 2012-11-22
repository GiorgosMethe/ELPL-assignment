import sys
from collections import defaultdict

rulesRL = defaultdict(set)
rulesLR = defaultdict(set)
sentences = []

class chart_item():
    def __init__(self, node, child, prob, split):
        self.node = node
        self.child = child
        self.prob = prob
        self.split = split


def readPCFG():
	for line in open("output.txt", "r"):
		values = line.split(" ")
		if len(values) == 6:
			if type(rulesRL[(values[2],values[3])])!=type({}):
				rulesRL[(values[2],values[3])] = dict()
			rulesRL[(values[2],values[3])][values[1]] = values[4]
		else:
			if type(rulesRL[values[2]])!=type({}):
				rulesRL[values[2]] = dict()
			rulesRL[values[2]][values[1]] = values[3]

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
		print "Sentence in line ", i, " is: "
		ChartInitialization(s)
		i += 1

def node_exist(l,ref):
	for nodes in l:
		if nodes.node == ref.node and nodes.child == ref.child:
			return True
	return False

def check_unaries(chart):
	added = True
	while added == True:
		added = False
		for item in chart:
			if item.node in rulesRL:
				for key, value in rulesRL[item.node].iteritems():
					temp = chart_item(key, item.node, value, 0)
					if not node_exist(chart,temp):
						added = True
						chart.append(temp)


def ChartInitialization(s):
	chart = defaultdict(set)
	for i in range(len(s)):
		chart[i,i+1] = []
		if s[i] in rulesRL:
			for key, value in rulesRL[s[i]].iteritems():
				chart[i,i+1].append(chart_item(key, s[i], value, 0))
		check_unaries(chart[i,i+1])
		
	n = len(s)+1
	for span in range(2,n):
		for begin in range(n-span):
			end = begin + span
			chart[begin,end] = []
			for split in range(begin+1,end):
				A = chart[begin,split]
				B = chart[split,end]
				for x in A:
					for y in B:
						if (x.node,y.node) in rulesRL:
							for key, value in rulesRL[x.node,y.node].iteritems():
								temp = chart_item(key,(x.node,y.node), value, split)
								if not node_exist(chart[begin,end],temp):
				 					chart[begin,end].append(temp)
			check_unaries(chart[begin,end])
	printTable(chart,len(s)+1)

def printTable(table,n):

	for item in table[0,n-1]:
		if item.node == "TOP":
			print item.node, item.child
	
