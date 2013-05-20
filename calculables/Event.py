from supy import wrappedChain

class PfHt(wrappedChain.calculable):
	def update(self,ignored):
		self.value = sum([pt for pt in self.source['jetPt']])

class nPfJets (wrappedChain.calculable):
	def update(self,ignored):
		self.value = len(self.source["jetPt"])
