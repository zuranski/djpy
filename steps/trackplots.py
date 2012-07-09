from supy import analysisStep

class disptracks(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
		
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			tracks = cand.disptracks
			for t in tracks:
				#if t.vtxweight < 0.5 : continue
				self.book.fill(t.pt,'tpt',50,0,100,w=None,title="Displaced Tracks; pt ; tracks / bin")
          			self.book.fill(t.chi2,'tchi2',50,0,10,w=None,title="Displaced Tracks; chi2 ; tracks / bin")
				self.book.fill(t.nHits,'tnHits',20,0.5,20.5,w=None,title="Displaced Tracks; nValidHits ; tracks / bin")
				self.book.fill(t.nPixHits,'tnPixHits',7,-0.5,6.5,w=None,title="Displaced Tracks; nValidPixelHits ; tracks / bin")
          			self.book.fill(t.algo,'talgo',11,-0.5,10.5,w=None,title="Displaced Tracks; algo ; tracks / bin")
          			self.book.fill(t.vtxweight,'tvtxw',50,0,1,w=None,title="Displaced Tracks; vtx weight ; tracks / bin")
          			self.book.fill(t.ip2d,'tip2d',100,-10,10,w=None,title="Displaced Tracks; IP 2D ; tracks / bin")
          			self.book.fill(t.guesslxy/cand.lxy,'guesslxy',100,-5,5,w=None,title="Displaced Tracks; guesslxy ; tracks / bin")
          			self.book.fill(t.ip3d,'tip3d',100,-30,30,w=None,title="Displaced Tracks; IP 3D ; tracks / bin")

