from supy import analysisStep

class histos(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		nCount = len(e[self.collection])
		labels = [count[0] for count in e[self.collection]]
		for i in range(nCount):
			count = e[self.collection][i]
			self.book.fill(i,self.collection,nCount,-0.5,nCount-0.5,w=count[1],title="%s ; ; nCands"%self.collection,xAxisLabels=labels)
		 
