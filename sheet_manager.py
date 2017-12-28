import time
import graph
import reservations
from cons import v
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import csv
import statistics
import _thread
import itertools

inf = np.Inf
acorner = 6000
alength = 2000

def basic_graph_report():
	f = open('Report graph-basic.txt', 'w')
	print('first report, include info on the nodes, edges and statistics on them\n',file=f)  # python will convert \n to os.linesep
	lonley_nodes = 0
	lonley_nodes2 = 0
	G = graph.get_graph()
	i=0
	maxi = 0
	maxo = 0
	maxio=0
	linear = 0
	while i<v:
		od = G.out_degree(i)
		ind = G.in_degree(i)
		d=G.degree(i)
		if od==0:
			lonley_nodes+=1

		if ind==0:
			lonley_nodes2+=1

		if ind == 1 and od ==1:
			linear+=1

		if od > maxo:
			maxo = od
		if ind>maxi:
			maxi = ind
		if d>maxio:
			maxio =d
		i+=1


	print("number of nodes:",G.number_of_nodes(),"\n",file=f)
	print("number of edges",G.number_of_edges(),"\n",file=f)
	print("dead ends: ",lonley_nodes,"\n",file=f)
	print("no entry: ",lonley_nodes2,"\n",file=f)
	print("max in degree: ",maxi,"\n",file=f)
	print("max out degree: ",maxo,"\n",file=f)
	print("linear nodes (in and out degree of one): ",linear,"\n",file=f)
	print("max in and out degree: ",maxio,"\n",file=f)


	localtime = time.asctime( time.localtime(time.time()) )
	print("end of report, created at ",localtime,file=f)
	print("finish the processing of report #1")
	f.close()

def graph_histograms2():
	i = 0
	G = graph.get_graph()
	a =[G.degree(i) for i in range(0,v)]
	plt.figure()
	plt.hist(a,50, facecolor='green', alpha=0.5)
	plt.xlabel('degree')
	plt.ylabel('num of vertices')
	plt.yscale('log')
	plt.title('degrees')
	plt.axis([0, 6, 0, v])
	plt.grid(True)
	plt.savefig("images/histogrem graph-data degree")

	print("finish the processing of report #2.2")
def graph_histograms():
	ain = []
	aout = []
	i=0
	G = graph.get_graph()

	while i<v:
		od = G.out_degree(i)
		ind = G.in_degree(i)
		#d=G.degree(i)
		ain.append(ind)
		aout.append(od)
		i+=1
		# the histogram of the data
	plt.figure()
	plt.hist(ain,50, facecolor='green', alpha=0.5)
	plt.xlabel('in degree')
	plt.ylabel('num of vertices')
	plt.yscale('log')
	plt.title('in degrees')
	plt.axis([0, 6, 0, v])
	plt.grid(True)
	plt.savefig("images/histogrem graph-data in-degree")

	plt.figure()
	plt.hist(aout,50, facecolor='green', alpha=0.5)
	plt.xlabel('out degree')
	plt.ylabel('num of vertices')
	plt.yscale('log')
	plt.title('out degrees')
	plt.axis([0, 6, 0, v])
	plt.grid(True)

	plt.savefig("images/histogrems graph-data out-degree.png")
	print("finish the processing of report #2")

def generator_visualization():
	G = graph.get_square_graph(6900,4100,500)
	job_list = graph.work_generator(G,80,6900,4100,500,500,num=5)
	i=1
	# print(job_list)
	nodes_list = G.nodes(data=True)
	for job in job_list:
		# print(G.nodes(data=True)[job[0][1]])
		# print(job[1])
		job[0][1]['label'] = str(i)+".s"
		job[1][1]['label'] = str(i)+".d"
		i+=1
	nx.draw(G,location_list(G),node_size=0.01,labels=nx.get_node_attributes(G, 'label'), font_color = 'g')
	plt.savefig("images/Visualization work-generator for learn2.png")
	print("finish the processing of report #3")

def generator_histograms():
	generator_histograms1()
	generator_histograms2()
	print("finish the processing of report #4")

