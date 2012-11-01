# parser module

tempArray = []

class ParsedRules(object):
    def __init__(self, rule, lvl):
		self.rule = rule
		self.lvl = lvl

def createRules():
	for j in range(len(tempArray)):
		print tempArray[j].rule, tempArray[j].lvl

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
			parseDocument(inputText, i+1, lvl)
		else:
			a += inputText[i]
		if (openP == closeP):		
			if (inputText[i+1] == "\n"):
				lvl = -1
				parseDocument(inputText, i+2, lvl)
				createRules()
			break
	
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
