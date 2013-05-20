from supy import wrappedChain
from utils import MatchByDR

class jetTrueMatch(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genqEta'],
							self.source['genqPhi'],0.5) 

class jetTrue(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value=[self.source[self.var][self.source['jetTrueMatch'][i]]
                    if self.source['jetTrueMatch'][i] is not None else None for i in self.source['jetIndices']]

class dijetTrue(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['dijetIndices']]
			return
		self.value = [(self.source[self.var][self.source['dijetIdx1'][i]] +
		              self.source[self.var][self.source['dijetIdx2'][i]])/2.
                      if self.source['jetTrueLxy'][self.source['dijetIdx1'][i]] ==
                      self.source['jetTrueLxy'][self.source['dijetIdx2'][i]] != None else None
                      for i in self.source['dijetIndices']]

class jetTrueLxy(jetTrue): var='genqLxy'
class jetTrueCtau(jetTrue): var='genqCtau'
class jetTrueFlavor(jetTrue): var='genqFlavor'
class jetTrueNLep(jetTrue):	var='genqNLep'
class jetTrueBlxyz(jetTrue): var='genqBlxyz'

class dijetTrueLxy(dijetTrue): var='jetTrueLxy'
class dijetTrueCtau(dijetTrue):	var='jetTrueCtau'
class dijetTrueFlavor(dijetTrue): var='jetTrueFlavor'
class dijetTrueNLep(dijetTrue):	var='jetTrueNLep'
class dijetTrueBlxyz(dijetTrue): var='jetTrueBlxyz'

