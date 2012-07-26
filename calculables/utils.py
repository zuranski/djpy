import math
from scipy.cluster.hierarchy import *
import numpy as np

def MakeClusters(list,dist):
	if len(list)<2: return []
        X = np.array([[a] for a in list])
        T = fclusterdata(X,dist,criterion='distance')
        N = max(T)
        clusters = [[] for i in range(N)]
        for i in range(len(T)):
                clusters[T[i]-1].append(i)
        return [clr for clr in clusters if len(clr)>1]


def DeltaPhi(obj1,obj2):
	dphi = obj1.phi - obj2.phi
        while (dphi > math.pi ): dphi -= 2*math.pi
        while (dphi <= -math.pi ): dphi += 2*math.pi
	return dphi

def DeltaR(obj1,obj2):

        deta = obj1.eta - obj2.eta
	dphi = DeltaPhi(obj1,obj2)
        return math.sqrt(deta*deta + dphi*dphi)

def Theta(eta):
	return 2*math.atan(math.exp(-eta))

def StDev(list,center=None):
	if len(list) == 0: return 1e10
	if center is None: center = sum(list)/float(len(list))
	stdev = 0
	for item in list:
		stdev += math.pow((item-center)/center,2)
	return math.sqrt(stdev/float(len(list)))

def AvgDistance(list,weights=None,center=None):
	if len(list) == 0 : return 1e10
	if weights is None : weights = [1]*len(list)
	if center is None: center = sum(list)/float(len(list))
	AvgDist = 0
	sumWeights = 0
	for item,w in zip(list,weights):
		AvgDist += w*abs(item-center)/abs(center)
		sumWeights += w
	return AvgDist/sumWeights/float(len(list))

def Avg(list,weights=None):
	if len(list) == 0 : return 1e10 
	if weights is None: weights = [1]*len(list)
	Avg = 0
	sumWeights = 0
	for item,w in zip(list,weights):
		Avg += item*w
		sumWeights += w
	return Avg/float(sumWeights)
