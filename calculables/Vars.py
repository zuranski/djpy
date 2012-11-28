from supy import wrappedChain
from utils import DeltaR

class DiJetVar(wrappedChain.calculable):
	def __init__(self,indices=None):
		self.indices = indices if indices is not None else 'dijetIndices'

	def update(self,ignored):
		self.value = [-1 for i in range(len(self.source['dijetPt']))]
		for idx in self.source[self.indices]:
			self.value[idx] = self.calculate(idx)

class JetVar(wrappedChain.calculable):
	def __init__(self,indices=None):
		self.indices = indices if indices is not None else 'jetIndices'

	def update(self,ignored):
		self.value = [-1 for i in range(len(self.source['jetPt']))]
		for idx in self.source[self.indices]:
			self.value[idx] = self.calculate(idx)

class jetPromptness(JetVar):
	def calculate(self,idx):
		return self.source['jetNPromptTracks'][idx]*self.source['jetPromptEnergyFrac'][idx]

class dijetVtxNRatio(DiJetVar):
	def calculate(self,idx):
		return self.source['dijetVtxN'][idx]/float(self.source['dijetNDispTracks'][idx]) if self.source['dijetNDispTracks'][idx] > 0 else -1

class dijetVtxDelta(DiJetVar):
	def calculate(self,idx):
		return abs(self.source['dijetVtxN1'][idx]-self.source['dijetVtxN2'][idx])/float(self.source['dijetVtxN'][idx])

class dijetVtxptRatio(DiJetVar):
	def calculate(self,idx):
		return self.source['dijetVtxpt'][idx]/float(self.source['dijetPt'][idx])

class dijetDR(DiJetVar):
	def calculate(self,idx):
		return DeltaR(
                      self.source['jetEta'][self.source['dijetIdx1'][idx]],
                      self.source['jetPhi'][self.source['dijetIdx1'][idx]],
                      self.source['jetEta'][self.source['dijetIdx2'][idx]],
                      self.source['jetPhi'][self.source['dijetIdx2'][idx]]
                     ) 

class dijetPromptness(DiJetVar):
	def calculate(self,idx):
		return self.source['dijetNPromptTracks'][idx]*self.source['dijetPromptEnergyFrac'][idx]

class dijetPromptness1(DiJetVar):
	def calculate(self,idx):
		return self.source['jetNPromptTracks'][self.source['dijetIdx1'][idx]]*self.source['jetPromptEnergyFrac'][self.source['dijetIdx1'][idx]]

class dijetPromptness2(DiJetVar):
	def calculate(self,idx):
		return self.source['jetNPromptTracks'][self.source['dijetIdx2'][idx]]*self.source['jetPromptEnergyFrac'][self.source['dijetIdx2'][idx]]

class dijetNPromptTracks1(DiJetVar):
	def calculate(self,idx):
		return self.source['jetNPromptTracks'][self.source['dijetIdx1'][idx]]

class dijetNPromptTracks2(DiJetVar):
	def calculate(self,idx):
		return self.source['jetNPromptTracks'][self.source['dijetIdx2'][idx]]

class dijetPromptEnergyFrac1(DiJetVar):
	def calculate(self,idx):
		return self.source['jetPromptEnergyFrac'][self.source['dijetIdx1'][idx]]

class dijetPromptEnergyFrac2(DiJetVar):
	def calculate(self,idx):
		return self.source['jetPromptEnergyFrac'][self.source['dijetIdx2'][idx]]

class dijetPt1(DiJetVar):
	def calculate(self,idx):
		return self.source['jetPt'][self.source['dijetIdx1'][idx]]

class dijetPt2(DiJetVar):
	def calculate(self,idx):
		return self.source['jetPt'][self.source['dijetIdx2'][idx]]
