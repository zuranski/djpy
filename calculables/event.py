from supy import wrappedChain

class CaloHt (wrappedChain.calculable):
	def update(self,ignored):
		ht = 0
		for pt in self.source["jpt"]:
			ht += pt		
		self.value = ht

class nCaloJets (wrappedChain.calculable):
	def update(self,ignored):
		self.value = len(self.source["jpt"])

class PfHt (wrappedChain.calculable):
	def update(self,ignored):
		ht = 0
                try:
	 		for pfjet in self.source["pfjets"]:
				ht += pfjet.pt	
                except KeyError: pass
		self.value = ht

class nPfJets (wrappedChain.calculable):
	def update(self,ignored):
		try:
			self.value = len(self.source["pfjets"])
		except KeyError:
			self.value = 0
