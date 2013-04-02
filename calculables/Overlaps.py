from supy import wrappedChain

class dijetNoOverlaps(wrappedChain.calculable):
	def __init__(self,indices=''):
		self.indices = indices

	def overlaps(self,cands):
		to_pop = []
		for i in range(len(cands)-1):
			for j in range(i+1,len(cands)):
				p1 = [cands[i]['1'],cands[i]['2']]
				p2 = [cands[j]['1'],cands[j]['2']]
				if len(set(p1).intersection(set(p2)))>0: 
					to_pop.append(cands[j]['idx'] if cands[i]['val']>cands[j]['val'] else cands[i]['idx'])
		return [a for a in set(to_pop)]

	def update(self,ingored):
		self.value = [-1 for i in range(len(self.source['dijetPt']))]
		cands = []
		for idx in self.source[self.indices]:
			cand = {}
			cand['1'] = self.source['dijetIdx1'][idx]
			cand['2'] = self.source['dijetIdx2'][idx]
			cand['val'] = self.source['dijetLxysig'][idx]
			cand['idx'] = idx
			cands.append(cand)
		indices_to_pop = self.overlaps(cands)
		good_indices = [i for i in self.source[self.indices] if i not in indices_to_pop]
		for i in good_indices: self.value[i]=True

class ksNoOverlaps(wrappedChain.calculable):
	def __init__(self,indices=''):
		self.indices = indices

	def overlaps(self,cands):
		to_pop = []
		for i in range(len(cands)-1):
			for j in range(i+1,len(cands)):
				p1 = [cands[i]['1'],cands[i]['2']]
				p2 = [cands[j]['1'],cands[j]['2']]
				if len(set(p1).intersection(set(p2)))>0: 
					to_pop.append(cands[j]['idx'] if cands[i]['val']>cands[j]['val'] else cands[i]['idx'])
		return [a for a in set(to_pop)]

	def update(self,ingored):
		self.value = [-1 for i in range(len(self.source['ksPt']))]
		cands = []
		for idx in self.source[self.indices]:
			cand = {}
			cand['1'] = self.source['ksTrk1Pt'][idx]
			cand['2'] = self.source['ksTrk2Pt'][idx]
			cand['val'] = -self.source['ksChi2'][idx]
			cand['idx'] = idx
			cands.append(cand)
		indices_to_pop = self.overlaps(cands)
		good_indices = [i for i in self.source[self.indices] if i not in indices_to_pop]
		for i in good_indices: self.value[i]=True
