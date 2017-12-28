import networkx as nx
import csv
import time
import numpy as np
import math
import cons
from sklearn.neighbors import NearestNeighbors

inf = np.Inf
neighbors_list=[]
def air_distance2(n1,n2):
	# G = get_graph()
	# print(G)
	global neighbors_list
	v1 = neighbors_list[n1]
	v2 = neighbors_list[n2]
	# print(n1,n2)
	return math.sqrt((v1[1]['x']-v2[1]['x'])**2+(v1[1]['y']-v2[1]['y'])**2)

def get_graph():
	G = nx.Graph()
	f1 = csv.reader(open("SFV.txt"),delimiter=' ')
	i = 0
	for row in f1:
		G.add_node (int(row[0]),x=float(row[1]),y=float(row[2]))

	f1 = csv.reader(open("SFE.txt"),delimiter=' ')
	for row in f1:
		G.add_edge(int(row[1]),int(row[2]),weight=float(row[3]))
	return G

def get_lop_graph(jobList):
	"unescery"
	G=get_graph()
	node_list = G.nodes(data = True)
	for job in jobList:
		node_list[jobList[0]][1]['label'] = 'save'
		node_list[jobList[1]][1]['label'] = 'save'
	for node in node_list:
		if node[1]['label'] != 'save':
			G.remove_node(node[0])
	return G

def get_square_graph (x,y,h):
	"left down"
	G = get_graph()
	for node in G.nodes(data=True):
		if node[1]['x'] < float(x) or node[1]['x'] > float(x+h):
			G.remove_node(node[0])
		elif node[1]['y'] < y or node[1]['y'] > y+h:
			G.remove_node(node[0])
	return G

def air_distance(n1,n2):
	"data = True"
	return math.sqrt((n1[1]['x']-n2[1]['x'])**2+(n1[1]['y']-n2[1]['y'])**2)

def work_generator(G,mean_distance=800,lcornerx=0,lcornery=0,graph_x_length = 10000,graph_y_length = 10000,radius = 50,num=1):
	i=0
	ch=0
	jobList=[]
	node_list = G.nodes(data=True)
	nbrs = NearestNeighbors(n_neighbors=1, algorithm='ball_tree').fit([(node[1]['x'],node[1]['y'])for node in node_list])
	while i<num:
		distance = np.random.rayleigh(mean_distance)
		angle = np.random.uniform(0,2)
		x = np.random.uniform(lcornerx,lcornerx+graph_x_length)
		y = np.random.uniform(lcornery,lcornery+graph_y_length)
		sp_distances, sp_indices = nbrs.kneighbors([[x,y]])
		if sp_distances[0][0]>radius:
			ch+=1
			continue
		ep_distances, ep_indices = nbrs.kneighbors([[x+(distance+50)*math.cos(angle),y+(distance+50)*math.sin(angle)]])
		if ep_distances[0][0]>radius:
			ch+=1
			continue
		# if air_distance(sp_indices[0][0],ep_indices[0][0])<5:
		# 	ch+=1
		# 	continue
		jobList.append((node_list[sp_indices[0][0]],node_list[ep_indices[0][0]]))
		i+=1
	# print(ch)
	return jobList

def order_graph2(G,jobList):
	work_graph = nx.DiGraph()
	global neighbors_list
	neighbors_list = G.nodes(data = True)
	s=0
	t=0
	for sjob in jobList: # sjob is the starting job veretex
		for tjob in jobList: # tjob is the target job vetex
			if tjob == sjob:
				t+=1
				continue
			else:	
				work_graph.add_edge(s,t,weight = nx.shortest_path_length(G,sjob[1][0],tjob[0][0],weight = 'weight'))
				# print(nx.shortest_path_length(G,sjob[1][0],tjob[0][0],weight = 'weight'))
				# print(s,",",t)
				# print("*")
				t+=1
		# work_graph[s]['inner_length'] = nx.astar_path_length(G,sjob[0][0],sjob[1][0],air_distance2) # the inner length is the distance between the starting point and the end point of the order
		s+=1
		t=0
	return work_graph

def order_graph(G,jobList):
	work_graph = nx.DiGraph()
	global neighbors_list
	neighbors_list = G.nodes()
	s=0
	t=0
	for sjob in jobList: # sjob is the starting job veretex
		l = nx.shortest_path_length(G,sjob[0][0],weight = 'weight')
		for tjob in jobList: # tjob is the target job vetex
			if tjob == sjob:
				t+=1
				continue
			else:
				# print(l[tjob[1][0]])
				work_graph.add_edge(s,t,weight = l[tjob[1][0]])
				t+=1
		s+=1
		t=0
	return work_graph

def check():
	start = time.time()
	G=get_graph()
	jobList = work_generator(G,num = 10)
	# print(jobList)
	OG = order_graph(G,jobList)
	print(time.time()-start)