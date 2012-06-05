from supy import analysisStep

class general(analysisStep):
	def uponAcceptance(self,e):
		N = len(e["jpt"])
		for i in range(N):
			self.book.fill(e["jpt"].at(i),"jpt",100,40,500,None,title="CaloJets ; pt[GeV] ;jets / bin")
			self.book.fill(e["jeta"].at(i),"jeta",50,-3,3,w=None,title="CaloJets ; eta ;jets / bin")
			self.book.fill(e["jphi"].at(i),"jphi",50,-4,4,w=None,title="CaloJets ; phi ;jets / bin")
			self.book.fill(e["jmass"].at(i),"jmass",100,0,300,w=None,title="CaloJets ; mass ;jets / bin")
