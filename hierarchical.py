import re
import math
import time
import numpy as np
import matplotlib.pyplot as plt


#to hierarchical clustering with Eucledean distance.
#cluster distance is average distance
#agglomerative algorithm



#to implement a hierarchical cluster algorithm

#check if a point is in an list of points
def pointIn(p, ps):
	result=False
	for i in range(len(ps)):
		if ps[i].index==p.index:
			result=True
	return result
#find the index	of a poinnt in a list of list of points
#garranteed to be there
def getIndex(p,clusters):
	index=0
	for i in range(len(clusters)):
		if pointIn(p,clusters[i]):
			index=i
	return index	

#distance of 2 points
def distance(pa, pb):
	#a and b are data points
	d=0
	data1=pa.data
	data2=pb.data
	for i in range(len(pa.data)):
		d=d+ (data1[i]-data2[i])*(data1[i]-data2[i])
	d=math.sqrt(d)
	return d
		

#distance of 2 cluster of points
def nodeDistance(na, nb):
		#use mean distance as meansure of distance between clusters
		lena=len(na.points)
		lenb=len(nb.points)
		if lena==0 or lenb==0:
			return 0
		dist=0
		for i in range(lena):
			for j in range(lenb):
				dist=dist+distance(na.points[i],nb.points[j])
		dist=dist/(lena*lenb)
		return dist
#represents a data point		
class Point():
	def __init__(self, index, data, label):
		self.index=index #as a indexing id for data point
		self.data=data
		self.label=label
#represents a clustering node
class Node():
	def __init__(self,points,step):
		self.points=points #a list of datapoints
		self.step=step
		self.edges=[]

#class to do hierarchial clustering
class HierarchyCluster():
	def __init__(self):
		#self.nodes=[]
		clusters=[]   #current nodes during calculation
		self.allpoints=[]  #holds all data points
		self.givenClusters=[] #calculate based on label 
		for i in range(4):
			self.givenClusters.append([])
		data=readData()
		dimension=len(data[0])-1
		print("the dimension of data is")
		print(dimension)
		for i in range(len(data)):
			if np.random.rand()<=0.01:  #randomly get about 400 samples
				p=Point(i,data[i][1:],data[i][0])
				self.allpoints.append(p)
				self.givenClusters[int(data[i][0])-1].append(p)
				n=Node([p],len(data))
				clusters.append(n)
			#inittiating clusters with single nodes.
		#building the hierarchical tree
		
		
		length=len(clusters)
		print("initial length "+str(length))
		self.alldistance=np.zeros((length,length))
		for i in range(length):
			for j in range(length):
				self.alldistance[i][j]=distance(clusters[i].points[0],clusters[j].points[0])
		
		while length>1:
			minavd=nodeDistance(clusters[0],clusters[1])
			indexa=0
			indexb=1
			for i in range(length-1):
				for j in range(i+1,length):
					#print(j)
					d=nodeDistance(clusters[i],clusters[j])
					#print(d)
					if d < minavd:
						minavd=d
						indexa=i
						indexb=j
			#print("loop")
			n1=clusters.pop(indexa)
			n2=clusters.pop(indexb-1)			
			#clusters[i].points=n1.points+n2.points
			nodet=Node(n1.points+n2.points,length)
			self.connect(nodet,n1)
			self.connect(nodet,n2)
			#print("node has edges "+ str(len(nodet.edges)))
			clusters.append(nodet)
			length=length-1
			print("current length "+str(length))
		self.root=clusters[0]	
		
			
		
	def connect(self, nodea,nodeb):
		nodea.edges.append(nodeb)
		
	
	#from the hierarchical clustering generate clusters given the number of groups	
	def generateClusters(self,groupnumber):
	
		resultnodes=[self.root]
		while len(resultnodes) < groupnumber:
			minstep=10000
			minindex=0
			for i in range(len(resultnodes)):
				if resultnodes[i].step<minstep:
					minstep=resultnodes[i].step
					minindex=i
			n=resultnodes.pop(minindex)
			for i in range(len(n.edges)):
				resultnodes.append(n.edges[i])
			
			
		result=[]
		for i in range(len(resultnodes)):
			result.append(resultnodes[i].points)
			print(len(resultnodes[i].points))
		return result		
		#n is the number of clusters
	

	#calculate Rand Index
	def randIndex(self,clusters):
		print("cluster has "+str(len(clusters)))
		print("given clusters has "+str(len(self.givenClusters)))
		c2=self.givenClusters
		l=len(self.allpoints)
		count=0
		for i in range(l-1):
			for j in range(i+1,l):
				i1=getIndex(self.allpoints[i], c2)
				i2=getIndex(self.allpoints[i],clusters)
				j1=getIndex(self.allpoints[j],c2)
				j2=getIndex(self.allpoints[j],clusters)
				if i1==j1 and i2==j2:
					count=count+1
				if i1!=j1 and i2!=j2:
					count=count+1
				#print( str(i1)+" "+str(j1)+ " "+str(i2)+" "+str(j2))
		return 2*count/(l * l-1)
			
		
	
	
	
		

def readData():
	data=[]
	with open('data.txt', newline='') as csvfile:
			for line in csvfile:
				sp=re.split(" +",line)
				p=[]
				for i in range(len(sp)-1):
					p.append(float(sp[i+1]))
				data.append(p)
	return data
	
	





#the executing body
			
g=HierarchyCluster()
ris=[]
for i in range(2,10):
	c1=g.generateClusters(i)  
	ri=g.randIndex(c1)
	ris.append(ri)

plt.plot(range(2,10), ris)
plt.title('cluster number vs Rand Index')
plt.xlabel('cluster number')
plt.ylabel('Rand Index')
plt.grid(True)
plt.show()
 


