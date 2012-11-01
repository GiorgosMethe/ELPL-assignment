#(TOP (S (NP (NNP Ms.) (NNP Haag)) (S@ (VP (VBZ plays) (NP (NNP Elianti))) (. .))) )
import parser

f = open('trainingSet',"r")
text = f.read()
parser.parseDocument(text,0,-1)





