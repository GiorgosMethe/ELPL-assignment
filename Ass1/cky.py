import sys
from collections import defaultdict

""" Dictionary to hold the rules from the extracted pcfg
	Binary rules are held like:
	<<rulesRL[right_side][left_side] = prob>>
"""
rulesRL = defaultdict(set)
sentences = []

class chart_item():
    def __init__(self, prob, split, unary):
        self.prob = prob
        self.split = split
        self.unary = unary


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

def check_unaries(chart):
	added = True
	while added == True:
		added = False
		tempChart = chart.copy()
		for key, value in tempChart.iteritems():
			if key in rulesRL:
				for key1,value1 in rulesRL[key].iteritems():
					if type(chart[key1]) != type({}):
						chart[key1] = {}
						chart[key1][key] = chart_item(value, 0, True)
					else:
						if not key in chart[key1]:
							chart[key1][key] = chart_item(value, 0, True)
		tempChart = chart.copy()

def ChartInitialization(s):
	chart = {}
	for i in range(len(s)):
		chart[i,i+1] = defaultdict(set)
		if s[i] in rulesRL:
			for key, value in rulesRL[s[i]].iteritems():
				if type(chart[i,i+1][key]) != type({}):
					chart[i,i+1][key] = {}
					chart[i,i+1][key][s[i]] = chart_item(value, 0, False)
				else:
					if not s[i] in chart[i,i+1][key]:
						chart[i,i+1][key][s[i]] = chart_item(value, 0, False)
		check_unaries(chart[i,i+1])
		
	n = len(s)+1
	for span in range(2,n):
		for begin in range(n-span):
			end = begin + span
			chart[begin,end] = defaultdict(set)
			for split in range(begin+1,end):
				for x in chart[begin,split]:
					for y in chart[split,end]:
						if (x,y) in rulesRL:
							for key, value in rulesRL[(x,y)].iteritems():
								if type(chart[begin,end][key]) != type({}):
									chart[begin,end][key] = {}
									chart[begin,end][key][(x,y)] = chart_item(value, split, False)
								else:
									if not s[i] in chart[begin,end][key]:
										chart[begin,end][key][(x,y)] = chart_item(value, split, False)
			check_unaries(chart[begin,end])
	print_top_productions(chart,n)


def print_top_productions(chart,n):
	for i in range(n):
		for j in range(n):
			if (i,j) in chart:
				if i == 0 and j == 7:
					for key,value in chart[i,j].iteritems():
						if key == "TOP":
							for key1,value1 in chart[i,j][key].iteritems():
								print key,key1
	