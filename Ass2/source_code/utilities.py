from collections import defaultdict
from operator import itemgetter, attrgetter
import collections

""" Dictionary to hold the rules from the extracted pcfg
Binary rules are held like:
<<rulesRL[right_side][left_side] = prob>>
"""
rulesRL = defaultdict(set)
rulesLR = defaultdict(set)

class item:
	def __init__(self, rule, prob):
		self.rule = rule
		self.prob = prob

class ambiguous_item:
	def __init__(self, ruleL, ruleR, num, prob):
		self.ruleL = ruleL
		self.ruleR = ruleR
		self.num = num
		self.prob = prob

def read_pcfg(file_name):
	"""Reads the grammar rules from the output of the pcfg
	parser.
	Output: writes the rulesRL dictionary
	"""
	for line in open(file_name, "r"):
		values = line.split(" ")
		if len(values) == 6:
			if type(rulesRL[(values[2],values[3])])!=type({}):
				rulesRL[(values[2],values[3])] = dict()
			rulesRL[(values[2],values[3])][values[1]] = values[4]
			if type(rulesLR[values[1]])!=type({}):
				rulesLR[values[1]] = dict()
			rulesLR[values[1]][(values[2],values[3])] = values[4] 
		else:
			if type(rulesRL[values[2]])!=type({}):
				rulesRL[values[2]] = dict()
			rulesRL[values[2]][values[1]] = values[3]
			if type(rulesLR[values[1]])!=type({}):
				rulesLR[values[1]] = dict()
			rulesLR[values[1]][values[2]] = values[3]

def most_likely_production(noTerminal,num):
	most_likely = []
	if noTerminal in rulesLR:
		for key,value in rulesLR[noTerminal].iteritems():
			most_likely.append(item(key,float(value)))
			if len(most_likely) > num:
				most_likely = sorted(most_likely, key=attrgetter('prob'))
				most_likely.pop(0)
		for n in  sorted(most_likely, key=attrgetter('prob'), reverse=True):
			print n.rule, n.prob
	else:
		print "non-terminal not found in grammar"

def ambiguous():
	ambiguous_words = []
	for key,value in rulesRL.iteritems():
		if isinstance(key, basestring) and key not in rulesLR:
			counter = 0
			for key1,value1 in rulesRL[key].iteritems():
				counter +=1
			for key1,value1 in rulesRL[key].iteritems():
				ambiguous_words.append(ambiguous_item(key,key1,counter,value1))

	for n in  sorted(ambiguous_words, key=attrgetter('num'), reverse=True):
		if n.num > 4:
			print n.ruleL,"<-",n.ruleR,", probability:", "%0.6f" % float(n.prob)