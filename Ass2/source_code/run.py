import tree_parser
import cky
import sys
sys.setrecursionlimit(20000)
import argparse
import utilities

help = {
	'e':	'Generate a grammar from the passed treebank',
	'ps':	'CYK parser, takes a sentence as argument',
	'pf':	'CYK parser, takes a file of sentences and prints the top productions',
	'pfw':	'CYK parser, takes a file of sentences and write a file of top productions',
	'v':	'Viterbi parser, takes a file of sentences and an extracted pcfg and writes the most probable trees for each one of them',
	's':	'Show grammar',
	'm':	'Most likely productions',
	'a':  'Ambiguous words'
}
parser = argparse.ArgumentParser()
parser.add_argument('-e', '--treebank', nargs=2, help=help['e'])
parser.add_argument('-s', '--s_file' , help=help['s'])
parser.add_argument('-a', '--a_file' , help=help['a'])
parser.add_argument('-m', '--m_file',nargs = 2, help=help['m'])
parser.add_argument('-ps', '--ps_file', nargs=2 , help=help['ps'])
parser.add_argument('-pf', '--pf_file', nargs=2 , help=help['pf'])
parser.add_argument('-pfw', '--pfw_file', nargs=3 , help=help['pfw'])
parser.add_argument('-v', '--v_file', nargs=3 , help=help['pfw'])
args = parser.parse_args()

# extract args
if args.pf_file:
	cky.read_pcfg(args.pf_file[0])
	cky.read_sentences(args.pf_file[1])
	cky.iterate_sentences()

if args.v_file:
	cky.read_pcfg(args.v_file[0])
	cky.read_sentences(args.v_file[1])
	cky.iterate_sentences_viterbi(args.v_file[2])

if args.pfw_file:
	cky.read_pcfg(args.pfw_file[0])
	cky.read_sentences(args.pfw_file[1])
	cky.iterate_sentences_write(args.pfw_file[2])

if args.ps_file:
	cky.read_pcfg(args.ps_file[0])
	cky.read_sentences_input(args.ps_file[1])
	cky.iterate_sentences()

if args.s_file:
	for line in open(args.s_file, "r"):
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
	tree_parser.parse_document(text,0,-1)
	tree_parser.fix_probs()
	tree_parser.write_file(args.treebank[1])

if args.m_file:
	utilities.read_pcfg(args.m_file[0])
	# change the second argument to get different number of likely productions
	utilities.most_likely_production(args.m_file[1],4)

if args.a_file:
	utilities.read_pcfg(args.a_file)
	utilities.ambiguous()
