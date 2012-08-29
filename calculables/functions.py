from utils import *

def passed(cutNames,cand):
	for cutName in cutNames:
		try:
			cand.passes.index(cutName)
		except ValueError:
			return False
	return True

def selected(cutNames,collection):
	selected = []
	for cand in collection:
		if passed(cutNames,cand): selected.append(cand)
	return selected

def passes(cand,cuts):
	cand.passes = []
	for i in range(len(cuts)):
                cut = cuts[i]
                value = getattr(cand,cut.name)

		passedValue = False
		passedMin = False
		passedMax = False

		if cut.value is None: passed = passedValue = True
		if cut.min is None: passed = passedMin = True
		if cut.max is None: passed = passedMax = True

		if cut.value is not None and value == cut.value: passedValue = True
		if cut.min is not None and value > cut.min: passedMin = True
		if cut.max is not None and value < cut.max: passedMax = True

		passed = passedValue and passedMin and passedMax
		
                if passed:
			cand.passes.append(cut.name)
		else:
			cand.passes.append('-'+cut.name)

def myJetID(jet):
	if jet.PromptEnergyFrac > 1: return False
	if jet.muFrac>0.8: return False
	if jet.eleFrac>0.9: return False
	return True

def groupTracks(cand,jet1,jet2):
	cand.vtxN1 = 0
	cand.vtxN2 = 0
	trks1 = jet1.disptracks
	trks2 = jet2.disptracks
	trks = cand.disptracks
	for trk in trks:
		if trk.vtxweight < 0.5 : continue	
		for trk1 in trks1:
			if abs(trk1.chi2-trk.chi2)<1e-5:
				cand.vtxN1 +=1
				break
		for trk2 in trks2:
			if abs(trk2.chi2-trk.chi2)<1e-5:
				cand.vtxN2 +=1
				break


def doubleFeatures(cand,jet1,jet2):
	cand.dR = DeltaR(jet1,jet2)
	cand.dPhi = DeltaPhi(jet1,jet2)
	cand.nPrompt1 = jet1.nPrompt
	cand.nPrompt2 = jet2.nPrompt
	cand.PromptEnergyFrac1 = jet1.PromptEnergyFrac
	cand.PromptEnergyFrac2 = jet2.PromptEnergyFrac
	cand.pt1 = jet1.pt
	cand.pt2 = jet2.pt

def vtxFeatures(cand):

	# good vertex
	cand.hasVtx = False
	if cand.lxy != -1 and cand.vtxchi2 < 5 and cand.vtxN >= 2:
		cand.hasVtx = True
	try:
		if cand.vtxN1 == 0 or cand.vtxN2 == 0 :
			cand.hasVtx = False
	except AttributeError:
		pass
	# same sign vertex
	cand.vtxSameSign = False
	if cand.vtxN == abs(cand.vtxCharge):
		cand.vtxSameSign = True
	# vertexed ratio
	cand.vtxNTotRatio = -1
	cand.vtxNRatio = -1
	if (cand.nDispTracks+cand.nPrompt)>0:
		cand.vtxNTotRatio = cand.vtxN/float(cand.nDispTracks+cand.nPrompt)
	if cand.nDispTracks>0:
		cand.vtxNRatio = cand.vtxN/float(cand.nDispTracks)
	cand.vtxptRatio = cand.vtxpt/float(cand.pt)

def mcdRSingle(cand,gjets):
	dR=1e5
	truelxy = -1
	for gjet in gjets:
	    dR_i = DeltaR(gjet,cand)
	    if dR_i < dR and dR_i < 0.3:
		dR = dR_i
		truelxy = gjet.lxy
	return truelxy
	
def mcdRDouble(cand1,cand2,gjets):
	truelxy1 = mcdRSingle(cand1,gjets)
	truelxy2 = mcdRSingle(cand2,gjets)
	return truelxy1 if truelxy1==truelxy2 else -1

def mcTracksFromExo(cand):
	nFromExo = 0
	for t in cand.disptracks:
		if t.vtxweight<0.5 : continue
		if t.exo == 6000111 or t.exo == 6000112: nFromExo+=1
	return nFromExo/float(cand.vtxN) if cand.vtxN>0 else 0

def mcmatchSingle(cand,gjets):
	cand.truelxy = mcdRSingle(cand,gjets)
	cand.ExoVtxFrac = mcTracksFromExo(cand)

