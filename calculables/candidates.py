from supy import wrappedChain
from utils import *
from functions import *

class candsSingle (wrappedChain.calculable):
	def update(self,ignored):		
		candsSingle = []
		for cand in self.source['pfjets']:
			if len(self.source['gjets'])>0:
				if cand.truelxy < 0 : continue
			vtxFeatures(cand)
			tracksFeatures(cand)
			tracksClusters(cand)
			passes(cand,self.source['cutsSingle'])
			candsSingle.append(cand)
		self.value = candsSingle

class candsDouble (wrappedChain.calculable):
	def update (self,ignored):
		candsDouble = []
 		for cand in self.source['pfjetpairs']:
			if len(self.source['gjets'])>0:
				if cand.truelxy < 0 : continue
			jet1 = self.source['pfjets'][cand.idx1]
			jet2 = self.source['pfjets'][cand.idx2]
			doubleFeatures(cand,jet1,jet2)
			groupTracks(cand,jet1,jet2)
			vtxFeatures(cand)
			tracksFeatures(cand)
			passes(cand,self.source['cutsDouble'])
			candsDouble.append(cand)
		self.value = candsDouble
