from supy import wrappedChain
from utils import MatchByDR,mergeVectors

class genjet(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([self.source['genjet'+self.var+'1'],self.source['genjet'+self.var+'2']])

class genjetEta(genjet): var='Eta'
class genjetPhi(genjet): var='Phi'
class genjetPt(genjet): var='Pt'
class genjetEnergy(genjet):	var='Energy'
class genjetLxy(genjet): var='Lxy'
class genjetAngle(genjet): var='Angle'
class genjetCorr(genjet): var='Corr'

# special case
class genjetDeltaR(wrappedChain.calculable):
	def update(self,ignored):
		self.value=mergeVectors([ [self.source['gendijetDR'][0] for pt in self.source['genjetPt1']],
                                  [self.source['gendijetDR'][1] for pt in self.source['genjetPt2']] ])
