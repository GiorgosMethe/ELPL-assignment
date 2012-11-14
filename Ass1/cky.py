import sys

rules = dict()
sentences = []

def initialize_threedlist(value):
    list=[]
    for row in range(value):
        list.append([]*value)
        for col in range(value):
        	list[row].append([])
    return list

def readPCFG():
	for line in open("output.txt", "r"):
		values = line.split(" ")
		if len(values) == 5:
			rules[values[2]+" "+values[3]] = dict()
			rules[values[2]+" "+values[3]][values[1]] = values[4]
		else:
			rules[values[2]] = dict()
			rules[values[2]][values[1]] = values[3]

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
		ckyAlgorithm(s)
		i += 1

def checkAndReturnItems(a,b):
	retunTable = [];
	if(len(a)!=0 and len(b)!=0):
		for item1 in a:
			for item2 in b:
				retunTable.append(item1+" "+item2)
	elif len(a)==0:
		for item2 in b:
				retunTable.append(item2)
	else:
		for item1 in a:
				retunTable.append(item1)
	return retunTable


def ckyAlgorithm(s):
	CKYtable = initialize_threedlist(len(s))
	for i in range(len(s)):
		if s[i] in rules:
			for key, value in rules[s[i]].iteritems():
				CKYtable[i][i].append(key)
	n = len(s)
	for i in range(1, n):
		for j in range(n-i+1):
  			for k in range(i-1):
  				for item in checkAndReturnItems(CKYtable[j+k][i-k], CKYtable[j][k]):
						if item in rules:
							for key, value in rules[item].iteritems():
								CKYtable[j][i] = []
								CKYtable[j][i].append(key)
	f = False
	for i in range(len(s)):
		if(len(CKYtable[0][i]) != 0):
			f = True
	print f

def printCKYtable(CKYtable):
	pass
	for a in CKYtable:
		print a
		
