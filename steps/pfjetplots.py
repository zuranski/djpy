from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pfjpt",100,0,300,None,"%s ; pt[GeV] ;pfjets / bin" %self.collection)
			self.book.fill(cand.eta,"pfjeta",50,-3,3,w=None,title="%s ; eta ;pfjets / bin" %self.collection)
			#self.book.fill(cand.phi,"pfjphi_%s"%self.collection,50,-4,4,w=None,title="%s ; phi ;pfjets / bin" %self.collection)
			self.book.fill(cand.energy,"pfjenergy",50,40,500,w=None,title="%s ; energy ;pfjets / bin" %self.collection)
			self.book.fill(cand.mass,"pfjmass",100,0,500,w=None,title="%s ; mass ;pfjets / bin" %self.collection)

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
			self.book.fill(cand.nPrompt,"pfjNPromptTrks",50,-0.5,49.5,w=None,title="%s ; N Prompt Tracks ;pfjets / bin" %self.collection)
			self.book.fill(cand.nDispTracks,"pfjNDispTrks",50,-0.5,49.5,w=None,title="%s ; NDisplaced Tracks ;pfjets / bin" %self.collection)
			self.book.fill(cand.PromptEnergyFrac,"pfjPromptEnergyFrac",50,0,1,w=None,title="%s ; Prompt Energy Fraction ;pfjets / bin" %self.collection)
			self.book.fill(cand.Promptness,"pfjPromptness",100,0,3,w=None,title="%s ; Promptness ;pfjets / bin" %self.collection)

class double(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.dR,"dR",50,0,6,w=None,title="%s; dR ;pfjets / bin" %self.collection )
			self.book.fill(cand.dPhi,"dPhi",50,-4,4,w=None,title="%s ; dPhi ;pfjets / bin" %self.collection)
