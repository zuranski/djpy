from supy import wrappedChain
from utils import MatchByDR,mergeVectors

class genjetEta(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([self.source['genjetEta1'],self.source['genjetEta2']])

class genjetPhi(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([self.source['genjetPhi1'],self.source['genjetPhi2']])

class genjetPt(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([self.source['genjetPt1'],self.source['genjetPt2']])

class genjetLxy(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([self.source['genjetLxy1'],self.source['genjetLxy2']])

class jetgenjetMatch(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genjetEta'],
							self.source['genjetPhi'],0.15) 

class jetgenjetPt(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genjetPt'][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else None for i in self.source['jetIndices']]

class jetgenjetLxy(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genjetLxy'][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else None for i in self.source['jetIndices']]

class jetgenjetEta(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genjetEta'][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else None for i in self.source['jetIndices']]

class jetgenjetPhi(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genjetPhi'][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else None for i in self.source['jetIndices']]
