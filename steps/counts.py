from supy import analysisStep

class cuts(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		nCount = len(e[self.collection])
		counts = [count[1] for count in e[self.collection]]
		cutNames = [count[0].name for count in e[self.collection]]
		labels = [count[0].name+'('+count[0].rangeName()+')' for count in e[self.collection]]
		labels = ["*"+label if cutName in e["doubleLooseCuts"] else "**"+label if cutName in e["doubleTightCuts"] else label for label,cutName in zip(labels,cutNames)]
		for i in range(nCount):
			self.book.fill(i,self.collection,nCount,-0.5,nCount-0.5,w=counts[i],title="%s ; ; nCands"%self.collection,xAxisLabels=labels)
		 
class discs(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		nCount = len(e[self.collection])
		counts = [count[1] for count in e[self.collection]]
		cutNames = [count[0].name for count in e[self.collection]]
		labels = [count[0].name+'('+count[0].rangeName()+')' for count in e[self.collection]]
		for i in range(nCount):
			self.book.fill(i,self.collection,nCount,-0.5,nCount-0.5,w=counts[i],title="%s ; ; nCands"%self.collection,xAxisLabels=labels)
