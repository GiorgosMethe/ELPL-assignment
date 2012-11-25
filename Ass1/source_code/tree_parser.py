# parser module
import sys
from pprint import pprint
temp_array = []

rule_dict = dict()
rule_count = dict()
rules = []

class parsed_rules(object):
    def __init__(self, rule, lvl):
		self.rule = rule
		self.lvl = lvl

class Rule(object):
    def __init__(self, leftSide, rightSide):
		self.leftSide = leftSide
		self.rightSide = rightSide

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress),

def create_rules():
	for i in range(len(temp_array)-1):
		rightSide = ""
		for j in range(i+1,len(temp_array)):
			if(temp_array[j].lvl-1 == temp_array[i].lvl):
				if(rightSide == ""):
					rightSide += temp_array[j].rule
				else:
					rightSide += " " + temp_array[j].rule
			if(j == len(temp_array)-1 or temp_array[j].lvl == temp_array[i].lvl):
				if rightSide != "" :
					save_rule(Rule(temp_array[i].rule,rightSide))
				break

def save_rule(newRule):
	if newRule.leftSide in rule_count:
		rule_count[newRule.leftSide] += 1
	else:
		rule_count[newRule.leftSide] = 1
		rules.append(newRule.leftSide)

	if newRule.leftSide in rule_dict:
			if newRule.rightSide in rule_dict[newRule.leftSide]:
				rule_dict[newRule.leftSide][newRule.rightSide] += 1
			else:
				rule_dict[newRule.leftSide][newRule.rightSide] = 1
	else:
		rule_dict[newRule.leftSide] = dict()
		rule_dict[newRule.leftSide][newRule.rightSide] = 1

def fix_probs():
	for rule in rules:
		for key, value in rule_dict[rule].iteritems():
			f = float(value)/rule_count[rule]
			rule_dict[rule][key] = f

def write_file(file_name):
	print "Printing output...(",file_name,")",
	f = open(file_name, 'w')
	i = 0
	for rule in rules:
		for key, value in rule_dict[rule].iteritems():
			f.write('{num:{fill}{width}} '.format(num=i, fill='0', width=5))
			f.write(rule)
			f.write(' ')
			f.write(key)
			f.write(' ')
			f.write(str(value))
			f.write(' \n')
			i += 1
	f.close()
	print "completed successfully"

def parse_document(inputText,start,lvl):
	openP = 0
	closeP = 0
	a = ""
	pc = -1
	print "Parsing document progress:"
	for i in range(start, len(inputText)):
		progress = float(i+1)/len(inputText) * 100
		update_progress(int(progress))
		if (inputText[i] == "\n" ):
			create_rules()
			del temp_array[:]
			i += 1
			lvl = -1
		elif (inputText[i] == ")"):
			if(a != "" and a != " "):
				fix_rules(a,lvl)
				a = ""
			closeP += 1
			if (openP != closeP):
				lvl -= 1
		elif (inputText[i] == "("):
			if(a != "" and a != " "):				
				fix_rules(a,lvl)
				a = ""
			openP += 1
			lvl += 1
		else:
			a += inputText[i]
	print "Parsing document completed successfully"
	
def fix_rules(inputString,level):
	fixed = ""
	lvlOff = 0
	for i in range(len(inputString)):
		if(inputString[i] == " "):
			if(fixed != ""):
				temp_array.append(parsed_rules(fixed, level + lvlOff))
				lvlOff += 1
			fixed = ""
		else:
			fixed += inputString[i]
			if(i == len(inputString)-1):
				temp_array.append(parsed_rules(fixed, level + lvlOff))
				lvlOff += 1
				fixed = ""