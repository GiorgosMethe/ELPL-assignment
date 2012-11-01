# parser module

anArray = []

class ParsedRules(object):
    def __init__(self, rule, lvl):
		self.rule = rule
		self.lvl = lvl

def printRules():
    for item in anArray:
        print item.rule, item.lvl

def parseDocument(inputText,start,lvl):
	openP = 0
	closeP = 0
	a = ""
	for i in range(start, len(inputText)):
		if (inputText[i] == ")"):
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
			parseDocument(inputText, i-1, lvl)
		else:
			a += inputText[i]
		if (openP == closeP):		
			if (inputText[i+1] == "\n"):
				lvl = -1
				parseDocument(inputText, i+2, lvl)
			break
	
def fixRules(inputString,level):
	anArray.append(ParsedRules(inputString, level))
	printRules()
