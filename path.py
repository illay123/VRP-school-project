import networkx as nx
import time
import numpy as np
import math
from sklearn.neighbors import NearestNeighbors
from queue import PriorityQueue
from graph import get_graph

inf = np.Inf

def air_distance(n1,n2):
	return math.sqrt((n1[1]['x']-n2[1]['x'])**2+(n1[1]['y']-n2[1]['y'])**2)

def get_k_family(G,s,k=2):
	"s as a tuple, data = true"
	k_family = []
	node_list = G.nodes(data=True)
	if k == 0:
		return [s]
	if s[1].get('dis') == None:
		s[1]['dis'] = 0
	for node in G.neighbors(s[0]):
		# print (s[1]['dis'])
		# print(G[node][s[0]])
		if node_list[node][1].get('dis') ==None:
			node_list[node][1]['dis'] = inf
		# print(node_list[node][1]['dis'])
		node_list[node][1]['change'] = False
		if node_list[node][1]['dis'] > s[1]['dis'] + G[node][s[0]]['weight']:
			node_list[node][1]['dis'] = s[1]['dis'] + G[node][s[0]]['weight']
			node_list[node][1]['change'] = True
		k_family+=get_k_family(G,node_list[node],k-1)
	# print("k_family ",k_family)
	neighbors = [node_list[node] for node in G.neighbors(s[0])]
	# print("G.neighbors ", neighbors)
	total_list = k_family+neighbors
	return list({v[0]:v for v in total_list}.values())

def heuristic_path_length(G,s,t,deep=2,num=2,number_of_pathes=1):
	"dont work yet"

	q = PriorityQueue()
	nop = 0
	path_length = []

	if s==t:
		return 0
	s[1]['dis'] = 0
	q.put(s)

	while nop<number_of_pathes:
		try:
			vertex = q.get(timeout=5)
		except queue.Empty:
			print ("Fatel error 231") #file 2, function 3, error 1 
		print ("q = ",q.qsize(),"v = ",vertex,"nop = ", nop)
		
		if vertex[0] == t[0]:
			nop+=1
			path_length.append(t[1]['dis'])
			continue

		neighbors_list = get_k_family(G,vertex,k=deep)

		#list of #num heuristic closest to target neighbors
		dis_list = []
		for node in neighbors_list:
			dis_list.append(node[1]['dis']+air_distance(node,t))
		# print(dis_list)
		idx = np.argpartition(dis_list,min(num,len(dis_list)-1))
		for i in idx:
			if neighbors_list[i][1]['change']:
				q.put(neighbors_list[i])

	return min(path_length)

def check():
	G=get_graph()
	print("start")
	start = time.time()
	st = G.nodes(data = True)[0]
	ta = G.nodes(data = True)[25]
	print(heuristic_path_length(G,st,ta,1,2))
	print("my time: ",time.time()-start)
	start = time.time()
	print("real: ",nx.shortest_path_length(G,0,25,weight = 'weight'))
	print("his time: ", time.time()-start)

def air_distance2(n1,n2):
	# G = get_graph()
	# print(G)
	v1 = neighbors_list[n1]
	v2 = neighbors_list[n2]
	# print(n1,n2)
	return math.sqrt((v1[1]['x']-v2[1]['x'])**2+(v1[1]['y']-v2[1]['y'])**2)

def check2():
	G = get_graph()
	start = time.time()
	print("start")
	print ("A*: ",nx.astar_path_length(G,0,2579,air_distance2,'weight'))
	# G = get_graph()
	# v1 = G.nodes(data = True)[10]
	# v2 = G.nodes(data = True)[100]
	print("A*: ",time.time()-start)
	start = time.time()
	print("real: ",nx.shortest_path_length(G,0,2579,weight = 'weight'))
	print("his time: ", time.time()-start)

G = get_graph()
neighbors_list = G.nodes(data = True)
check2()