def generator_histograms1():
	G = graph.get_graph()
	# nodes_list = G.nodes(data=True)
	air_dis=[]
	job_list = graph.work_generator(G,radius = 100,mean_distance=100,num=500)
	for job in job_list:
		# print(job)
		air_dis.append(graph.air_distance(job[0],job[1]))
	plt.figure()
	plt.hist(air_dis,50, facecolor='green', alpha=0.5)
	plt.xlabel('air distance of travel')
	plt.ylabel('num of travels')
	plt.title('distrbution of air distances mean = 100 num = 500')
	plt.grid(True)
	plt.savefig("images/histogrem generator-data air-dis.png")

def generator_histograms2():
	G = graph.get_square_graph(acorner,acorner,alength)
	nodes_list = G.nodes(data=True)
	job_list = graph.work_generator(G,mean_distance=160,lcornerx=acorner,lcornery=acorner,graph_x_length = alength,graph_y_length = alength,radius = 50,num=500)
	real_dis=[]
	i=0
	for job in job_list:
		try:
			real_dis.append(nx.shortest_path_length(G,source=job[0][0],target=job[1][0],weight = 'weight'))
		except nx.exception.NetworkXNoPath as e:
			print("unreachable")
		i+=1
		print(i)
	plt.figure()
	plt.hist(real_dis,50, facecolor='green', alpha=0.5)
	plt.xlabel('real distance of travel')
	plt.ylabel('num of travels')
	plt.title('distrbution of real distances mean = 160 num = 500')
	plt.grid(True)
	plt.savefig("images/histogrem generator-data real-dis2.png")

def order_graph_visualization(num=5):
	G = graph.get_graph()
	JobList = graph.work_generator(G,num = num)

	# print(JobList)

	OG = graph.order_graph(G,JobList)

	print (len(OG.edges()))

	nx.draw(OG)
	plt.savefig("images/Visualization order_grpah of 5.png")
	print("finish the processing of report #5")

# function
def location_list(G):
	a={}
	for node in G.nodes(data=True):
		a[node[0]] = (node[1]['x'],node[1]['y'])
	return a

def refrsh():
	generator_histograms()
	generator_visualization()
	basic_graph_report()
	graph_histograms()

def check():
	G = graph.get_square_graph(acorner,acorner,200)
	print(G.nodes())
	print(graph.work_generator(G,mean_distance=160,lcornerx=acorner,lcornery=acorner,graph_x_length = alength,graph_y_length = 200,radius = 50,num=5))

def reservation_heuristics_numbers(size = 9, num = 100):
	f = open('images/Numbers reservation-hueristics2.csv', 'w')
	print("start")
	print('size,optimal,greedy,statistic1,statistic2,iterative1,iterative2',file=f)
	for x in range(0,num):
		G = graph.get_graph()
		JobList = graph.work_generator(G,num=size)
		OG = graph.order_graph(G,JobList)

		o=reservations.optimal(OG)
		s1=min([reservations.statistical_closest_neighbor(OG,node,reservations.prob1) for node in OG.nodes()])
		s2=min([reservations.statistical_closest_neighbor(OG,node,reservations.prob2) for node in OG.nodes()])
		g=min([reservations.closest_neighbor(OG,node) for node in OG.nodes()])
		i1=reservations.iterative_statistical_closest_neighbor(OG,100,reservations.prob1)
		i2=reservations.iterative_statistical_closest_neighbor(OG,100,reservations.prob2)

		print(size,',',o,',',g,',',s1,',',s2,',',i1,',',i2,file=f)
		print(x)
	print("finish processing of report #6")

def reservation_heuristics_report():
	f = csv.reader(open("images/Numbers reservation-hueristics2.csv"),delimiter=',')
	file = open('images/Report reservations_heuristics.txt', 'w')
	print("calculations on algorithms",file=file)
	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)
	for i in range(1,6+1):
		print(name[i],"-> mean: %.2f "%statistics.mean(a[:,i]),"median: %.2f "%statistics.median(a[:,i]),"standerd deviation: %.2f"%statistics.stdev(a[:,i]),file=file)
	print("finish processing of report #7")

