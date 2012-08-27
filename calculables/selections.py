from supy import wrappedChain
from functions import selected

# DOUBLE CANDIDATES
class doubleVeryLooseCuts(wrappedChain.calculable):
	cuts = ['hasVtx','glxydistclr']
	def update(self,ignored):
		self.value = self.cuts

class doubleLooseCuts(wrappedChain.calculable):
	cuts = [
	'pt1',
	'pt2',
	'hasVtx',
	'nAvgMissHitsAfterVert',
	'posip2dFrac',
	'vtxpt',
	'vtxmass',
	'vtxN',
	'vtxSameSign',
	]
	def update(self,ignored):
		self.value = self.cuts

class doubleTightCuts(wrappedChain.calculable):
	cuts = [
	'pt1',
	'pt2',
	'hasVtx',
	#'glxyrmsvtx',
	'nAvgMissHitsAfterVert',
	'posip2dFrac',
	'vtxpt',
	'vtxmass',
	'vtxN',
	'vtxSameSign',
	#'Promptness',
	#'lxysig',
	]
	def update(self,ignored):
		self.value = self.cuts

class doubleDiscCuts(wrappedChain.calculable):
	cuts = ['discvtxQual','discpromptness','disckin'] 
	def update(self,ignored):
		self.value = self.cuts

class doubleVeryLoose(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['doubleVeryLooseCuts'],self.source['candsDouble'])

class doubleLoose(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['doubleLooseCuts'],self.source['candsDouble'])

class doubleTight(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['doubleTightCuts'],self.source['candsDouble'])

class doubleDisc(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['doubleDiscCuts'],self.source['candsDoubleDisc'])

# SINGLE CANDIDATES
class singleLooseCuts(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = self.cuts

class singleTightCuts(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = self.cuts

class singleLoose(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['singleLooseCuts'],self.source['candsSingle'])

class singleTight(wrappedChain.calculable):
	def update(self,ignored):
		self.value = selected(self.source['singleTightCuts'],self.source['candsSingle'])
