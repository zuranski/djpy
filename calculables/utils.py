import math

def DeltaPhi(phi1,phi2):
	dphi = phi1 - phi2
	while (dphi > math.pi ): dphi -= 2*math.pi
	while (dphi <= -math.pi ): dphi += 2*math.pi
	return dphi

def DeltaR(eta1,phi1,eta2,phi2):

	deta = eta1 - eta2
	dphi = DeltaPhi(phi1,phi2)
	return math.sqrt(deta*deta + dphi*dphi)

def Theta(eta):
	return 2*math.atan(math.exp(-eta))

def p(pt,eta):
	return pt*math.cosh(eta)

def MatchByDR(eta1_v,phi1_v,eta2_v,phi2_v,DRmax):
	matched = [None for i in range(len(eta1_v))]
	for i in range(len(eta1_v)):
		bestDR = 1e5
		bestMatchIdx = None 
		for j in range(len(eta2_v)):
			DR = DeltaR(eta1_v[i],phi1_v[i],eta2_v[j],phi2_v[j])
			if (DR < bestDR) and (DR < DRmax) : 
				bestMatchIdx = j
				bestDR = DR
		matched[i] = bestMatchIdx
	return matched

def passed (e,idx,cut):
	var = e[cut['name']][idx]
	passVal = (var == cut['val']) if 'val' in cut else True
	passMin = (var >= cut['min']) if 'min' in cut else True
	passMax = (var <= cut['max']) if 'max' in cut else True
	return (passVal and passMin and passMax)

def mergeVectors(vectors):
	out=[]
	for vec in vectors:
		out+=[a for a in vec]
	return out
