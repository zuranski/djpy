from supy import analysisStep

class jetHistogramer(analysisStep):
	def uponAcceptance(self,e):
		N = len(e["jpt"])
		for i in range(N):
			self.book.fill(e["jpt"].at(i),"jpt",100,30,500,None,title="CaloJets ; pt[GeV] ;jets / bin")
			self.book.fill(e["jeta"].at(i),"jeta",50,-3,3,w=None,title="CaloJets ; eta ;jets / bin")
			self.book.fill(e["jphi"].at(i),"jphi",50,-4,4,w=None,title="CaloJets ; phi ;jets / bin")

		N = len(e["pfjpt"])
		for i in range(N):
			self.book.fill(e["pfjpt"].at(i),"pfjpt",100,30,500,None,"PFJets ; pt[GeV] ;pfjets / bin")
			self.book.fill(e["pfjeta"].at(i),"pfjeta",50,-3,3,w=None,title="PFJets ; eta ;pfjets / bin")
			self.book.fill(e["pfjphi"].at(i),"pfjphi",50,-4,4,w=None,title="PFJets ; phi ;pfjets / bin")
			self.book.fill(e["pfjNeuF"].at(i),"pfjNeuF",50,0,1,w=None,title="PFJets ; Nuetral Energy Fraction ;pfjets / bin")
			self.book.fill(e["pfjChgF"].at(i),"pfjChgF",50,0,1,w=None,title="PFJets ; Charged Energy Fraction ;pfjets / bin")
			self.book.fill(e["pfjNTrks"].at(i),"pfjNTrks",100,0,50,w=None,title="PFJets ; NTracks ;pfjets / bin")
