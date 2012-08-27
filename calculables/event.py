from supy import wrappedChain

class PfHt (wrappedChain.calculable):
	def update(self,ignored):
		ht = 0
                try:
	 		for jet in self.source["singlejets"]:
				ht += jet.pt	
                except KeyError: pass
		self.value = ht

class nPfJets (wrappedChain.calculable):
	def update(self,ignored):
		try:
			self.value = len(self.source["singlejets"])
		except KeyError:
			self.value = 0
