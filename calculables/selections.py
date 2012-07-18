from supy import wrappedChain,analysisStep
from functions import selected

class singleTight(wrappedChain.calculable,analysisStep):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class doubleTight(wrappedChain.calculable):
	cuts = ['PromptEnergyFrac','hasVtx','vtxN','posip2dFrac','vtxNRatio','glxydistvtx','vtxN','vtxpt','lxysig']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

class singleLoose(wrappedChain.calculable):
	cuts = ['nPrompt','PromptEnergyFrac','hasVtx','vtxSameSign']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsSingle'])

class doubleLoose(wrappedChain.calculable):
	cuts = ['PromptEnergyFrac','hasVtx','vtxN','posip2dFrac']
	def update(self,ignored):
		self.value = selected(self.cuts,self.source['candsDouble'])

