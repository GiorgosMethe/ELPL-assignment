import threading
from threading import Thread

binary_node = "@"
unary_node = "%%%%%"
nodes = []

class tree_node():
    def __init__(self, node, lvl, terminal):
    	self.node = node
        self.lvl = lvl
        self.terminal = terminal

def build_tree(words):
	tree_bank = ""
	level = -1
	i = 0
	if len(words) > 15:
		tree_bank += "(TOP"
		for item in words:
			tree_bank += " (POS " + item + ")"
		tree_bank += ")"
	else:
		if len(nodes) == 1:
			tree_bank += "(TOP)"
		else:	
			while i != len(nodes):
				if nodes[i].lvl < level:
						for w in range(level-nodes[i].lvl):
							tree_bank += ")"
							level -= 1
				if nodes[i+1].terminal == True:
					tree_bank += " (" + str(nodes[i].node) + " " + str(nodes[i+1].node) + ")"
					level = nodes[i].lvl
					i +=1
				else:
					tree_bank += " (" + str(nodes[i].node) + " "
					level = nodes[i].lvl
				i += 1
			for i in range(level):
				tree_bank += ")"
	
	write_treebank(tree_bank, "out1")
	del nodes[:]


def run(chart,x,y,node,words,lvl):
	if binary_node in node:
		lvl -= 1
	else:
		if unary_node in node:
			temp = node.split(unary_node)
			nodes.append(tree_node(temp[0],lvl,False))
			nodes.append(tree_node(temp[1],lvl+1,False))
			lvl += 1
		else:
			nodes.append(tree_node(node,lvl,False))
	if node in chart[x,y]:
		max_prob = chart[x,y][node].prob
		max_node = chart[x,y][node].child
		max_item = chart[x,y][node]
		if max_node == node or max_node in words:
			nodes.append(tree_node(max_node,lvl+1,True))
			return
		if max_item.unary:
			run(chart,x,y,max_node,words,lvl+1)
			return
		else:
   	 		run(chart,x,max_item.split,max_node[0],words,lvl+1)
    		run(chart,max_item.split,y,max_node[1],words,lvl+1)
    		return
	else:
		return


def write_treebank(treebank,file_name):
	f = open(file_name, 'a')
	f.write(treebank+"\n")
	f.close()