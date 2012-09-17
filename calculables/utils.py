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

def passed (var,cut):
	passVal = (var == cut['val']) if 'val' in cut else True
	passMin = (var >= cut['min']) if 'min' in cut else True
	passMax = (var <= cut['max']) if 'max' in cut else True
	return (passVal and passMin and passMax)

def abcdCmp(histo):
	a = histo.GetBinContent(1,1)
	aerr = histo.GetBinError(1,1)
	b = histo.GetBinContent(1,2)
	berr = histo.GetBinError(1,2)
	c = histo.GetBinContent(2,1)
	cerr = histo.GetBinError(2,1)
	d = histo.GetBinContent(2,2)
	derr = histo.GetBinError(2,2)
	exp = 0
	expErr = 0
	if a>0 and b>0 and c>0 and d>0:
		exp = math.log(a*d/float(b*c))
		expErr = math.sqrt(pow(aerr/float(a),2)+pow(berr/float(b),2)+pow(cerr/float(c),2)+pow(derr/float(d),2))
	return min(5,max(exp/float(expErr),-5)) if exp is not 0 else 0