def mcmatchDouble(cand,cand1,cand2,gjets):
	cand.truelxy = mcdRDouble(cand1,cand2,gjets)
	cand.ExoVtxFrac = mcTracksFromExo(cand)

def tracksIPs(cand):

	import math
	cand.nposip2d = 0
	cand.posip2dFrac = 0
	cand.nposip3d = 0
	cand.posip3dFrac = 0
	for t in cand.disptracks:
		if t.ip2d > 0 and t.vtxweight>0.5:
			cand.nposip2d += 1
		if t.ip3d > 0 and t.vtxweight>0.5:
			cand.nposip3d += 1
	if len(cand.disptracks)>0 and cand.hasVtx:
		cand.posip2dFrac = cand.nposip2d/float(cand.vtxN)
		cand.posip3dFrac = cand.nposip3d/float(cand.vtxN)

def guesslxys(cand):
	import math
	for t in cand.disptracks:
		dphi = t.phi - cand.phi
		r = 330*t.pt/3.8
		d = abs(t.ip2d)
		a1 = -1 + (3*math.pow(math.sin(dphi),2)-1)/2*math.pow(math.sin(dphi),3)
		a2 = (3*math.pow(math.sin(dphi),2)-1)/2*math.pow(math.sin(dphi),3)
		if (dphi*t.charge)>0:
			t.guesslxy = t.ip2d/math.sin(dphi)*(1+a1*d/r + a2*d*d/r/r)
		else:
			t.guesslxy = t.ip2d/math.sin(dphi)*(1-a1*d/r - a2*d*d/r/r)

def tracksLxys(cand):

	cand.nguessed = 0
	cand.guessedFrac = 0
	for t in cand.disptracks:
		if abs(t.guesslxy) < 1.4*cand.lxy and abs(t.guesslxy) > 0.6*cand.lxy:
			cand.nguessed+=1
	if len(cand.disptracks)>0:
		cand.guessedFrac = cand.nguessed/float(len(cand.disptracks))

	all_lxys = [abs(t.guesslxy) for t in cand.disptracks]
	all_chi2s = [1/t.chi2 for t in cand.disptracks]
	vtx_lxys = [abs(t.guesslxy) for t in cand.disptracks if t.vtxweight>0.5]
	vtx_chi2s = [1/t.chi2 for t in cand.disptracks if t.vtxweight>0.5]

	cand.glxyrmsall = StDev(all_lxys,center=cand.lxy)
	cand.glxydistall = AvgDistance(all_lxys,weights=all_chi2s,center=cand.lxy)
	cand.glxyrmsvtx = StDev(vtx_lxys,center=cand.lxy)
	cand.glxydistvtx = AvgDistance(vtx_lxys,weights=vtx_chi2s,center=cand.lxy)

def tracksHits(cand):
	cand.nHitsBefVert = 0
	cand.nMissHitsAfterVert = 0
	cand.nAvgHitsBefVert = 1e10
	cand.nAvgMissHitsAfterVert = 1e10
	for t in cand.disptracks:
		if t.vtxweight<0.5: continue
		cand.nHitsBefVert += t.nHitsInFrontOfVert
		cand.nMissHitsAfterVert += t.nMissHitsAfterVert
	if cand.hasVtx:
		cand.nAvgHitsBefVert = cand.nHitsBefVert/float(cand.vtxN)
		cand.nAvgMissHitsAfterVert = cand.nMissHitsAfterVert/float(cand.vtxN)

def tracksClusters(cand):
	glxys = [abs(t.guesslxy) for t in cand.disptracks]
	cand.clusters = MakeClusters(glxys,0.15*cand.lxy)

	cand.bestclusterN = 0
	cand.bestclusterlxy = 1e10
	cand.glxyrmsclr = 1e10
	cand.glxydistclr = 1e10

	for cluster in cand.clusters:
		lxys = [abs(cand.disptracks[i].guesslxy) for i in cluster]
		chi2s = [1/cand.disptracks[i].chi2 for i in cluster]
		dist = abs(Avg(lxys,chi2s) - cand.lxy)/cand.lxy
		if dist < cand.bestclusterlxy:
			cand.bestclusterN = len(cluster)
			cand.bestclusterlxy = dist
			cand.glxyrmsclr = StDev(lxys,center=cand.lxy)
			cand.glxydistclr = AvgDistance(lxys,weights=chi2s,center=cand.lxy)

def tracksFeatures(cand):
	guesslxys(cand)
	tracksClusters(cand)
	tracksIPs(cand)
	tracksLxys(cand)
	tracksHits(cand)
