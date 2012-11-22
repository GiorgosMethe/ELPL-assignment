# parser module
import sys
from pprint import pprint
tempArray = []

ruleDict = dict()
ruleCount = dict()
rules = []

class ParsedRules(object):
    def __init__(self, rule, lvl):
		self.rule = rule
		self.lvl = lvl

class Rule(object):
    def __init__(self, leftSide, rightSide):
		self.leftSide = leftSide
		self.rightSide = rightSide

def update_progress(progress):
    print '\r[{0}] {1}%'.format('#'*(progress/10), progress),

def createRules():
	for i in range(len(tempArray)-1):
		rightSide = ""
		for j in range(i+1,len(tempArray)):
			if(tempArray[j].lvl-1 == tempArray[i].lvl):
				if(rightSide == ""):
					rightSide += tempArray[j].rule
				else:
					rightSide += " " + tempArray[j].rule
			if(j == len(tempArray)-1 or tempArray[j].lvl == tempArray[i].lvl):
				if rightSide != "" :
					saveRule(Rule(tempArray[i].rule,rightSide))
				break

def saveRule(newRule):

	if newRule.leftSide in ruleCount:
		ruleCount[newRule.leftSide] += 1
	else:
		ruleCount[newRule.leftSide] = 1
		rules.append(newRule.leftSide)

	if newRule.leftSide in ruleDict:
			if newRule.rightSide in ruleDict[newRule.leftSide]:
				ruleDict[newRule.leftSide][newRule.rightSide] += 1
			else:
				ruleDict[newRule.leftSide][newRule.rightSide] = 1
	else:
		ruleDict[newRule.leftSide] = dict()
		ruleDict[newRule.leftSide][newRule.rightSide] = 1

def fixProbs():
	for rule in rules:
		for key, value in ruleDict[rule].iteritems():
			f = float(value)/ruleCount[rule]
			ruleDict[rule][key] = f

def writeFile():
	print "Printing output...(output.txt)",
	f = open('output.txt', 'w')
	i = 0
	for rule in rules:
		for key, value in ruleDict[rule].iteritems():
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


def printRules():
	pprint(ruleDict)

def parseDocument(inputText,start,lvl):
	openP = 0
	closeP = 0
	a = ""
	pc = -1
	print "Parsing document progress:"
	for i in range(start, len(inputText)):
		progress = float(i+1)/len(inputText) * 100
		update_progress(int(progress))
		if (inputText[i] == "\n" ):
			createRules()
			del tempArray[:]
			i += 1
			lvl = -1
		elif (inputText[i] == ")"):
			if(a != "" and a != " "):
				fixRules(a,lvl)
				a = ""
			closeP += 1
			if (openP != closeP):
				lvl -= 1
		elif (inputText[i] == "("):
			if(a != "" and a != " "):				
				fixRules(a,lvl)
				a = ""
			openP += 1
			lvl += 1
		else:
			a += inputText[i]
	print "Parsing document completed successfully"
	
def fixRules(inputString,level):
	fixed = ""
	lvlOff = 0
	for i in range(len(inputString)):
		if(inputString[i] == " "):
			if(fixed != ""):
				tempArray.append(ParsedRules(fixed, level + lvlOff))
				lvlOff += 1
			fixed = ""
		else:
			fixed += inputString[i]
			if(i == len(inputString)-1):
				tempArray.append(ParsedRules(fixed, level + lvlOff))
				lvlOff += 1
				fixed = ""