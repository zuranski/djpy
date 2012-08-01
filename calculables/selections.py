from supy import wrappedChain
from functions import selected

class doubleAll(wrappedChain.calculable):
	cuts = ['hasVtx']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class doubleLoose(wrappedChain.calculable):
	cuts = [
	'pt1',
	'pt2',
	'hasVtx',
	'glxyrmsvtx',
	'nAvgMissHitsAfterVert',
	'posip2dFrac',
	'vtxpt',
	#'vtxmass',
	'vtxN',
	'lxysig',
	]
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class doubleTight(wrappedChain.calculable):
	cuts = [
	'pt1',
	'pt2',
	'hasVtx',
	'glxyrmsvtx',
	'nAvgMissHitsAfterVert',
	'posip2dFrac',
	'vtxpt',
	#'vtxmass',
	'vtxN',
	'Promptness',
	'lxysig',
	]
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class singleLoose(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class singleTight(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])
