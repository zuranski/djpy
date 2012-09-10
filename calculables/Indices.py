from supy import wrappedChain
from utils import MatchByDR

class jetIndices(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['jetTrueLxy'] is not None:
			self.value = [i for i in range(len(self.source['jetPt']))
				          if self.source['jetTrueLxy'][i] is not -1 ]
		else:
			self.value = [i for i in range(len(self.source['jetPt']))]

class dijetIndices(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['jetTrueLxy'] is not None:
			self.value = [i for i in range(len(self.source['dijetPt']))
						  if self.source['jetTrueLxy'][self.source['dijetIdx1'][i]] ==
						  self.source['jetTrueLxy'][self.source['dijetIdx2'][i]] != -1 
						 ]
		else:
			self.value = [i for i in range(len(self.source['dijetPt']))]

class Indices(wrappedChain.calculable):
	def __init__(self,val=None,min=None,max=None,indices=''):
		for item in ['val','min','max','indices']: setattr(self,item,eval(item))

	def passed (self,var,min,max,val):
		passVal = (var == val) if val is not None else True
		passMin = (var >= min) if min is not None else True
		passMax = (var <= max) if max is not None else True
		return (passVal and passMin and passMax)

	def update(self,ignored):
		indicesOut = []
		indicesIn = self.source[self.indices]
		vars = self.source[self.coll]
		for idx in indicesIn:
			if self.passed(vars[idx],self.min,self.max,self.val): indicesOut.append(idx)
		self.value = indicesOut

class jetVtxChi2Indices(Indices):
	coll='jetVtxChi2'
class dijetVtxChi2Indices(Indices):
	coll='dijetVtxChi2'
class dijetVtxNIndices(Indices):
	coll='dijetVtxN'
class dijetVtxN1Indices(Indices):
	coll='dijetVtxN1'
class dijetVtxN2Indices(Indices):
	coll='dijetVtxN2'
class dijetVtxNTotRatioIndices(Indices):
	coll='dijetVtxNTotRatio'
class dijetbestclusterNIndices(Indices):
	coll='dijetbestclusterN'
class dijetPosip2dFracIndices(Indices):
	coll='dijetPosip2dFrac'
class dijetNAvgMissHitsAfterVertIndices(Indices):
	coll='dijetNAvgMissHitsAfterVert'
class dijetglxyrmsclrIndices(Indices):
	coll='dijetglxyrmsclr'
class dijetVtxptIndices(Indices):
	coll='dijetVtxpt'
class dijetVtxmassIndices(Indices):
	coll='dijetVtxmass'
class dijetNPromptTracksIndices(Indices):
	coll='dijetNPromptTracks'
class dijetPromptEnergyFracIndices(Indices):
	coll='dijetPromptEnergyFrac'
class dijetLxysigIndices(Indices):
	coll='dijetLxysig'
class dijetDiscriminantPromptnessIndices(Indices):
	coll='dijetDiscriminantPromptness'
class dijetDiscriminantVtxIndices(Indices):
	coll='dijetDiscriminantVtx'
