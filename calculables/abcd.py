from supy import wrappedChain,analysisStep
from functions import selected

def cutsABCD(all_cuts,cutpair):
	cutNames = [cut.name for cut in all_cuts]
	for cut in cutpair: cutNames.remove(cut)
	cuts = {}
	cuts['A'] = cutNames + ['-'+cutpair[0],'-'+cutpair[1]] 
	cuts['B'] = cutNames + [cutpair[0],'-'+cutpair[1]] 
	cuts['C'] = cutNames + ['-'+cutpair[0],cutpair[1]] 
	cuts['D'] = cutNames + [cutpair[0],cutpair[1]] 
	cuts['plot'] = cutNames
	return cuts

def countsABCD(cuts,candidates):
	counts = {}
	counts['A'] = len(selected(cuts['A'],candidates))
	counts['B'] = len(selected(cuts['B'],candidates))
	counts['C'] = len(selected(cuts['C'],candidates))
	counts['D'] = len(selected(cuts['D'],candidates))
	return counts

class abcdObj():
	candidates = []
	counts = {}

class abcd(wrappedChain.calculable):
	cutpair = ['','']
	abcdObj = None
	def update(self,ignored):
		cuts = cutsABCD(self.source['cutsDouble'],self.cutpair)
		abcdObj.candidates = selected(cuts['plot'],self.source['candsDouble'])
		abcdObj.counts = countsABCD(cuts,self.source['candsDouble']) 
		self.value = abcdObj

		
class abcd_Promptness_glxyrmsvtx(abcd):
	cutpair = ['Promptness','glxyrmsvtx']

class abcd_Promptness_posip2dFrac(abcd):
	cutpair = ['Promptness','posip2dFrac']

class abcd_Promptness_vtxpt(abcd):
	cutpair = ['Promptness','vtxpt']

class abcd_Promptness_vtxmass(abcd):
	cutpair = ['Promptness','vtxmass']

class abcd_Promptness_vtxN(abcd):
	cutpair = ['Promptness','vtxN']

class abcd_Promptness_nAvgMissHitsAfterVert(abcd):
	cutpair = ['Promptness','nAvgMissHitsAfterVert']
