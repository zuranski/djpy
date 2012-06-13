from supy import wrappedChain

# store cuts in a simple struct
class cut():
	name = None
	min = None
	max = None	
	def __init__(self,name,min,max):
		self.name = name
		self.min = min
		self.max = max

# define cuts for single and double cands and store them in the event
class cutsSingle(wrappedChain.calculable):
	cuts = []
	cuts.append(cut('nPrompt',0,5))
	cuts.append(cut('PromptEnergyFrac',0,0.2))
	cuts.append(cut('hasVtx',0.5,1.5))
	cuts.append(cut('hasV0',0.5,1.5))
	cuts.append(cut('hasNuclearInt',0.5,1.5))

	def update(self,ignored):
		self.value = self.cuts

class cutsDouble(wrappedChain.calculable):
	cuts = []
	cuts.append(cut('nPrompt1',0,5))
	cuts.append(cut('nPrompt2',0,5))
	cuts.append(cut('PromptEnergyFrac',0,0.2))
	cuts.append(cut('hasVtx',0.5,1.5))
	cuts.append(cut('hasV0',0.5,1.5))
	cuts.append(cut('hasNuclearInt',0.5,1.5))

	def update(self,ignored):
		self.value = self.cuts
