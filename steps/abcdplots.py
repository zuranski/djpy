from supy import analysisStep

class abcd_histo(analysisStep):
	def __init__(self,collection,binning1 = None, binning2 = None):
		self.collection = "%s" %collection
		self.cut1 = self.collection.split("_")[1]
		self.cut2 = self.collection.split("_")[2]
		self.binning1 = binning1
		self.binning2 = binning2
	
	def uponAcceptance(self,e):
		for cand in e[self.collection].candidates:
			self.book.fill((getattr(cand,self.cut1),getattr(cand,self.cut2)),
			self.collection,(self.binning1[0],self.binning2[0]),(self.binning1[1],self.binning2[1]),
			(self.binning1[2],self.binning2[2]),w=None,
			title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; cands/bin")

class abcd_counts(analysisStep):
	def __init__(self,collection = None):
		self.collection = "%s" %collection
		self.cut1 = self.collection.split("_")[1]
		self.cut2 = self.collection.split("_")[2]

	def uponAcceptance(self,e):
		weights = e[self.collection].counts
		self.book.fill((0,0),self.collection+'counts',(2,2),(-0.5,-0.5),(1.5,1.5),w=weights['A'],
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,0),self.collection+'counts',(2,2),(-0.5,-0.5),(1.5,1.5),w=weights['B'],
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((0,1),self.collection+'counts',(2,2),(-0.5,-0.5),(1.5,1.5),w=weights['C'],
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,1),self.collection+'counts',(2,2),(-0.5,-0.5),(1.5,1.5),w=weights['D'],
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
