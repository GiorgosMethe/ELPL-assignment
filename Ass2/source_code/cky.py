import sys
import random
import viterbi
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
adverb_node = "ADV"
name_node = "NNP"
noun_node = "N"
adjective_node = "ADJP"
treebank = ""

"""Holds information about each rule in every chart_item
position
"""

class chart_item():
    def __init__(self, child, prob, split, unary):
    	self.child = child
    	self.prob = prob
        self.split = split
        self.unary = unary

def update_progress(progress):
    print '\r[{0}%'.format(progress),

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
			if item == '' or item == '\n':
				break
			temp.append(item)
		sentences.append(temp)

def handle_unknown_words(unknown_word):
	""" UNKNOWN right side rule,
	we can decide a approximately and with a naive approach,
	to give words a non terminal rule.
	"""
	num = False
	for c in unknown_word:
		if c in ['0','1','2','3','4','5','6','7','8','9']:
			num = True
	if is_number(unknown_word) or num:
		return numeral_node
	elif len(unknown_word) > 4:
		p = False
		for c in unknown_word:
			if c == "-":
				p = True
		if (unknown_word[(len(unknown_word)-2):(len(unknown_word))] == "ly" or
		 unknown_word[(len(unknown_word)-1):(len(unknown_word))] == "y"):
			return adverb_node
		elif p or (unknown_word[(len(unknown_word)-4):(len(unknown_word))] == "able" or
		 unknown_word[(len(unknown_word)-2):(len(unknown_word))] == "ed"):
			return adjective_node
		elif (unknown_word[(len(unknown_word)-2):(len(unknown_word))] == "er" or
		unknown_word[(len(unknown_word)-3):(len(unknown_word))] == "ers" or 
		unknown_word[(len(unknown_word)-2):(len(unknown_word))] == "es" or 
		unknown_word[(len(unknown_word)-1):(len(unknown_word))] == "s" or
		unknown_word[(len(unknown_word)-3):(len(unknown_word))] == "ist" or
		unknown_word[(len(unknown_word)-4):(len(unknown_word))] == "ists" or
		unknown_word[(len(unknown_word)-3):(len(unknown_word))] == "ion" or
		unknown_word[(len(unknown_word)-3):(len(unknown_word))] == "ing"):
			return noun_node
		else:
			a = random.uniform(0, 1)
			if a < 0.8:
				return name_node
			else:
				return noun_node
	else:
		a = random.uniform(0, 1)
		if a < 0.8:
			return name_node
		else:
			return noun_node

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
		if item == '' or item == '\n':
			break
		temp.append(item)
	sentences.append(temp)

def iterate_sentences():
	"""iterates over all saved sentences and runs the cky parser
	for each one of them
    """
	i = 1
	for s in sentences:
		print "Sentence in line ", i, " has these top productions: "
		chart = cky_parsing(s)
		print_top_productions(chart,len(s)+1)
		i += 1

def iterate_sentences_viterbi(outfile):
	"""iterates over all saved sentences and runs the cky parser
	for each one of them
    """
	i = 1
	for s in sentences:
		print "Sentence in line ", i
		if len(s) <= 15:
			chart = cky_parsing_most(s)
		 	viterbi.run(chart,0,len(s),start_node,s,0)
		viterbi.build_tree(s,outfile)
		i += 1

def iterate_sentences_write(file_name):
	"""iterates over all saved sentences and runs the cky parser
	for each one of them
    """
	i = 1
	print "Writing output...",file_name
	for s in sentences:
		print "Sentence in line ", i
		chart = cky_parsing(s)
		write_top_productions(chart,len(s)+1,file_name,i)
		i += 1
	print "completed successfully"

def check_unaries_most(chart):
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
					if key1 in chart:
						if (value.prob * float(value1)) > chart[key1].prob:
							chart[key1] = chart_item(key, (value.prob * float(value1)), 0, True)
							added = True
					else:
						chart[key1] = chart_item(key, (value.prob * float(value1)), 0, True)
						added = True

def check_unaries_most_d(chart,word):
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
					if key1 in chart:
						if chart[key1].child != word:
							if (value.prob * float(value1)) > chart[key1].prob:
								chart[key1] = chart_item(key, (value.prob * float(value1)), 0, True)
								added = True
					else:
						chart[key1] = chart_item(key, (value.prob * float(value1)), 0, True)
						added = True

def cky_parsing_most(s):
	"""cky parser from stanford slides
	Output: the complete parse-forest
    """
	chart = {}
	for i in range(len(s)):
		chart[i,i+1] = defaultdict(set)
		if s[i] in rulesRL:
			for key, value in rulesRL[s[i]].iteritems():
				chart[i,i+1][key] = chart_item(s[i], float(value), 0, True)
		else:
			most_probable = handle_unknown_words(s[i])
			chart[i,i+1][most_probable] = chart_item(s[i], float(1.0), 0, True)
		check_unaries_most_d(chart[i,i+1],s[i])

	n = len(s)+1
	for span in range(2,n):
		for begin in range(n-span):
			end = begin + span
			chart[begin,end] = defaultdict(set)
			for split in range(begin+1,end):
				for x, valuex in chart[begin,split].iteritems():
					for y, valuey in chart[split,end].iteritems():
						if (x,y) in rulesRL:
							for key, value in rulesRL[(x,y)].iteritems():
								probability = float(value) * valuex.prob * valuey.prob
								if key in chart[begin,end]:
									if probability > chart[begin,end][key].prob:
										chart[begin,end][key] = chart_item((x,y), probability, split, False)
								else:
									chart[begin,end][key] = chart_item((x,y), probability, split, False)
				check_unaries_most(chart[begin,end])
	return chart

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
					if key1 == start_node:
						if type(chart[key1]) != type({}):
							chart[key1] = {}
							chart[key1][key] = chart_item(value, value, 0, True)
							added = True
						else:
							if not key in chart[key1]:
								chart[key1][key] = chart_item(value, value, 0, True)
								added = True

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
					chart[i,i+1][key][s[i]] = chart_item(value, value, 0, False)
				else:
					if not s[i] in chart[i,i+1][key]:
						chart[i,i+1][key][s[i]] = chart_item(value, value, 0, False)
		else:
			most_probable = handle_unknown_words(s[i])
			chart[i,i+1][most_probable] = {}
			chart[i,i+1][most_probable][s[i]] = chart_item(value, 1.0, 0, False)

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
									chart[begin,end][key][(x,y)] = chart_item(value, value, split, False)
								else:
									if not s[i] in chart[begin,end][key]:
										chart[begin,end][key][(x,y)] = chart_item(value,value, split, False)
				check_unaries(chart[begin,end])
	return chart


def print_top_productions(chart,n):
	"""prints the top production in the upper right 
	corner of the chart table
    """
	for key,value in chart[0,n-1].iteritems():
		if key == start_node:
			for key1,value1 in chart[0,n-1][key].iteritems():
				print key,"->",key1,"\n",

def write_top_productions(chart,n,file_name,line):
	f = open(file_name, 'a')
	f.write("Sentence in line "+str(line)+" has these top productions:\n")
	for key,value in chart[0,n-1].iteritems():
		if key == start_node:
			for key1,value1 in chart[0,n-1][key].iteritems():
				f.write(key+"->"+key1+"\n")
	f.close()