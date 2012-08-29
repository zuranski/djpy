from supy import wrappedChain
from utils import *
from functions import *

class candsSingle (wrappedChain.calculable):
	def update(self,ignored):		
		candsSingle = []
		for cand in self.source['singlejets']:
			if not myJetID(cand) : continue
			if not self.source['isRealData']:	
 				gjets = self.source['gjets']
				if len(gjets) > 0:
					mcmatchSingle(cand,self.source['gjets'])
					if cand.ExoVtxFrac < 0.95 or cand.truelxy < 0 : continue
			cand.Promptness = cand.nPrompt*cand.PromptEnergyFrac
			vtxFeatures(cand)
			tracksFeatures(cand)
			tracksClusters(cand)
			passes(cand,self.source['cutsSingle'])
			candsSingle.append(cand)
		self.value = candsSingle

class candsDouble (wrappedChain.calculable):
	def update (self,ignored):
		candsDouble = []
 		for cand in self.source['doublejets']:
			jet1 = self.source['singlejets'][cand.idx1]
			jet2 = self.source['singlejets'][cand.idx2]
			if not myJetID(jet1) : continue
			if not myJetID(jet2) : continue
			if not self.source['isRealData']:	
 				gjets = self.source['gjets']
				if len(gjets) > 0:
					mcmatchDouble(cand,jet1,jet2,self.source['gjets'])
					if cand.ExoVtxFrac < 0.95 or cand.truelxy < 0 : continue
			cand.Promptness = cand.nPrompt*cand.PromptEnergyFrac
			doubleFeatures(cand,jet1,jet2)
			groupTracks(cand,jet1,jet2)
			vtxFeatures(cand)
			tracksFeatures(cand)
			passes(cand,self.source['cutsDouble'])
			candsDouble.append(cand)
		self.value = candsDouble

class candsDoubleDisc(wrappedChain.calculable):
	def update(self,ignored):
		candsDoubleDisc = []
		try:
			for cand,discpromptness,disckin,discvtxQual in zip (self.source['doubleVeryLoose'],self.source['Discriminantpromptness'],self.source['Discriminantkin'],self.source['DiscriminantvtxQual']):
				cand.discpromptness = discpromptness
				cand.discvtxQual = discvtxQual
				cand.disckin = disckin
				passes(cand,self.source['cutsDoubleDisc'])
				candsDoubleDisc.append(cand)
		except TypeError: 
			pass 
		self.value = candsDoubleDisc
