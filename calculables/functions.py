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
	cand.Prompt = True
	if cand.PromptEnergyFrac1<0.2 and cand.PromptEnergyFrac2<0.2 and cand.nPrompt1<5 and cand.nPrompt2<5:
		cand.Prompt=False

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
	if (cand.nDispTracks+cand.nPrompt)>0:
		cand.vtxNRatio = cand.vtxN/float(cand.nDispTracks+cand.nPrompt)

def tracksIPs(cand):
	import math
	cand.nposip2d = 0
	cand.posip2dFrac = 0
	cand.nposip3d = 0
	cand.posip3dFrac = 0
	for t in cand.disptracks:
		if t.ip2d > 0:
			cand.nposip2d += 1
		if t.ip3d > 0:
			cand.nposip3d += 1
	if len(cand.disptracks)>0:
		cand.posip2dFrac = cand.nposip2d/float(len(cand.disptracks))
		cand.posip3dFrac = cand.nposip3d/float(len(cand.disptracks))

def tracksLxys(cand):
	cand.nguessed = 0
	cand.guessedFrac = 0
	for t in cand.disptracks:
		if abs(t.guesslxy) < 1.4*cand.lxy and abs(t.guesslxy) > 0.6*cand.lxy:
			cand.nguessed+=1
	if len(cand.disptracks)>0:
		cand.guessedFrac = cand.nguessed/float(len(cand.disptracks))
	all_lxys = [abs(t.guesslxy) for t in cand.disptracks]
	all_pts = [t.pt for t in cand.disptracks]
	vtx_lxys = [abs(t.guesslxy) for t in cand.disptracks if t.vtxweight>0.5]
	vtx_pts = [t.pt for t in cand.disptracks if t.vtxweight>0.5]
	cand.glxyrmsall = StDev(all_lxys,center=cand.lxy)
	cand.glxydistall = AvgDistance(all_lxys,weights=all_pts,center=cand.lxy)
	cand.glxyrmsvtx = StDev(vtx_lxys,center=cand.lxy)
	cand.glxydistvtx = AvgDistance(vtx_lxys,weights=vtx_pts,center=cand.lxy)
	
def tracksClusters(cand):
	# sort tracks based on guesslxy in ascending order
	def abslxy(t):
		return abs(t.guesslxy)
	tracks = [t for t in cand.disptracks]
	tracks.sort(key=abslxy)

	# make clusters
	clusters = []
	cluster = []
	for i in range(len(tracks)-1):
		a = (tracks[i].guesslxy)
		b = (tracks[i+1].guesslxy)
		dist = (b-a)*2/(b+a)
	        if dist < 0.15:
        	        if len(cluster) == 0:
                	        cluster.append(i)
                        	cluster.append(i+1)
	                else:
        	                cluster.append(i+1)
	        else:
			if len(cluster)>0: clusters.append(cluster)
                	cluster = []
	if len(cluster)>0: clusters.append(cluster)
	cand.clusters = clusters

	maxcluster = []
	length = 0
	for cluster in clusters:
		if len(cluster)>length:
			length = len(cluster)
			maxcluster = cluster		
	cand.maxclusterN = len(maxcluster)
	if len(maxcluster) == 0 :
		cand.maxclusterlxy = -1
		cand.glxyrmsclr = -1
		cand.glxydistclr = -1
	else:
		clr_lxys = []
		clr_pts = []
		lxy = 0
		pt = 0
		for i in maxcluster:
			clr_lxys.append(abs(tracks[i].guesslxy))
			clr_pts.append(tracks[i].pt)
			lxy += abs(tracks[i].guesslxy)*tracks[i].pt
			pt += tracks[i].pt
		cand.maxclusterlxy = lxy/pt
		cand.glxyrmsclr = StDev(clr_lxys,center=cand.lxy)
		cand.glxydistclr = AvgDistance(clr_lxys,weights=clr_pts,center=cand.lxy)

def tracksFeatures(cand):
	tracksClusters(cand)
	tracksIPs(cand)
	tracksLxys(cand)
