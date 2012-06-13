from supy import wrappedChain

class countsSingle (wrappedChain.calculable):
	def getCounts(self,cuts,collection):
		counts = [0]*len(cuts)
                for cand in collection:
                        for i in range(len(cuts)):
				cutname = cuts[i].name
				try:
					cand.passes.index(cutname)
					counts[i]+=1
				except ValueError: 
					break
                counts = [(cut.name+'('+str(cut.min)+','+str(cut.max)+')',count) for cut,count in zip(cuts,counts)]
                return counts
	
	def update(self,ignored):
		self.value = self.getCounts(self.source['cutsSingle'],self.source['candsSingle'])

class countsDouble (countsSingle):
	def update(self,ignored):
		self.value = self.getCounts(self.source['cutsDouble'],self.source['candsDouble'])
		
			
