from supy import wrappedChain
from utils import MatchByDR

class jetTrueMatch(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['genjetPt']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genjetEta'],
							self.source['genjetPhi'],0.5) 

class jetTrueLxy(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[self.source['genjetLxy'][self.source['jetTrueMatch'][i]] 
                    if self.source['jetTrueMatch'][i] is not None else -1 for i in self.source['jetIndices']]

class jetTrueCtau(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[self.source['genjetCtau'][self.source['jetTrueMatch'][i]] 
                    if self.source['jetTrueMatch'][i] is not None else -1 for i in self.source['jetIndices']]

class dijetTrueLxy(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['genjetPt']) == 0: 
			self.value = [True for i in self.source['dijetIndices']]
			return
		self.value = [self.source['jetTrueLxy'][self.source['dijetIdx1'][i]]
                      if self.source['jetTrueLxy'][self.source['dijetIdx1'][i]] ==
                      self.source['jetTrueLxy'][self.source['dijetIdx2'][i]] != -1 else -1
                      for i in self.source['dijetIndices']]

class dijetTrueCtau(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['genjetPt']) == 0: 
			self.value = [True for i in self.source['dijetIndices']]
			return
		self.value = [self.source['jetTrueCtau'][self.source['dijetIdx1'][i]] 
                      if self.source['jetTrueCtau'][self.source['dijetIdx1'][i]] ==
                      self.source['jetTrueCtau'][self.source['dijetIdx2'][i]] != -1 else -1
                      for i in self.source['dijetIndices']]

class jetTrigPrompt(wrappedChain.calculable):
	def __init__(self,tag):
		self.tag = tag

	def update(self,ignored):
		etas, phis = [],[]
		for idx in range(len(self.source['trgobjTag'])):
			if self.source['trgobjTag'][idx] == self.tag : 
				etas.append(self.source['trgobjEta'][idx])
				phis.append(self.source['trgobjPhi'][idx])
		
		matches = MatchByDR(self.source['jetEta'],
                            self.source['jetPhi'],
                            etas,
                            phis,0.5)
		self.value = [True if matches[i] is not None else False for i in range(len(matches))]
