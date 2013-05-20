from supy import wrappedChain
from utils import MatchByDR

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
