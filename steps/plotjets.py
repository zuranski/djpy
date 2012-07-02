from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pfjpt",100,0,200,None,"%s ; pt[GeV] ;pfjets / bin" %self.collection)
			self.book.fill(cand.eta,"pfjeta",50,-3,3,w=None,title="%s ; eta ;pfjets / bin" %self.collection)
			self.book.fill(cand.phi,"pfjphi",50,-4,4,w=None,title="%s ; phi ;pfjets / bin" %self.collection)
			self.book.fill(cand.energy,"pfjenergy",50,40,500,w=None,title="%s ; energy ;pfjets / bin" %self.collection)
			self.book.fill(cand.mass,"pfjmass",250,0,250,w=None,title="%s ; mass ;pfjets / bin" %self.collection)

class double(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e['dispDouble']:
			self.book.fill(cand.dR,"dR",50,0,6,w=None,title="%s; dR ;pfjets / bin" %self.collection )
			self.book.fill(cand.dPhi,"dPhi",50,-4,4,w=None,title="%s ; dPhi ;pfjets / bin" %self.collection)


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
			self.book.fill(cand.guesslxyrms,"pfjguesslxyrms",100,0,5,w=None,title="%s ; guesslxyrms ;pfjets / bin" %self.collection)
			self.book.fill(cand.guessedFrac,"pfjguessedFrac",30,0,1,w=None,title="%s ; guessed Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.posip2dFrac,"pfjposip2dFrac",30,0,1,w=None,title="%s ; posip2d Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.posip3dFrac,"pfjposip3dFrac",30,0,1,w=None,title="%s ; posip3d Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.lxysig,"pfjlxysig",100,0,100,w=None,title="%s ; lxy significance ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxpt,"pfjvtxpt",100,0,100,w=None,title="%s ; vtx pt ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxmass,"pfjvtxmass",300,0,10,w=None,title="%s ; vtx mass ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxchi2,"pfjvtxchi2",50,0,20,w=None,title="%s ; vtx chi2 ;pfjets / bin" %self.collection)
			self.book.fill(cand.vtxN,"NVtx",15,0.5,15.5,w=None,title="%s ; N Tracks used in Vtx ; pfjets / bin" %self.collection)	
			self.book.fill(cand.nDispTracks + cand.nPrompt - cand.vtxN,"NnotVtx",15,0.5,15.5,w=None,title="%s ; N Tracks NOT used in Vtx ; pfjets / bin" %self.collection)	
			self.book.fill(cand.vtxNRatio,"vtxNRatio",30,0.,1.,w=None,title="%s ; vtxNRatio; pfjets / bin" %self.collection)	
			self.book.fill(cand.vtxdR,"Vtx dR",50,0.,4.,w=None,title="%s ; Vtx deltaR ; pfjets / bin" %self.collection)	
			self.book.fill(cand.vtxCharge,"Vtx Charge",11,-5.5,5.5,w=None,title="%s ; Vtx charge ; pfjets / bin" %self.collection)	
			self.book.fill((cand.vtxN,cand.vtxmass),"NtrkMass",(15,300),(0.5,0),(15.5,30),w=None,title="%s ; N Tracks used in Vtx ; vtx mass" %self.collection)	
			self.book.fill((cand.vtxpt,cand.vtxmass),"VtxPtMass",(100,300),(0,0),(100,30),w=None,title="%s ; vtx pt ; vtx mass" %self.collection)	
			self.book.fill((cand.vtxdR,cand.vtxmass),"VtxdRMass",(50,300),(0,0),(4,30),w=None,title="%s ; vtx dR ; vtx mass" %self.collection)	
			self.book.fill((cand.vtxCharge,cand.vtxmass),"VtxChargeMass",(11,300),(-5.5,0),(5.5,30),w=None,title="%s ; vtx Charge ; vtx mass" %self.collection)	
			self.book.fill((cand.vtxN,cand.vtxCharge),"VtxChargeNTrk",(15,11),(0.5,-5.5),(15.5,5.5),w=None,title="%s ; N Tracks used in Vtx ; vtx Charge" %self.collection)	

class vertexmap(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			if cand.vtxmass < 0.6 : continue
			import math
			r = math.sqrt(cand.vtxX*cand.vtxX + cand.vtxY*cand.vtxY)
			z = abs(cand.vtxZ)
			if z < 26 or (r>16 and z<70) or( r>55 and z<110):	
				self.book.fill((cand.vtxX,cand.vtxY),"vtx X-Y",(500,500),(-110,-110),(110,110),w=None,title="%s ; vtx X ; vtx Y" %self.collection)	
			else:
				self.book.fill((z,r),"vtx R-Z",(500,500),(0,0),(400,110),w=None,title="%s ; vtx Z ; vtx R" %self.collection)	

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