def reservation_heuristics_gof_report():
	"based of goodness of fit test"
	size = 200
	f = csv.reader(open("images/Numbers reservation-hueristics2.csv"),delimiter=',')
	file = open('images/Report goodness_of_fit.txt', 'w')
	print("calculations on algorithms",file=file)
	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)

	chi_squared = []
	for i in range(2,6+1):
		results =[]
		j=0
		while j< size:
		 	results.append((a[:,1][j]-a[:,i][j])**2/a[:,i][j])
		 	j+=1
		chi_squared.append(sum(results))
		print(name[i],"-> mean: %.2f "%sum(results),file=file)
	print("finish processing of report #8")

def MSE():
	"based of goodness of fit test"
	size = 200
	f = csv.reader(open("images/Numbers reservation-hueristics2.csv"),delimiter=',')
	file = open('images/Report MSE.txt', 'w')
	print("calculations on algorithms",file=file)
	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)

	chi_squared = []
	for i in range(1,6+1):
		results =[]
		j=0
		while j< size:
		 	results.append((1 - a[:,1][j]/a[:,i][j]))
		 	j+=1
		# chi_squared.append(sum(results))
		print(name[i],"-> mean: %.2f "%(sum(results)/200),file=file)
	print("finish processing of report #8")

def reservation_solver_with_iterative_numbers_per_it_num(size = 9, num = 100, itnum = 250):
	f = open('images/Numbers reservation for iteration graph4.csv', 'w')
	print("start")
	print('size,iterations,optimal,iterative',file=f)
	for it in range(2,itnum):
		for x in range(0,num):
			G = graph.get_graph()
			JobList = graph.work_generator(G,num=size)
			OG = graph.order_graph(G,JobList)

			o=reservations.optimal(OG)
			i=reservations.iterative_statistical_closest_neighbor(OG,it,reservations.prob2)

			print(size,',',it,',',o,',',i,file=f)
			print(x,":",it)
	print("finish processing of report #6.1")
	f.close()

def t_manager():
	print("start")
	try:
		_thread.start_new_thread(reservation_solver_with_iterative_numbers_per_it_num2,(9,20,250,'default1.csv',))
		_thread.start_new_thread(reservation_solver_with_iterative_numbers_per_it_num2,(9,20,250,'default2.csv',))
	except:
		print("paralelism error")

def reservation_solver_with_iterative_numbers_per_it_num2(size = 9, num = 100, itnum = 250,fileName = 'default.csv'):
	f = open('images/'+fileName, 'w')
	print("start")
	print('size,iterations,optimal,iterative',file=f)
	for x in range(0,num):
		G = graph.get_graph()
		JobList = graph.work_generator(G,num=size)
		OG = graph.order_graph(G,JobList)
		o=reservations.optimal(OG)
		OG.graph['SP']=o
		string = "Test Cases/test case #"+str(x)+".gml"
		nx.write_gml(OG,string)

		for it in range(2,itnum):
			i=reservations.iterative_statistical_closest_neighbor(OG,it,reservations.prob2)

			print(size,',',it,',',o,',',i,file=f)
			print(x,":",it)
	print("finish processing of report #6.1")
	f.close()

def Error(a1,a2,b1,b2,c1,c2):
	a = a2/a1
	b = b2/b1
	c = c2/c1
	return (a+b+c)/3

def iter_to_accuracy_solver_graph():
	f = csv.reader(open("images/Numbers reservation for iteration improved.csv"),delimiter=',')
	print("start")

	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)
	results = [0]*250

	for i in range(2,250):
		for x in range(1,30):
			results[i]+=(a[i*x+1][3]/a[i*x+1][2]-1)/29
			# print(a[i*x-2][3],a[i*x-2][2])
	# print(a[0])
	# print(a[0][3]/a[0][2])
	# print(a[0][0][2])
	# print(i*x+1)

	# print(results[2:5])
	results = results[2:]
	plt.figure()
	plt.plot(range(2,250),results)
	plt.xlabel('num of iterations')
	plt.ylabel('Error - MSE')
	plt.title('Error to iterations number of the solver function\n for 9 customers on map')
	# plt.grid(True)
	plt.savefig("images/final graph.png")
	print("finish processing of report #9")

