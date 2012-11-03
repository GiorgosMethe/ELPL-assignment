import tree_parser

f = open('trainingSet.txt',"r")
text = f.read()
tree_parser.parseDocument(text,0,-1)
tree_parser.fixProbs()
tree_parser.writeFile()