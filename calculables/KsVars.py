from supy import wrappedChain
from utils import p

class ksVar(wrappedChain.calculale):
	fixes=('ks','')
	def update(self,ignored): self.value=[self.calculate(idx) for idx in self.source['jetIndices']

class P(ksVar):
	def calculate(self,idx):
		return p(self.source['ksPt'][idx],self.source['ksEta'][idx])
