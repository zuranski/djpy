from supy import wrappedChain

class DijetVar(wrappedChain.calculable):
	def __init__(self,indices=None):
		self.indices = indices if indices is not None else 'dijetIndices'

	def update(self,ignored):
		self.value = [-1 for i in range(len(self.source['dijetPt']))]
		for idx in self.source[self.indices]:
			self.value[idx] = self.calculate(idx)

class dijetVtxNRatio(DijetVar):
	def calculate(self,idx):
		return self.source['dijetVtxN'][idx]/float(self.source['dijetNDispTracks'][idx])

class dijetVtxNTotRatio(DijetVar):
	def calculate(self,idx):
		return self.source['dijetVtxN'][idx]/float(self.source['dijetNDispTracks'][idx]
				+self.source['dijetNPromptTracks'][idx])

class dijetVtxptRatio(DijetVar):
	def calculate(self,idx):
		return self.source['dijetVtxpt'][idx]/float(self.source['dijetPt'][idx])
