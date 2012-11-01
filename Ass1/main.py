#(TOP (S (NP (NNP Ms.) (NNP Haag)) (S@ (VP (VBZ plays) (NP (NNP Elianti))) (. .))) )
import tree_parser

f = open('trainingSet.txt',"r")
text = f.read()
tree_parser.parseDocument(text,0,-1)