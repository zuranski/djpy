from supy import analysisStep

class vertices(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.lxy,"pfjlxy",100,0,100,w=None,title="%s ; lxy ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxyrmsall,"pfjglxyrms_all",100,0,2.5,w=None,title="%s ; glxyrms_all ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxyrmsvtx,"pfjglxyrms_vtx",100,0,2.5,w=None,title="%s ; glxyrms_vtx ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxyrmsclr,"pfjglxyrms_clr",100,0,2.5,w=None,title="%s ; glxyrms_clr ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxydistall,"pfjglxydist_all",100,0,2.5,w=None,title="%s ; glxydist_all ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxydistvtx,"pfjglxydist_vtx",100,0,2.5,w=None,title="%s ; glxydist_vtx ;pfjets / bin" %self.collection)
			self.book.fill(cand.glxydistclr,"pfjglxydist_clr",100,0,2.5,w=None,title="%s ; glxydist_clr ;pfjets / bin" %self.collection)
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
