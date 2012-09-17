from supy import wrappedChain
from utils import passed

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
	def __init__(self,cut={},indices=''):
		for item in ['cut','indices']: setattr(self,item,eval(item))
		self.fixes = (cut['name'],'')

	def update(self,ignored):
		self.value = []
		for idx in self.source[self.indices]:
			if passed(self.source[self.cut['name']][idx],self.cut): self.value.append(idx)

class ABCDIndices(wrappedChain.calculable):
	def __init__(self,cuts=[],indices=''):
		for item in ['cuts','indices']: setattr(self,item,eval(item))
		self.fixes=(cuts[0]['name']+'_'+cuts[1]['name']+'_','_'+cuts[0]['more']+'_'+cuts[1]['more'])

	def update(self,ignored):
		self.value = {'A':[],'B':[],'C':[],'D':[]}
		for idx in self.source[self.indices]:
			pass1 = passed(self.source[self.cuts[0]['name']][idx],self.cuts[0])
			pass2 = passed(self.source[self.cuts[1]['name']][idx],self.cuts[1])
			if not pass1 and not pass2 : self.value['A'].append(idx)
			if not pass1 and pass2 :     self.value['B'].append(idx)
			if pass1 and not pass2 :     self.value['C'].append(idx)
			if pass1 and pass2 :         self.value['D'].append(idx)
