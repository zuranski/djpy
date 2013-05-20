from supy import wrappedChain
from utils import DeltaR,p

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

class ksP(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [p(self.source['ksPt'][idx],self.source['ksEta'][idx]) for idx in self.source['ksIndices']]

class genjetPtDiff(jetVar):
	def calculate(self,idx):
		return (self.source['jetPt'][idx]-self.source['jetgenjetPt'][idx])/self.source['jetgenjetPt'][idx]

class genjetDR(jetVar):
	def calculate(self,idx):
		return DeltaR(
      				  self.source['jetEta'][idx],
				      self.source['jetPhi'][idx],
				      self.source['jetgenjetEta'][idx],
				      self.source['jetgenjetPhi'][idx]
			         ) 
