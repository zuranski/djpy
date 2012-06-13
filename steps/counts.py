from supy import analysisStep

class counts(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		nCounts = len(e[self.collection])
		for count in e[self.collection]:
			self.book.fill(count[0],self.collection,0,nCounts,nCounts,w=count[1],title="%s ; ; nCands"%self.collection)
		 
