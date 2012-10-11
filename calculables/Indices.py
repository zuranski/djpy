from supy import wrappedChain
from utils import passed

class jetIndices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['jetPt']))]

class dijetIndices(wrappedChain.calculable):
	def update(self,ignored):
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
		self.fixes=(cuts[0]['name']+'_'+cuts[1]['name']+'_'+cuts[2]['name']+'_','_'+cuts[0]['more']+'_'+cuts[1]['more']+'_'+cuts[2]['more'])

	def update(self,ignored):
		self.value = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[]}
		for idx in self.source[self.indices]:
			pass0 = passed(self.source[self.cuts[0]['name']][idx],self.cuts[0])
			pass1 = passed(self.source[self.cuts[1]['name']][idx],self.cuts[1])
			pass2 = passed(self.source[self.cuts[2]['name']][idx],self.cuts[2])
			if pass0 and not pass1 and not pass2 : self.value['A'].append(idx)
			if pass0 and not pass1 and pass2 :     self.value['B'].append(idx)
			if pass0 and pass1 and not pass2 :     self.value['C'].append(idx)
			if pass0 and pass1 and pass2 :         self.value['D'].append(idx)
			if not pass0 and not pass1 and not pass2 : self.value['E'].append(idx)
			if not pass0 and not pass1 and pass2 :     self.value['F'].append(idx)
			if not pass0 and pass1 and not pass2 :     self.value['G'].append(idx)
			if not pass0 and pass1 and pass2 :         self.value['H'].append(idx)
