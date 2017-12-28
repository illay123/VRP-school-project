import networkx

def air_distance(n1,n2):
	v1 = neighbors_list[n1]
	v2 = neighbors_list[n2]
	return math.sqrt((v1[1]['x']-v2[1]['x'])**2+(v1[1]['y']-v2[1]['y'])**2)

class cluster(object):
	"""docstring for cluster"""
	def __init__(self,G,job):
		super(cluster, self).__init__()
		self.path = nx.astar_path(G,job[0],job[1],air_distance,'weight')
		self.length = nx.astar_path_length(G,job[0],job[1],air_distance,'weight')
		self.POP = [job]

	def unite(self,G,next):
		if self == next:
			return false
		length, path() = shortest_path_points(G,self.POP+[next])
		if length >= :
			pass



		

def cluster_list(G,jobList):
	""
	cl = []
	cjobList = [cluster(G,job) for job in job list]
	for currentJob in cjobList:
		for nextJob in cjobList:
			if currentJob.unite(G,nextJob):
				remove(nextJob)
		cl.append(currentJob)
	return cl

	pass

def cluster_graph(G,jobList):
	pass