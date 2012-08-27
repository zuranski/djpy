from supy import analysisStep

class histos(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pt_%s"%self.collection,50,0,500,None,"%s ; pt[GeV] ;candidates / bin" %self.collection)
			self.book.fill(cand.eta,"eta_%s"%self.collection,30,-3,3,w=None,title="%s ; eta ;candidates / bin" %self.collection)
			self.book.fill(cand.phi,"phi_%s"%self.collection,30,-4,4,w=None,title="%s ; phi ;candidates / bin" %self.collection)
			self.book.fill(cand.truelxy,"truelxy_%s"%self.collection,30,0,60,w=None,title="%s ; lxy ;candidates / bin" %self.collection)
			self.book.fill(cand.mass,"mass_%s"%self.collection,100,0,500,w=None,title="%s ; mass ;candidates / bin" %self.collection)
