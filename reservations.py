import graph
import cons
import networkx as nx
import time
import numpy as np
import math
import random
import itertools

inf = np.Inf


def optimal2(G,cnode = -1): # recursive naive optimal sulution
	# print(G.nodes(),cnode)
	l = []
	nodeList = G.nodes()
	if len(nodeList) == 1:
		# print("hi")
		return 0
	elif cnode == -1:
		for node in nodeList:
			l.append(optimal(G,node))
	else:
		for node in nodeList:
			if node == cnode:
				continue
			NG = G.copy()
			NG.remove_node(cnode)
			# print(G[cnode][node])
			l.append(optimal(NG,node)+G[cnode][node]['weight'])
	return min(l)

def optimal(G): # naive optimal sulution but more efficient
	# print(G.edges(data = True))
	nodeList = G.nodes()
	size = len(nodeList)
	m = inf
	for perm in itertools.permutations(nodeList):
		i=1
		total = 0
		s = perm[0]
		while i<size:
			t = perm[i]
			total += G[s][t]['weight']
			s = t
			i+=1
		if total < m:
		 	m = total
	return m

def closest_neighbor(G,snode=0):
	current = snode
	total = 0
	unvisited = G.nodes()
	while len(unvisited) != 0:
		length = inf
		for node in unvisited:
			if current != node and length > G[current][node]['weight']:
				length = G[current][node]['weight']
				nex = node
		unvisited.remove(nex)
		total+=length
		current = nex
	return total

#for scn
def normalize(l): 
	total = 0
	new_l = []
	for x in l:
		total+=x
	for x in l:
		new_l.append(x/total)
	return new_l

#for scn
def prob1(G,l,snode):
	prob_list = []
	for node in l:
		if node == snode:
			continue
		prob_list.append(1/G[snode][node]['weight'])
	prob_list = normalize(prob_list)
	return prob_list
	
def prob2(G,l,snode):
	# print(l,snode)
	prob_list = []
	li = list(l)
	# li.remove(snode)
	m = min(G[snode][node]['weight'] for node in li)
	# if m==0:
	# 	raise 'Error'
	prob_list = [(m/G[snode][node]['weight'])**4 for node in li]
	prob_list = normalize(prob_list)
	return prob_list

def statistical_closest_neighbor(G,snode=0,prob = prob1):
	current = snode
	total = 0
	unvisited = G.nodes()
	unvisited.remove(snode)
	while len(unvisited) != 0:
		p = prob(G,unvisited,current)
		r = random.uniform(0, 1)
		i=0
		for x in p:
			if r<x:
				break
			r-=x
			i+=1

		# print(current,",",unvisited)
		total+=G[current][unvisited[i]]['weight']
		current = unvisited[i]
		unvisited.remove(unvisited[i])
	return total

def iterative_statistical_closest_neighbor(G,num = 100,prob = prob1):
	start = time.time()
	l = G.nodes()
	m = []
	m2 = []
	for i in range(1,num):
		for node in l:
			m.append(statistical_closest_neighbor(G,node,prob))
		m2.append(min(m))
	return min(m2)

def check(n = 3):
	print("start")

	G = graph.get_graph()
	JobList = graph.work_generator(G,num=n)

	start = time.time()
	OG = graph.order_graph(G,JobList)
	print("order graph time: ",time.time() - start)

	start = time.time()
	print("optimal: ",optimal(OG)," time: ",time.time() - start)

	start = time.time()
	m = []
	for node in OG.nodes():
		m.append(closest_neighbor(OG,node))
	print("greedy: ",min(m)," time: ",time.time() - start)

	start = time.time()
	m = []
	for node in OG.nodes():
		m.append(statistical_closest_neighbor(OG,node))
	print("statistical: ",min(m)," time: ",time.time() - start)

	start = time.time()
	print("iterative: ",iterative_statistical_closest_neighbor(OG)," time: ",time.time() - start)
	print()

# check(8)