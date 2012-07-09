from supy import wrappedChain

# store cuts in a simple struct
class cut():
	name = None
	min = None
	max = None
	value = None
	
	def __init__(self,name,min=None,max=None,value=None):
		self.name = name
		self.min = min
		self.max = max
		self.value = value
	
	def rangeName(self):
		name = ''
		if self.value is not None: name = str(self.value)
		if self.min is not None: name += 'min='+str(self.min)
		if self.max is not None:
			if len(name)>0:
				 name += ','
			name += 'max='+str(self.max) 
		return name

# define cuts for single and double cands and store them in the event
class cutsSingle(wrappedChain.calculable):
	cuts = []
	cuts.append(cut('nPrompt',max=5))
	cuts.append(cut('PromptEnergyFrac',max=0.2))
	cuts.append(cut('hasVtx',value=True))
	cuts.append(cut('vtxSameSign',value=False))

	def update(self,ignored):
		self.value = self.cuts

class cutsDouble(wrappedChain.calculable):
	cuts = []
	cuts.append(cut('nPrompt1',max=5))
	cuts.append(cut('nPrompt2',max=5))
	cuts.append(cut('PromptEnergyFrac1',max=0.2))
	cuts.append(cut('PromptEnergyFrac2',max=0.2))
	cuts.append(cut('hasVtx',value=True))
	cuts.append(cut('vtxSameSign',value=False))
	cuts.append(cut('posip2dFrac',min=0.6))
	cuts.append(cut('posip3dFrac',min=0.6))
	cuts.append(cut('guessedFrac',min=0.01))
	cuts.append(cut('guesslxyrms',max=0.5))
	cuts.append(cut('vtxNRatio',min=0.34))
	cuts.append(cut('vtxN',min=2.5))
	cuts.append(cut('vtxpt',min=5.))
	cuts.append(cut('lxysig',min=8.))

	def update(self,ignored):
		self.value = self.cuts
