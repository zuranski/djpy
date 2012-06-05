from supy import analysisStep

class general(analysisStep):
	def uponAcceptance(self,e):
		for pfjet in e["pfjets"]:
			self.book.fill(pfjet.pt,"pfjpt",100,40,500,None,"PFJets ; pt[GeV] ;pfjets / bin")
			self.book.fill(pfjet.eta,"pfjeta",50,-3,3,w=None,title="PFJets ; eta ;pfjets / bin")
			self.book.fill(pfjet.phi,"pfjphi",50,-4,4,w=None,title="PFJets ; phi ;pfjets / bin")
			self.book.fill(pfjet.energy,"pfjenergy",50,40,500,w=None,title="PFJets ; energy ;pfjets / bin")
			self.book.fill(pfjet.mass,"pfjmass",100,0,300,w=None,title="PFJets ; mass ;pfjets / bin")

class fractions(analysisStep):

	def uponAcceptance(self,e):
		for pfjet in e["pfjets"]:
			self.book.fill(pfjet.neuHadFrac,"pfjNeuHadFrac",50,0,1,w=None,title="PFJets ; Neutral Hadron Energy Fraction ;pfjets / bin")
			self.book.fill(pfjet.neuHadN,"pfjNeuHadN",50,0,100,w=None,title="PFJets ; Neutral Hadron Multiplicity ;pfjets / bin")
			self.book.fill(pfjet.chgHadFrac,"pfjChgHadFrac",50,0,1,w=None,title="PFJets ; Charged Hadron Energy Fraction ;pfjets / bin")
			self.book.fill(pfjet.chgHadN,"pfjChgHadN",50,0,100,w=None,title="PFJets ; Charged Hadron Multiplicity ;pfjets / bin")
			self.book.fill(pfjet.phFrac,"pfjphFrac",50,0,1,w=None,title="PFJets ; Photon Energy Fraction ;pfjets / bin")
			self.book.fill(pfjet.phN,"pfjphN",50,0,100,w=None,title="PFJets ; Photon Multiplicity ;pfjets / bin")
			self.book.fill(pfjet.eleFrac,"pfjeleFrac",50,0,1,w=None,title="PFJets ; Electron Energy Fraction ;pfjets / bin")
			self.book.fill(pfjet.eleN,"pfjeleN",50,0,10,w=None,title="PFJets ; Electron Multiplicity ;pfjets / bin")
			self.book.fill(pfjet.muFrac,"pfjmuFrac",50,0,1,w=None,title="PFJets ; Muon Energy Fraction ;pfjets / bin")
			self.book.fill(pfjet.muN,"pfjmuN",50,0,10,w=None,title="PFJets ; Muon Multiplicity ;pfjets / bin")

class tracks(analysisStep):
	def uponAcceptance(self,e):
		for pfjet in e["pfjets"]:
			self.book.fill(pfjet.nPrompt,"pfjNPromptTrks",100,0,50,w=None,title="PFJets ; N Prompt Tracks ;pfjets / bin")
			self.book.fill(pfjet.nDispTracks,"pfjNDispTrks",100,0,50,w=None,title="PFJets ; NDisplaced Tracks ;pfjets / bin")
			self.book.fill(pfjet.PromptEnergyFrac,"pfjPromptEnergyFrac",50,0,1,w=None,title="PFJets ; Prompt Energy Fraction ;pfjets / bin")

class vertices(analysisStep):
	def uponAcceptance(self,e):
		for pfjet in e["pfjets"]:
			if pfjet.lxy < 0 : continue
			self.book.fill(pfjet.lxy,"pfjlxy",100,-2,100,w=None,title="PFJets ; lxy ;pfjets / bin")
			self.book.fill(pfjet.lxysig,"pfjlxysig",100,-2,100,w=None,title="PFJets ; lxy significance ;pfjets / bin")
			self.book.fill(pfjet.vtxpt,"pfjvtxpt",100,-2,300,w=None,title="PFJets ; vtx pt ;pfjets / bin")
			self.book.fill(pfjet.vtxmass,"pfjvtxmass",100,-2,200,w=None,title="PFJets ; vtx mass ;pfjets / bin")
			self.book.fill(pfjet.vtxchi2,"pfjvtxchi2",100,-2,100,w=None,title="PFJets ; vtx chi2 ;pfjets / bin")
