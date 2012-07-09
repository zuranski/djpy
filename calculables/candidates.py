from supy import wrappedChain
from calcUtils import *
from candUtils import *

class candsSingle (wrappedChain.calculable):
	def extra(self,cand):
		cand.hasVtx = False
		if cand.lxy != -1 and cand.vtxchi2 < 5 :
			cand.hasVtx = True
		cand.vtxSameSign = False
		if cand.vtxN == abs(cand.vtxCharge):
			cand.vtxSameSign = True
		cand.vtxNRatio = -1
		if (cand.nPrompt + cand.nDispTracks)>0:
			cand.vtxNRatio = cand.vtxN/float(cand.nPrompt + cand.nDispTracks)

	def update(self,ignored):		
		candsSingle = []
		for cand in self.source['pfjets']:
			if len(self.source['gjets'])>0:
				if cand.truelxy < 0 : continue
			self.extra(cand)
			trackextra(cand)
			passes(cand,self.source['cutsSingle'])
			candsSingle.append(cand)
		self.value = candsSingle

class candsDouble (candsSingle):

	def groupTrks(self,cand):
		cand.vtxN1 = 0
		cand.vtxN2 = 0
		if not cand.hasVtx:
			return
		trks1 = self.source['pfjets'][cand.idx1].disptracks
		trks2 = self.source['pfjets'][cand.idx2].disptracks
		trks = cand.disptracks
		for trk in trks:
			if trk.vtxweight < 0.5 : continue	
			for trk1 in trks1:
				if abs(trk1.chi2-trk.chi2)<1e-5:
					cand.vtxN1 +=1
					break
			for trk2 in trks2:
				if abs(trk2.chi2-trk.chi2)<1e-5:
					cand.vtxN2 +=1
					break
		if cand.vtxN1 == 0 or cand.vtxN2 == 0:
			cand.hasVtx = False

	def extraDouble(self,cand):
		jet1 = self.source['pfjets'][cand.idx1]
		jet2 = self.source['pfjets'][cand.idx2]
		cand.dR = DeltaR(jet1,jet2)
		cand.dPhi = DeltaPhi(jet1,jet2)
		cand.nPrompt1 = jet1.nPrompt
		cand.nPrompt2 = jet2.nPrompt
		cand.PromptEnergyFrac1 = jet1.PromptEnergyFrac
		cand.PromptEnergyFrac2 = jet2.PromptEnergyFrac

	def update (self,ignored):
		candsDouble = []
 		for cand in self.source['pfjetpairs']:
			if len(self.source['gjets'])>0:
				if cand.truelxy < 0 : continue
			self.extra(cand)
			self.extraDouble(cand)
			self.groupTrks(cand)
			trackextra(cand)
			passes(cand,self.source['cutsDouble'])
			candsDouble.append(cand)
		self.value = candsDouble
