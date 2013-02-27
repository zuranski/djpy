from supy import wrappedChain

class PfHt (wrappedChain.calculable):
	def update(self,ignored):
		ht = 0
                try:
	 		for pt in self.source["jetPt"]:
				ht += pt	
                except KeyError: pass
		self.value = ht

class mygenHT(wrappedChain.calculable):
	def update(self,ignored):
		ht=0
		try:
			for pt,eta in zip(self.source['genqPt'],self.source['genqEta']):
				if abs(eta)<3: ht+=pt
		except KeyError: pass
		self.value = ht

class nPfJets (wrappedChain.calculable):
	def update(self,ignored):
		try:
			self.value = len(self.source["jetPt"])
		except KeyError:
			self.value = 0
