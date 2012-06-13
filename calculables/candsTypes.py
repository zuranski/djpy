from supy import wrappedChain

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

class dispSingle(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','-hasNuclearInt']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class dispDouble(wrappedChain.calculable):
	cuts = ['nPrompt1','nPrompt2','PromptEnergyFrac','hasVtx','-hasNuclearInt']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class nuclSingle(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','-hasV0','hasNuclearInt']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class nuclDouble(wrappedChain.calculable):
	cuts = ['nPrompt1','nPrompt2','PromptEnergyFrac','hasVtx','-hasV0','hasNuclearInt']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

