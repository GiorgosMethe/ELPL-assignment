import sys
from collections import defaultdict

rulesRL = defaultdict(set)
rulesLR = defaultdict(set)
sentences = []

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

def node_exist(l,ref_node):
	for nodes in l:
		if nodes == ref_node:
			return True
	return False

def ChartInitialization(s):
	chart = defaultdict(set)
	score = defaultdict(set)
	for i in range(len(s)):
		chart[i,i+1] = []
		if s[i] in rulesRL:
			for key, value in rulesRL[s[i]].iteritems():
				chart[i,i+1].append(key)
		for item in chart[i,i+1]:
			if item in rulesRL:
				for key, value in rulesRL[item].iteritems():
					if(not node_exist(chart[i,i+1],key)):
						chart[i,i+1].append(key)
	n = len(s)+1
	for span in range(2,n):
		for begin in range(n-span):
			end = begin + span
			chart[begin,end] = []
			for split in range(begin+1,end):
				A = chart[begin,split]
				B = chart[split,end]
				for x in A:
					if x in rulesRL:
							for key, value in rulesRL[x].iteritems():
								if(not node_exist(chart[begin,end],key)):
									chart[begin,end].append(key)
				for x in B:
					if x in rulesRL:
							for key, value in rulesRL[x].iteritems():
								if(not node_exist(chart[begin,end],key)):
									chart[begin,end].append(key)
				for x in A:
					for y in B:
						if (x,y) in rulesRL:
							for key, value in rulesRL[x,y].iteritems():
								if(not node_exist(chart[begin,end],key)):
									chart[begin,end].append(key)
	printTable(chart,len(s)+1)


def printTable(table,n):
	for i in range(n):
		print ""
		for j in range(n):
			for item in table[i,j]:
				print item,
			print "\t",
	
