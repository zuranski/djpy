from utils import *

def passes(cand,cuts):
	cand.passes = []
	for i in range(len(cuts)):
                cut = cuts[i]
                value = getattr(cand,cut.name)

		passedValue = False
		passedMin = False
		passedMax = False

		if cut.value is not None and value == cut.value: passedValue = True
		if cut.min is not None and value > cut.min: passedMin = True
		if cut.max is not None and value < cut.max: passedMax = True

		if cut.value is None: passed = passedValue = True
		if cut.min is None: passed = passedMin = True
		if cut.max is None: passed = passedMax = True
		
		passed = passedValue and passedMin and passedMax
		
                if passed:
			cand.passes.append(cut.name)
		else:
			cand.passes.append('-'+cut.name)

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

def vtxFeatures(cand):
	# good vertex
	cand.hasVtx = False
	if cand.lxy != -1 and cand.vtxchi2 < 5 :
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
	cand.vtxNRatio = -1
	if (cand.nPrompt + cand.nDispTracks)>0:
		cand.vtxNRatio = cand.vtxN/float(cand.nPrompt + cand.nDispTracks)

def tracksFeatures(cand):
	import math
	cand.guesslxyrms = -1
	cand.nguessed = 0
	cand.guessedFrac = 0
	cand.nposip2d = 0
	cand.posip2dFrac = 0
	cand.nposip3d = 0
	cand.posip3dFrac = 0
	stdevXY = 0
	n = 0
	for t in cand.disptracks:
		if abs(t.guesslxy) < 1.2*cand.lxy and abs(t.guesslxy)>0.8*cand.lxy:
			cand.nguessed += 1
		if t.ip2d > 0:
			cand.nposip2d += 1
		if t.ip3d > 0:
			cand.nposip3d += 1

		if t.vtxweight < 0.5: continue
		stdevXY += pow((abs(t.guesslxy) - cand.lxy)/cand.lxy,2)
		n+=1
	if n>1:
		cand.guesslxyrms = math.sqrt(stdevXY/n)/float(n)
	if len(cand.disptracks)>1:
		cand.guessedFrac = cand.nguessed/float(len(cand.disptracks))
		cand.posip2dFrac = cand.nposip2d/float(len(cand.disptracks))
		cand.posip3dFrac = cand.nposip3d/float(len(cand.disptracks))
			
