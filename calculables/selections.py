from supy import wrappedChain,analysisStep

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

class singleTight(wrappedChain.calculable,analysisStep):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class doubleTight(wrappedChain.calculable):
	cuts = ['nPrompt1','nPrompt2','PromptEnergyFrac1','PromptEnergyFrac2','hasVtx','vtxSameSign','posip2dFrac','posip3dFrac','guessedFrac','guesslxyrms','vtxNRatio','vtxN','vtxpt','lxysig']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class singleLoose(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class doubleLoose(wrappedChain.calculable):
	cuts = ['nPrompt1','nPrompt2','PromptEnergyFrac1','PromptEnergyFrac2','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

