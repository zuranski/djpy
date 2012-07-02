from calcUtils import *

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

def trackextra(cand):
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
			
