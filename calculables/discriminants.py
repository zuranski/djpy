from supy import wrappedChain

class doublePromptEnergyFrac(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.PromptEnergyFrac for cand in self.source['doubleVeryLoose']]

class doublenPrompt(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.nPrompt for cand in self.source['doubleVeryLoose']]

class doublevtxN(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.vtxN for cand in self.source['doubleVeryLoose']]

class doublenAvgMissHitsAfterVert(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.nAvgMissHitsAfterVert for cand in self.source['doubleVeryLoose']]

class doubleposip2dFrac(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.posip2dFrac for cand in self.source['doubleVeryLoose']]

class doublevtxpt(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.vtxpt for cand in self.source['doubleVeryLoose']]

class doublevtxptRatio(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.vtxptRatio for cand in self.source['doubleVeryLoose']]

class doublevtxmass(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.vtxmass for cand in self.source['doubleVeryLoose']]

class doubleglxydistclr(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.glxydistclr for cand in self.source['doubleVeryLoose']]

class doubleglxydistvtx(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.glxydistvtx for cand in self.source['doubleVeryLoose']]

class doublevtxNTotRatio(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.vtxNTotRatio for cand in self.source['doubleVeryLoose']]

class doublebestclusterN(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [cand.bestclusterN for cand in self.source['doubleVeryLoose']]
