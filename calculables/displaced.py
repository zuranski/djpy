from supy import wrappedChain

class dispPfJets (wrappedChain.calculable):
	def update(self,ignored):
		dispPfJets = []
		for pfjet in self.source['pfjets']:
			if pfjet.nPrompt >= 5 : continue
			if pfjet.PromptEnergyFrac > 0.2 : continue
			if pfjet.lxy == -1 : continue
			dispPfJets.append(pfjet)
		self.value = dispPfJets

class dispPfJetPairs (wrappedChain.calculable):
	def update (self,ignored):
		dispPfJetPairs = []
 		for pfjetpair in self.source['pfjetpairs']:
			pfjet1 = self.source['pfjets'][pfjetpair.idx1]
			pfjet2 = self.source['pfjets'][pfjetpair.idx2]
			if pfjet1.nPrompt >=5 or pfjet2.nPrompt >=5 : continue
			if pfjet1.PromptEnergyFrac > 0.2 or pfjet2.PromptEnergyFrac > 0.2 : continue
			if pfjetpair.lxy == -1 : continue
			dispPfJetPairs.append(pfjetpair)
		self.value = dispPfJetPairs
