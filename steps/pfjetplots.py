from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.pt,"pt",100,0,300,None,"%s ; pt[GeV] ;candidates / bin" %self.collection)
			self.book.fill(cand.eta,"eta",50,-3,3,w=None,title="%s ; eta ;candidates / bin" %self.collection)
			#self.book.fill(cand.phi,"phi_%s"%self.collection,50,-4,4,w=None,title="%s ; phi ;candidates / bin" %self.collection)
			self.book.fill(cand.energy,"energy",50,40,500,w=None,title="%s ; energy ;candidates / bin" %self.collection)
			self.book.fill(cand.mass,"mass",100,0,500,w=None,title="%s ; mass ;candidates / bin" %self.collection)

class fractions(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.neuHadFrac,"NeuHadFrac",50,0,1,w=None,title="%s ; Neutral Hadron Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.neuHadN,"NeuHadN",50,0,100,w=None,title="%s ; Neutral Hadron Multiplicity ;candidates / bin" %self.collection)
			self.book.fill(cand.chgHadFrac,"ChgHadFrac",50,0,1,w=None,title="%s ; Charged Hadron Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.chgHadN,"ChgHadN",50,0,100,w=None,title="%s ; Charged Hadron Multiplicity ;candidates / bin" %self.collection)
			self.book.fill(cand.phFrac,"phFrac",50,0,1,w=None,title="%s ; Photon Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.phN,"phN",50,0,100,w=None,title="%s ; Photon Multiplicity ;candidates / bin" %self.collection)
			self.book.fill(cand.eleFrac,"eleFrac",50,0,1,w=None,title="%s ; Electron Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.eleN,"eleN",50,0,10,w=None,title="%s ; Electron Multiplicity ;candidates / bin" %self.collection)
			self.book.fill(cand.muFrac,"muFrac",50,0,1,w=None,title="%s ; Muon Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.muN,"muN",50,0,10,w=None,title="%s ; Muon Multiplicity ;candidates / bin" %self.collection)

class tracks(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.nPrompt,"NPromptTrks",50,-0.5,49.5,w=None,title="%s ; N Prompt Tracks ;candidates / bin" %self.collection)
			self.book.fill(cand.nDispTracks,"NDispTrks",50,-0.5,49.5,w=None,title="%s ; NDisplaced Tracks ;candidates / bin" %self.collection)
			self.book.fill(cand.PromptEnergyFrac,"PromptEnergyFrac",50,0,1,w=None,title="%s ; Prompt Energy Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.nPrompt*cand.PromptEnergyFrac,"Promptness",100,0,3,w=None,title="%s ; Promptness ;candidates / bin" %self.collection)

class double(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.dR,"dR",50,0,6,w=None,title="%s; dR ;candidates / bin" %self.collection )
			self.book.fill(cand.dPhi,"dPhi",50,-4,4,w=None,title="%s ; dPhi ;candidates / bin" %self.collection)

class discs(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.discpromptness,"discpromptness",100,0.98,1.001,None,"%s ; promptness ;cands / bin" %self.collection)
			self.book.fill(cand.discvtxQual,"discvtxQual",100,0.98,1.001,None,"%s ; vtxQual ;cands / bin" %self.collection)
			self.book.fill(cand.disckin,"disckin",100,0.96,1.001,None,"%s ; kin ;cands / bin" %self.collection)
			self.book.fill((cand.discpromptness,cand.discvtxQual),"discpromptnessvtxQual",(15,15),(0.96,0.96),(1.01,1.01),None,"%s ; promptness ; vtxQual" %self.collection)
			self.book.fill((cand.discpromptness,cand.disckin),"discpromptnesskin",(15,15),(0.96,0.96),(1.01,1.01),None,"%s ; promptness ; kin" %self.collection)
			self.book.fill((cand.disckin,cand.discvtxQual),"disckinvtxQual",(15,15),(0.96,0.96),(1.01,1.01),None,"%s ; kin ; vtxQual" %self.collection)
		
