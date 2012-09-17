from supy import wrappedChain

class ABCDIndices(wrappedChain.calculable):
	def __init__(self,cuts=({},{}),indices=''):
		for item in ['cuts','indices']: setattr(self,item,eval(item))

	def passed (self,var,cut):
		passVal = (var == cut['val']) if 'val' in cut else True
		passMin = (var >= cut['min']) if 'min' in cut else True
		passMax = (var <= cut['max']) if 'max' in cut else True
		return (passVal and passMin and passMax)

	def update(self,ignored):
		self.value = {'A':[],'B'[],'C':[],'D':[]}
		indicesIn = self.source[self.indices]
		for idx in self.source[self.indices]:
			pass1 = self.passed(self.source[self.coll1])
			if self.passed(vars[idx],self.cut): indicesOut.append(idx)
		self.value = indicesOut
