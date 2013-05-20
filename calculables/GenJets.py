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

class jetgenjetMatch(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genjetEta'],
							self.source['genjetPhi'],0.15) 

class jetgenjet(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genjet'+self.var][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else None for i in self.source['jetIndices']]

class jetgenjetEta(jetgenjet): var='Eta'
class jetgenjetPhi(jetgenjet): var='Phi'
class jetgenjetPt(jetgenjet): var='Pt'
class jetgenjetEnergy(jetgenjet):	var='Energy'
class jetgenjetLxy(jetgenjet): var='Lxy'
class jetgenjetAngle(jetgenjet): var='Angle'
class jetgenjetCorr(jetgenjet): var='Corr'
class jetgenjetDeltaR(jetgenjet): var='DeltaR'

# very special case
class jetgenjetN(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[None for i in self.source['jetIndices']]

		belongsTo=[None for i in self.source['jetIndices']]
		for i in self.source['jetIndices']:
			# check if the jet is matched
			if self.source['jetgenjetMatch'][i] is None : continue
			# check from which X particle it comes [1]
			genEta=self.source['genjetEta'][self.source['jetgenjetMatch'][i]]
			belongsTo[i]=0 if genEta in self.source['genjetEta1'] else 1

		# count nGenJets for exo 1 and 2
		nGen1=sum([1 for pt in self.source['genjetPt1'] if pt>40 ]) 
		nGen2=sum([1 for pt in self.source['genjetPt2'] if pt>40 ]) 
		nGen=[nGen1,nGen2]
		# count nRecoJet matched for exo 1 and 2
		nReco=[belongsTo.count(0),belongsTo.count(1)]
		# if the two counts don't agree per X throw out
		for i,x in enumerate(belongsTo):
			if x is not None and nReco[x]==nGen[x]: self.value[i]=nReco[x]