def iter_to_accuracy_solver_graph2(amunt = 5):
	f = csv.reader(open("images/Numbers reservation for iteration improved.csv"),delimiter=',')
	print("start")
	num = 248
	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)
	results = np.empty((amunt,num))

	for i in range(0,num):
		for x in range(0,amunt):
			ai = i+num*x-2
			results[x][i]+=(a[ai][3]/a[ai][2]-1)
			# print(ai)
	for x in range(0,amunt):
		for i in range(3,num):
			results[x][i]=min([results[x][i],results[x][i-1]])

	print("breakpoint #1")
	plt.figure()
	# print(len(results[0]),len(range(0,num)))
	for i in range(0,amunt):
		plt.plot(range(3,num),results[i][3:])
	# plt.plot(range(0,num),results[1])
	plt.xlabel('num of iterations')
	plt.ylabel('Error - MSE')
	plt.title('Error to iterations number of the solver function\n for 9 customers on map')
	# plt.grid(True)
	plt.savefig("images/final graph2-2+1.png")
	print("finish processing of report #9")

def iter_to_accuracy_solver_graph3(amunt = 30):
	f = csv.reader(open("images/Numbers reservation for iteration improved.csv"),delimiter=',')
	print("start")
	num = 248
	name = next(f) # skip the description line
	a = [list(map(float,row)) for row in f]
	a = np.array(a)
	results = np.empty((num))

	for i in range(0,num):
		for x in range(0,amunt):
			ai = i+num*x
			if (a[ai][3]==a[ai][2]):
				results[i]+=1

	for n in results:
		print("%.2f",n)
	for i in range(2,num):
		results[i]=max([results[i],results[i-1]])
	print("after")
	for n in results:
		print("%.2f",n)
	# print(results[2:5])
	print("breakpoint #1")
	# print(results)
	plt.figure()
	# print(len(results[0]),len(range(0,num)))
	val = []
	for n in results:
		val.append(n/30)
	# print(val)
	plt.plot(range(10,num),val[10:])
	# plt.plot(range(0,num),results[1])
	plt.xlabel('num of iterations')
	plt.ylabel('num of perfect calculations')
	plt.title('Error to iterations number of the solver function\n for 9 customers on map')
	# plt.grid(True)
	plt.savefig("images/final graph3.png")
	print("finish processing of report #9")

def time_to_iter (size = 9):
	G = graph.get_graph()
	JobList = graph.work_generator(G,num=size)
	OG = graph.order_graph(G,JobList)

	t = time.time()
	o=reservations.optimal(OG)
	print (str(time.time() - t)+"for optimal")
	# s1=min([reservations.statistical_closest_neighbor(OG,node,reservations.prob1) for node in OG.nodes()])
	# s2=min([reservations.statistical_closest_neighbor(OG,node,reservations.prob2) for node in OG.nodes()])
	# g=min([reservations.closest_neighbor(OG,node) for node in OG.nodes()])
	# i1=reservations.iterative_statistical_closest_neighbor(OG,100,reservations.prob1)
	t = time.time()
	i2=reservations.iterative_statistical_closest_neighbor(OG,100,reservations.prob2)
	print (str(time.time() - t)+"for 100")

def new_graph_script(noi = 1000):
	size = 80
	G = graph.get_graph()
	JobList = graph.work_generator(G,num = size)
	print("finish creating job list")
	OG = graph.order_graph(G,JobList)

	sp = 1
	print("starting to calculate")
	greed = reservations.closest_neighbor(OG,sp)
	print(greed)
	print("start random restarts")
	a = np.empty([noi])
	m = np.Inf
	for i in range(0,noi):
		print(str(i)+" - best is: ",str(m))
		m = min([m,reservations.statistical_closest_neighbor(OG,snode = sp,prob = reservations.prob2)])
		# print(reservations.statistical_closest_neighbor(OG,snode = 0))
		a[i] = m

	plt.figure()
	base = np.empty([noi])
	base.fill(greed)
	plt.plot(range(0,noi),base)
	plt.plot(range(0,noi),a)

	plt.xscale('log')
	plt.xlabel('num of iterations')
	plt.ylabel('value')
	plt.title('compare between greedy and stochastic over 80 orders graph')
	# plt.grid(True)
	plt.savefig("images/improved smood graph4.png")
	print("finish processing of report #10")





iter_to_accuracy_solver_graph2()
# new_graph_script()