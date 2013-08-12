from supy import wrappedChain
from utils import MatchByDR

# matching jets to trigger objects
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

# matching trigger objects to gen quarks
class TrigPromptGenQ(wrappedChain.calculable):
	def __init__(self,tag='',instance=''):
		self.tag = tag
		self.fixes = ('',instance)

	def update(self,ignored):
		etas, phis = [],[]
		for idx in range(len(self.source['trgobjTag'])):
			if self.source['trgobjTag'][idx] == self.tag : 
				etas.append(self.source['trgobjEta'][idx])
				phis.append(self.source['trgobjPhi'][idx])
		
		matches = MatchByDR(etas,
							phis,
							self.source['genqEta'],
                            self.source['genqPhi'],
                            0.5)
		self.value = [self.source['genqFlavor'][matches[i]] if matches[i] is not None else None for i in range(len(matches))]
		#optional veto on muons
		#self.value = [a for a in self.value if a != 13]
