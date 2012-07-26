from supy import analysisStep

class histos(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pfjpt_%s"%self.collection,50,0,500,None,"%s ; pt[GeV] ;pfjets / bin" %self.collection)
			self.book.fill(cand.eta,"pfjeta_%s"%self.collection,30,-3,3,w=None,title="%s ; eta ;pfjets / bin" %self.collection)
			self.book.fill(cand.phi,"pfjphi_%s"%self.collection,30,-4,4,w=None,title="%s ; phi ;pfjets / bin" %self.collection)
			self.book.fill(cand.truelxy,"pfjtruelxy_%s"%self.collection,30,0,60,w=None,title="%s ; lxy ;pfjets / bin" %self.collection)
			self.book.fill(cand.mass,"pfjmass_%s"%self.collection,100,0,500,w=None,title="%s ; mass ;pfjets / bin" %self.collection)
