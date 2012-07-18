
def DeltaPhi(obj1,obj2):
	dphi = obj1.phi - obj2.phi
	import math
        while (dphi > math.pi ): dphi -= 2*math.pi
        while (dphi <= -math.pi ): dphi += 2*math.pi
	return dphi

def DeltaR(obj1,obj2):

        import math
        deta = obj1.eta - obj2.eta
	dphi = DeltaPhi(obj1,obj2)
        return math.sqrt(deta*deta + dphi*dphi)

def Theta(eta):
	import math
	return 2*math.atan(math.exp(-eta))

def StDev(list,center=None):
	if len(list)<2: return 9999
	import math
	if center is None: center = sum(list)/float(len(list))
	stdev = 0
	for item in list:
		stdev += math.pow((item-center)/center/center,2)
	return math.sqrt(stdev/float(len(list)))

def AvgDistance(list,weights=None,center=None):
	if len(list)<2: return 9999
	if center is None: center = sum(list)/float(len(list))
	AvgDist = 0
	if weights is not None:
		sumWeights = 0
		for item,w in zip(list,weights):
			AvgDist += w*abs(item-center)/abs(center)/abs(center)
			sumWeights += w
		return AvgDist/sumWeights/float(len(list))
	else:
		for item in list:
			AvgDist += abs(item-center)/abs(center)/abs(center)
		return AvgDist/float(len(list))
