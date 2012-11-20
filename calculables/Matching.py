from supy import wrappedChain
from utils import MatchByDR

class jetTrueLxy(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['genjetPt']) == 0: 
			self.value = [True for i in range(len(self.source['jetPt']))]
			return
		matches = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genjetEta'],
							self.source['genjetPhi'], 0.3)
		self.value = [(self.source['genjetLxy'][matches[i]] if matches[i] is not None else -1)
					  for i in range(len(matches))]

class dijetTrueLxy(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['genjetPt']) == 0: 
			self.value = [True for i in range(len(self.source['dijetPt']))]
			return
		self.value = [self.source['jetTrueLxy'][self.source['dijetIdx1'][i]] 
                      if self.source['jetTrueLxy'][self.source['dijetIdx1'][i]] ==
                      self.source['jetTrueLxy'][self.source['dijetIdx2'][i]] != -1 else -1
                      for i in range(len(self.source['dijetPt']))]

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
