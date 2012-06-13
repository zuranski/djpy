from supy import wrappedChain

class candsSingle (wrappedChain.calculable):
	def extra(self,cand):
		cand.hasVtx = False
		if cand.lxy != -1 and cand.vtxchi2 < 10 :
			cand.hasVtx = True
		cand.trksInVtx = 0
		cand.hasNuclearInt = False
		cand.hasV0 = False
                for t in cand.disptracks:
                        if t.vtxweight > 0.1: cand.trksInVtx+=1
		if cand.trksInVtx == 2 and ((cand.vtxmass < 0.6 and cand.vtxmass>0.4) or (cand.vtxmass>0.9 and cand.vtxmass<1.3)):
			cand.hasV0 = True
		if cand.trksInVtx <= 3 and cand.vtxmass > 0.6 and cand.vtxmass < 3 and not cand.hasV0: 
			cand.hasNuclearInt = True

	def passes(self,cand,cuts):
		cand.passes = []
		for i in range(len(cuts)):
	                cut = cuts[i]
                        value = getattr(cand,cut.name)
                        if value > cut.min and value < cut.max:
				cand.passes.append(cut.name)
			else:
				cand.passes.append('-'+cut.name)

	def update(self,ignored):		
		candsSingle = []
		for cand in self.source['pfjets']:
			self.extra(cand)
			self.passes(cand,self.source['cutsSingle'])
			candsSingle.append(cand)
		self.value = candsSingle

class candsDouble (candsSingle):
	def update (self,ignored):
		candsDouble = []
 		for cand in self.source['pfjetpairs']:
			cand.nPrompt1 = self.source['pfjets'][cand.idx1].nPrompt
			cand.nPrompt2 = self.source['pfjets'][cand.idx2].nPrompt
			self.extra(cand)
			self.passes(cand,self.source['cutsDouble'])
			candsDouble.append(cand)
		self.value = candsDouble
