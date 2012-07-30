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

class abcd_PromptEnergyFrac_glxyrmsclr(abcd):
	cutpair = ['PromptEnergyFrac','glxyrmsclr']
		
class abcd_PromptEnergyFrac_posip2dFrac(abcd):
	cutpair = ['PromptEnergyFrac','posip2dFrac']

class abcd_PromptEnergyFrac_lxysig(abcd):
	cutpair = ['PromptEnergyFrac','lxysig']

class abcd_PromptEnergyFrac_vtxNRatio(abcd):
	cutpair = ['PromptEnergyFrac','vtxNRatio']

class abcd_PromptEnergyFrac_vtxpt(abcd):
	cutpair = ['PromptEnergyFrac','vtxpt']

class abcd_PromptEnergyFrac_vtxmass(abcd):
	cutpair = ['PromptEnergyFrac','vtxmass']
