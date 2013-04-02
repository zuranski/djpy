from supy import wrappedChain
from utils import passed

class jetIndices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['jetPt']))]

class dijetIndices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['dijetPt']))]

class ksIndices(wrappedChain.calculable):
	def update(self,ignored):
		self.value = [i for i in range(len(self.source['ksPt']))]

class Indices(wrappedChain.calculable):
	def __init__(self,cut={},indices='',tag=''):
		for item in ['cut','indices']: setattr(self,item,eval(item))
		self.fixes = (cut['name'],tag)

	def update(self,ignored):
		self.value = []
		for idx in self.source[self.indices]:
			if self.cut.has_key('vars'):
				if all(passed(self.source,idx,cut) for cut in self.cut['vars']) : self.value.append(idx)
			else :
				if passed(self.source,idx,self.cut): self.value.append(idx)

class ABCDIndices(wrappedChain.calculable):
	def __init__(self,cuts=[],indices='',prefix='',suffix=''):
		for item in ['cuts','indices']: setattr(self,item,eval(item))
		self.fixes=(prefix,suffix)

	def update(self,ignored):
		self.value = {'A':[],'B':[],'C':[],'D':[]}
		for idx in self.source[self.indices]:
			pass0 = all([passed(self.source,idx,cut) for cut in self.cuts[0]['vars']])
			pass1 = all([passed(self.source,idx,cut) for cut in self.cuts[1]['vars']])
			if not pass0 and not pass1 : self.value['A'].append(idx)
			if pass0 and not pass1 :     self.value['B'].append(idx)
			if not pass0 and pass1 :     self.value['C'].append(idx)
			if pass0 and pass1 :         self.value['D'].append(idx)

class ABCDEFGHIndices(wrappedChain.calculable):
	def __init__(self,cuts=[],indices='',prefix='',suffix=''):
		for item in ['cuts','indices']: setattr(self,item,eval(item))
		self.fixes=(prefix,suffix)

	def update(self,ignored):
		self.value = {'A':[],'B':[],'C':[],'D':[],'E':[],'F':[],'G':[],'H':[]}
		for idx in self.source[self.indices]:
			pass0 = all([passed(self.source,idx,cut) for cut in self.cuts[0]['vars']])
			pass1 = all([passed(self.source,idx,cut) for cut in self.cuts[1]['vars']])
			pass2 = all([passed(self.source,idx,cut) for cut in self.cuts[2]['vars']])
			if not pass0 and not pass1 and not pass2 : self.value['A'].append(idx)
			if pass0 and not pass1 and not pass2 :     self.value['B'].append(idx)
			if not pass0 and pass1 and not pass2 :     self.value['C'].append(idx)
			if not pass0 and not pass1 and pass2 :         self.value['D'].append(idx)
			if not pass0 and pass1 and pass2 : self.value['E'].append(idx)
			if pass0 and not pass1 and pass2 :     self.value['F'].append(idx)
			if pass0 and pass1 and not pass2 :     self.value['G'].append(idx)
			if pass0 and pass1 and pass2 :         self.value['H'].append(idx)

