from supy import wrappedChain

class countsSingle (wrappedChain.calculable):
	def getCounts(self,cuts,collection):
		counts = [0]*len(cuts)
                for cand in collection:
                        for i in range(len(cuts)):
				try:
					cand.passes.index(cuts[i].name)
					counts[i]+=1
				except ValueError: 
					break

                counts = [(cut,count) for cut,count in zip(cuts,counts)]
                return counts
	
	def update(self,ignored):
		self.value = self.getCounts(self.source['cutsSingle'],self.source['candsSingle'])

class countsDouble (countsSingle):
	def update(self,ignored):
		self.value = self.getCounts(self.source['cutsDouble'],self.source['candsDouble'])

class countsDoubleDisc (countsSingle):
	def update(self,ignored):
		self.value = self.getCounts(self.source['cutsDoubleDisc'],self.source['candsDoubleDisc'])
