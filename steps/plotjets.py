from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		for pfjet in e[self.collection]:
			self.book.fill(pfjet.pt,"pfjpt",100,40,500,None,"%s ; pt[GeV] ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.eta,"pfjeta",50,-3,3,w=None,title="%s ; eta ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.phi,"pfjphi",50,-4,4,w=None,title="%s ; phi ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.energy,"pfjenergy",50,40,500,w=None,title="%s ; energy ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.mass,"pfjmass",100,0,300,w=None,title="%s ; mass ;pfjets / bin" %self.collection)

class fractions(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		for pfjet in e[self.collection]:
			self.book.fill(pfjet.neuHadFrac,"pfjNeuHadFrac",50,0,1,w=None,title="%s ; Neutral Hadron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.neuHadN,"pfjNeuHadN",50,0,100,w=None,title="%s ; Neutral Hadron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.chgHadFrac,"pfjChgHadFrac",50,0,1,w=None,title="%s ; Charged Hadron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.chgHadN,"pfjChgHadN",50,0,100,w=None,title="%s ; Charged Hadron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.phFrac,"pfjphFrac",50,0,1,w=None,title="%s ; Photon Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.phN,"pfjphN",50,0,100,w=None,title="%s ; Photon Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.eleFrac,"pfjeleFrac",50,0,1,w=None,title="%s ; Electron Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.eleN,"pfjeleN",50,0,10,w=None,title="%s ; Electron Multiplicity ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.muFrac,"pfjmuFrac",50,0,1,w=None,title="%s ; Muon Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.muN,"pfjmuN",50,0,10,w=None,title="%s ; Muon Multiplicity ;pfjets / bin" %self.collection)

class tracks(analysisStep):

	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		for pfjet in e[self.collection]:
			self.book.fill(pfjet.nPrompt,"pfjNPromptTrks",100,0,50,w=None,title="%s ; N Prompt Tracks ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.nDispTracks,"pfjNDispTrks",100,0,50,w=None,title="%s ; NDisplaced Tracks ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.PromptEnergyFrac,"pfjPromptEnergyFrac",50,0,1,w=None,title="%s ; Prompt Energy Fraction ;pfjets / bin" %self.collection)

class vertices(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def uponAcceptance(self,e):
		for pfjet in e[self.collection]:
			self.book.fill(pfjet.lxy,"pfjlxy",100,-2,100,w=None,title="%s ; lxy ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.lxysig,"pfjlxysig",100,-2,100,w=None,title="%s ; lxy significance ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.vtxpt,"pfjvtxpt",100,-2,150,w=None,title="%s ; vtx pt ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.vtxmass,"pfjvtxmass",100,-2,50,w=None,title="%s ; vtx mass ;pfjets / bin" %self.collection)
			self.book.fill(pfjet.vtxchi2,"pfjvtxchi2",100,-2,100,w=None,title="%s ; vtx chi2 ;pfjets / bin" %self.collection)

class disptracks(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	def fractionUsedInVtx(self,tracks):
		n=0
		for t in tracks:
			if t.vtxweight > 0.01: n+=1
		return n/float(len(tracks))
		
	def uponAcceptance(self,e):
		for pfjet in e[self.collection]:
			tracks = pfjet.disptracks
			self.book.fill(self.fractionUsedInVtx(tracks),"fNVtx",20,0,1,w=None,title="%s ; Fraction of Tracks used in Vtx ; pfjets / bin")	

			for t in tracks:
				self.book.fill(t.pt,'tpt',50,0,100,w=None,title="Displaced Tracks; pt ; tracks / bin")
          			self.book.fill(t.chi2,'tchi2',50,0,10,w=None,title="Displaced Tracks; chi2 ; tracks / bin")
				self.book.fill(t.nHits,'tnHits',20,0.5,20.5,w=None,title="Displaced Tracks; nValidHits ; tracks / bin")
				self.book.fill(t.nPixHits,'tnPixHits',7,-0.5,6.5,w=None,title="Displaced Tracks; nValidPixelHits ; tracks / bin")
          			self.book.fill(t.algo,'talgo',11,-0.5,10.5,w=None,title="Displaced Tracks; algo ; tracks / bin")
          			self.book.fill(t.vtxweight,'tvtxw',50,0,1,w=None,title="Displaced Tracks; vtx weight ; tracks / bin")
          			self.book.fill(t.ip2d,'tip2d',100,-50,50,w=None,title="Displaced Tracks; IP 2D ; tracks / bin")
          			self.book.fill(t.ip3d,'tip3d',100,-100,100,w=None,title="Displaced Tracks; IP 3D ; tracks / bin")

