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
		sentences.append(line.split(" "))

def itarateSentences():
	for s in sentences:
		ckyAlgorithm(s)


def ckyAlgorithm(s):
	CKYtable = initialize_threedlist(len(s))
	for i in range(1,len(s)):
		for key, value in rules[s[i]].iteritems():
			CKYtable[i][i].append(key)
	n = len(s)
	for i in range(1, n):
		for j in range(0,n-i+1):
  			for k in range(0,i-1):
  				print j,i
  				for itemA in CKYtable[j+k][i-k]:
  					for itemB in CKYtable[j][k]:
  						st = itemA +" "+ itemB
  						st1 = itemB +" "+itemA
  						if st1 in rules:
							for key, value in rules[st1].iteritems():
								CKYtable[j][i].append(key)
  						if st in rules:
							for key, value in rules[st].iteritems():
								CKYtable[j][i].append(key)
	f = False
	for i in range(len(s)):
		if(len(CKYtable[0][i]) != 0):
			f = True
	print f

	# printCKYtable(CKYtable);


def printCKYtable(CKYtable):
	pass
	for a in CKYtable:
		print a
		