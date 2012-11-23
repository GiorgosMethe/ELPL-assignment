import sys
from collections import defaultdict

""" Dictionary to hold the rules from the extracted pcfg
Binary rules are held like:
<<rulesRL[right_side][left_side] = prob>>
"""
rulesRL = defaultdict(set)
sentences = []
start_node = "TOP"
unknown_node = "@UNKNOWN"
numeral_node = "CD"

"""Holds information about each rule in every chart_item
position
"""
class chart_item():
    def __init__(self, prob, split, unary):
    	self.prob = prob
        self.split = split
        self.unary = unary

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
		else:
			if type(rulesRL[values[2]])!=type({}):
				rulesRL[values[2]] = dict()
			rulesRL[values[2]][values[1]] = values[3]

def read_sentences(file_name):
	"""Reads all sentences from the given txt file.
	Output: writes sentences list
    """
	for line in open(file_name, "r"):
		items = line.split(" ")
		temp = []
		for item in items:
			if item == '':
				break
			temp.append(item)
		sentences.append(temp)

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def read_sentences_input(sentence):
	"""Reads sentence from terminal
    """
	items = sentence.split(" ")
	temp = []
	for item in items:
		if item == '':
			break
		temp.append(item)
	sentences.append(temp)

def iterate_sentences():
	"""iterates over all saved sentences and runs the cky parser
	for each one of them
    """
	i = 0
	for s in sentences:
		print "Sentence in line ", i, " is: "
		cky_parsing(s)
		i += 1

def check_unaries(chart):
	"""iterates over all nodes inot the specified chart position
	and looks for unaries
	Output: adds the unary rules to the specified chart position
    """
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

def cky_parsing(s):
	"""cky parser from stanford slides
	Output: the complete parse-forest
    """
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
		else:
			""" UNKNOWN right side rule,
			we can decide a approximately and with a naive approach,
			to give words a non terminal rule.
			"""
			num = False
			for c in s[i]:
				if c in ['0','1','2','3','4','5','6','7','8','9']:
					num = True
			if is_number(s[i]) or num:
				chart[i,i+1][numeral_node] = {}
				chart[i,i+1][numeral_node][s[i]] = chart_item(1.0, 0, False)
			elif len(s[i]) > 4:
				p = False
				for c in s[i]:
					if c == "-":
						p = True
				if (s[i][(len(s[i])-2):(len(s[i]))] == "ly" or
				 s[i][(len(s[i])-1):(len(s[i]))] == "y"):
					pass
					#ADV
				elif p or (s[i][(len(s[i])-4):(len(s[i]))] == "able" or
				 s[i][(len(s[i])-2):(len(s[i]))] == "ed"):
					pass
					#ADJ
				elif (s[i][(len(s[i])-2):(len(s[i]))] == "er" or
				s[i][(len(s[i])-3):(len(s[i]))] == "ers" or 
				s[i][(len(s[i])-2):(len(s[i]))] == "es" or 
				s[i][(len(s[i])-1):(len(s[i]))] == "s" or
				s[i][(len(s[i])-3):(len(s[i]))] == "ist" or
				s[i][(len(s[i])-4):(len(s[i]))] == "ists" or
				s[i][(len(s[i])-3):(len(s[i]))] == "ion" or
				s[i][(len(s[i])-3):(len(s[i]))] == "ing"):
					pass
					#N
				else:
					pass
					#name, uknown
			else:
				pass
				#name, uknown

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
	"""prints the top production in the upper right 
	corner of the chart table
    """
	for key,value in chart[0,n-2].iteritems():
		if key == start_node:
			for key1,value1 in chart[0,n-2][key].iteritems():
				print key,key1
	