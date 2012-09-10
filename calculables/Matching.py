from supy import wrappedChain
from utils import MatchByDR

class jetTrueLxy(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['isRealData'] : self.value = None; return
		if len(self.source['genjetPt']) == 0 : self.value = None; return
		matches = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genjetEta'],
							self.source['genjetPhi'], 0.3)
		self.value = [(self.source['genjetLxy'][matches[i]] if matches[i] is not None else -1)
					  for i in range(len(matches))]
