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

	def update(self,ignored):
		self.value = self.cuts

class cutsDouble(wrappedChain.calculable):
	cuts = []
	cuts.append(cut('pt1',min=40))
	cuts.append(cut('pt2',min=40))
	cuts.append(cut('hasVtx',value=True))
	cuts.append(cut('glxyrmsvtx',max=0.5))
	cuts.append(cut('nAvgMissHitsAfterVert',max=2.))
	cuts.append(cut('posip2dFrac',min=0.7))
	cuts.append(cut('vtxN',min=3.5))
	#cuts.append(cut('vtxpt',min=15))
	cuts.append(cut('vtxmass',min=10))
	cuts.append(cut('Promptness',max=0.55))
	cuts.append(cut('lxysig',min=8.))

	def update(self,ignored):
		self.value = self.cuts
