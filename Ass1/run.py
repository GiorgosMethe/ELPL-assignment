import tree_parser
import cky
import sys
import argparse
import pickle


help = {
	'e':	'Generate a grammar from the passed treebank.',
	'ps':	'CYK parser, takes a sentence as argument.',
	'pf':	'CYK parser, takes a .',
	's':	'Show grammar'
}
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--treebank', nargs=2, help=help['e'])
parser.add_argument('-s', '--s_grammar_file', help=help['s'])
parser.add_argument('-ps', '--ps_grammar_file', nargs=2 , help=help['ps'])
parser.add_argument('-pf', '--pf_grammar_file', nargs=2 , help=help['pf'])
args = parser.parse_args()

# extract args
if args.pf_grammar_file:
	cky.read_pcfg(args.pf_grammar_file[0])
	cky.read_sentences(args.pf_grammar_file[1])
	cky.iterate_sentences()

if args.ps_grammar_file:
	cky.read_pcfg(args.ps_grammar_file[0])
	cky.read_sentences_input(args.ps_grammar_file[1])
	cky.iterate_sentences()

if args.s_grammar_file:
	for line in open(args.s_grammar_file, "r"):
		values = line.split(" ")
		if len(values) == 6:
			print values[0],
			print "\t",
			print str.ljust(values[1],24)," --> ",
			print str.ljust(values[2],24),
			print str.ljust(values[3],24),
			print " probability = ",str.ljust(values[4],24)
		if len(values) == 5:
			print values[0],
			print "\t",
			print str.ljust(values[1],24)," --> ",
			print str.ljust(values[2],24),
			print str.ljust("-",24),
			print " probability = ",str.ljust(values[3],24)

if args.treebank:		
	f = open(args.treebank[0],"r")
	text = f.read()
	tree_parser.parseDocument(text,0,-1)
	tree_parser.fixProbs()
	tree_parser.writeFile(args.treebank[1])