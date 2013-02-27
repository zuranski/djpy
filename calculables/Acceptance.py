from supy import wrappedChain
from utils import DeltaR

class genjet1Indices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['genjetCtau1']))]

class genjet2Indices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['genjetCtau2']))]

class gendijet(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[]
		lxy=self.source['genqLxy']
		N=len(self.source['genqLxy'])
		for i in range(N-1):
			for j in range(i+1,N):
				if lxy[i]==lxy[j] : self.value.append((i,j))

class gendijetIndices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['gendijet']))]

class gendijetLxy(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genqLxy'][pair[0]] for pair in self.source['gendijet']]

class gendijetPt1(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genqPt'][pair[0]] for pair in self.source['gendijet']]

class gendijetPt2(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [self.source['genqPt'][pair[1]] for pair in self.source['gendijet']]

class gendijetEta1(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [abs(self.source['genqEta'][pair[0]]) for pair in self.source['gendijet']]

class gendijetEta2(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [abs(self.source['genqEta'][pair[1]]) for pair in self.source['gendijet']]

class gendijetDR(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [DeltaR(self.source['genqEta'][pair[0]],
							 self.source['genqPhi'][pair[0]],
							 self.source['genqEta'][pair[1]],
							 self.source['genqPhi'][pair[1]]) for pair in self.source['gendijet']]
