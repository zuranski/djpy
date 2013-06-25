from supy import wrappedChain
from utils import DeltaR,p,MatchByDR

class jetVar(wrappedChain.calculable):
	fixes=('jet','')
	def update(self,ignored): self.value=[self.calculate(idx) for idx in self.source['jetIndices']]

class NeuFrac(jetVar):
	def calculate(self,idx):
		return self.source['jetNeuHadFrac'][idx]+self.source['jetPhFrac'][idx]

class ChgFrac(jetVar):
	def calculate(self,idx):
		return self.source['jetChgHadFrac'][idx]+self.source['jetEleFrac'][idx]+self.source['jetMuFrac'][idx]

class NeuN(jetVar):
	def calculate(self,idx):
		return self.source['jetNeuHadN'][idx]+self.source['jetPhN'][idx]

class ChgN(jetVar):
	def calculate(self,idx):
		return self.source['jetChgHadN'][idx]+self.source['jetEleN'][idx]+self.source['jetMuN'][idx]

class PtBias(jetVar):
	def update(self,ignored):
		pts = self.source['jetPt']
		chgs = self.source['jetChgFrac']
		neus = self.source['jetNeuFrac']
		self.value = [pt*(1.05*chg + 0.95*neu) for pt,chg,neu in zip (pts,chgs,neus)]

class PtGeom(jetVar):
	def calculate(self,idx):
		return self.source['jetPt'][idx]*self.source['jetgenjetCorr'][idx]

class genjetDR(jetVar):
	def calculate(self,idx):
		return DeltaR(
      				  self.source['jetEta'][idx],
				      self.source['jetPhi'][idx],
				      self.source['jetgenjetEta'][idx],
				      self.source['jetgenjetPhi'][idx]
			         ) 

class genjetPtDiff(jetVar):
	def calculate(self,idx):
		return (self.source['jetPt'][idx]-self.source['jetgenjetPt'][idx])/self.source['jetgenjetPt'][idx]

class genjetEnergyDiff(jetVar):
	def calculate(self,idx):
		return (self.source['jetEnergy'][idx]-self.source['jetgenjetEnergy'][idx])/self.source['jetgenjetEnergy'][idx]

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
	fixes=('jetgenjet','')
	def update(self,ignored):
		self.value = [self.source['genjet'+self.var][self.source['jetgenjetMatch'][i]] 
					  if self.source['jetgenjetMatch'][i] is not None else -999 for i in self.source['jetIndices']]

class Eta(jetgenjet): var='Eta'
class Phi(jetgenjet): var='Phi'
class Pt(jetgenjet): var='Pt'
class Energy(jetgenjet):	var='Energy'
class Lxy(jetgenjet): var='Lxy'
class Angle(jetgenjet): var='Angle'
class Corr(jetgenjet): var='Corr'
class DeltaR(jetgenjet): var='DeltaR'

# very special case
class N(jetgenjet):
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
