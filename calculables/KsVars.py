from supy import wrappedChain
from utils import p

class ksVar(wrappedChain.calculable):
	fixes=('ks','')
	def update(self,ignored): self.value=[self.calculate(idx) for idx in self.source['ksIndices']]

class P(ksVar):
	def calculate(self,idx):
		return p(self.source['ksPt'][idx],self.source['ksEta'][idx])
