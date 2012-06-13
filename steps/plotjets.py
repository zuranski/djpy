from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pfjpt",100,40,500,None,"%s ; pt[GeV] ;pfjets / bin" %self.collection)
			self.book.fill(cand.eta,"pfjeta",50,-3,3,w=None,title="%s ; eta ;pfjets / bin" %self.collection)
			self.book.fill(cand.phi,"pfjphi",50,-4,4,w=None,title="%s ; phi ;pfjets / bin" %self.collection)
			self.book.fill(cand.energy,"pfjenergy",50,40,500,w=None,title="%s ; energy ;pfjets / bin" %self.collection)
			self.book.fill(cand.mass,"pfjmass",250,0,250,w=None,title="%s ; mass ;pfjets / bin" %self.collection)

class fractions(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.neuHadFrac,"pfjNeuHadFrac",50,0,1,w=None,title="%s ; Neutral Hadron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.neuHadN,"pfjNeuHadN",50,0,100,w=None,title="%s ; Neutral Hadron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(cand.chgHadFrac,"pfjChgHadFrac",50,0,1,w=None,title="%s ; Charged Hadron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.chgHadN,"pfjChgHadN",50,0,100,w=None,title="%s ; Charged Hadron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(cand.phFrac,"pfjphFrac",50,0,1,w=None,title="%s ; Photon Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.phN,"pfjphN",50,0,100,w=None,title="%s ; Photon Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(cand.eleFrac,"pfjeleFrac",50,0,1,w=None,title="%s ; Electron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.eleN,"pfjeleN",50,0,10,w=None,title="%s ; Electron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(cand.muFrac,"pfjmuFrac",50,0,1,w=None,title="%s ; Muon Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.muN,"pfjmuN",50,0,10,w=None,title="%s ; Muon Multiplicity ;pfjets / bin" %self.collection)

class tracks(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.nPrompt,"pfjNPromptTrks",100,0,50,w=None,title="%s ; N Prompt Tracks ;pfjets / bin" %self.collection)
			self.book.fill(cand.nDispTracks,"pfjNDispTrks",100,0,50,w=None,title="%s ; NDisplaced Tracks ;pfjets / bin" %self.collection)
			self.book.fill(cand.PromptEnergyFrac,"pfjPromptEnergyFrac",50,0,1,w=None,title="%s ; Prompt Energy Fraction ;pfjets / bin" %self.collection)

class vertices(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.lxy,"pfjlxy",100,0,100,w=None,title="%s ; lxy ;pfjets / bin" %self.collection)
			self.book.fill(cand.lxysig,"pfjlxysig",100,0,100,w=None,title="%s ; lxy significance ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxpt,"pfjvtxpt",100,0,100,w=None,title="%s ; vtx pt ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxmass,"pfjvtxmass",300,0,10,w=None,title="%s ; vtx mass ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxchi2,"pfjvtxchi2",50,0,20,w=None,title="%s ; vtx chi2 ;pfjets / bin" %self.collection)
			self.book.fill(cand.trksInVtx,"NVtx",15,0.5,15.5,w=None,title="%s ; N Tracks used in Vtx ; pfjets / bin" %self.collection)	

class disptracks(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
		
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			tracks = cand.disptracks
			for t in tracks:
				self.book.fill(t.pt,'tpt',50,0,100,w=None,title="Displaced Tracks; pt ; tracks / bin")
          			self.book.fill(t.chi2,'tchi2',50,0,10,w=None,title="Displaced Tracks; chi2 ; tracks / bin")
				self.book.fill(t.nHits,'tnHits',20,0.5,20.5,w=None,title="Displaced Tracks; nValidHits ; tracks / bin")
				self.book.fill(t.nPixHits,'tnPixHits',7,-0.5,6.5,w=None,title="Displaced Tracks; nValidPixelHits ; tracks / bin")
          			self.book.fill(t.algo,'talgo',11,-0.5,10.5,w=None,title="Displaced Tracks; algo ; tracks / bin")
          			self.book.fill(t.vtxweight,'tvtxw',50,0,1,w=None,title="Displaced Tracks; vtx weight ; tracks / bin")
          			self.book.fill(t.ip2d,'tip2d',100,-50,50,w=None,title="Displaced Tracks; IP 2D ; tracks / bin")
          			self.book.fill(t.ip3d,'tip3d',100,-100,100,w=None,title="Displaced Tracks; IP 3D ; tracks / bin")

