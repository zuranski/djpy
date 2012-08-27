from supy import analysisStep

class vertices(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection
	
	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.ExoVtxFrac,"ExoVtxFrac",20,0,1,w=None,title="%s ; ExoVtxFrac ;candidates / bin" %self.collection)
			self.book.fill(cand.lxy,"lxy",100,0,100,w=None,title="%s ; lxy ;candidates / bin" %self.collection)
			self.book.fill(cand.glxyrmsall,"glxyrmsall",100,0,2.5,w=None,title="%s ; glxyrms_all ;candidates / bin" %self.collection)
			self.book.fill(cand.glxyrmsvtx,"glxyrmsvtx",100,0,2.5,w=None,title="%s ; glxyrms_vtx ;candidates / bin" %self.collection)
			self.book.fill(cand.glxyrmsclr,"glxyrmsclr",100,0,2.5,w=None,title="%s ; glxyrms_clr ;candidates / bin" %self.collection)
			self.book.fill(cand.glxydistall,"glxydistall",100,0,2.5,w=None,title="%s ; glxydist_all ;candidates / bin" %self.collection)
			self.book.fill(cand.glxydistvtx,"glxydistvtx",100,0,2.5,w=None,title="%s ; glxydist_vtx ;candidates / bin" %self.collection)
			self.book.fill(cand.glxydistclr,"glxydistclr",100,0,2.5,w=None,title="%s ; glxydist_clr ;candidates / bin" %self.collection)
			self.book.fill(cand.guessedFrac,"guessedFrac",30,0,1,w=None,title="%s ; guessed Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.posip2dFrac,"posip2dFrac",30,0,1,w=None,title="%s ; posip2d Fraction ;candidates / bin" %self.collection)
			#self.book.fill(cand.posip3dFrac,"posip3dFrac",30,0,1,w=None,title="%s ; posip3d Fraction ;candidates / bin" %self.collection)
			self.book.fill(cand.lxysig,"lxysig",100,0,100,w=None,title="%s ; lxy significance ;candidates / bin" %self.collection)
			self.book.fill(cand.vtxpt,"vtxpt",200,0,200,w=None,title="%s ; vtx pt ;candidates / bin" %self.collection)
			self.book.fill(cand.vtxptRatio,"vtxptratio",50,0,1,w=None,title="%s ; vtx pt ratio ;candidates / bin" %self.collection)
			self.book.fill(cand.vtxmass,"vtxmass",300,0,100,w=None,title="%s ; vtx mass ;candidates / bin" %self.collection)
			#self.book.fill(cand.vtxchi2,"vtxchi2",50,0,20,w=None,title="%s ; vtx chi2 ;candidates / bin" %self.collection)
			self.book.fill(cand.vtxN,"NVtx",16,-0.5,15.5,w=None,title="%s ; N Tracks used in Vtx ; candidates / bin" %self.collection)	
			self.book.fill(cand.nDispTracks - cand.vtxN,"NnotVtx",16,-0.5,15.5,w=None,title="%s ; N Tracks NOT used in Vtx ; candidates / bin" %self.collection)	
			self.book.fill(cand.vtxNRatio,"vtxNRatio",30,0.,1.,w=None,title="%s ; vtxNRatio; candidates / bin" %self.collection)	
			self.book.fill(cand.vtxNTotRatio,"vtxNTotRatio",30,0.,1.,w=None,title="%s ; vtxNTotRatio; candidates / bin" %self.collection)	
			self.book.fill(cand.vtxdR,"Vtx dR",50,0.,4.,w=None,title="%s ; Vtx deltaR ; candidates / bin" %self.collection)	
			self.book.fill(cand.vtxCharge,"Vtx Charge",11,-5.5,5.5,w=None,title="%s ; Vtx charge ; candidates / bin" %self.collection)	
			#self.book.fill((cand.vtxN,cand.vtxmass),"NtrkMass",(15,300),(0.5,0),(15.5,30),w=None,title="%s ; N Tracks used in Vtx ; vtx mass" %self.collection)	
			#self.book.fill((cand.vtxpt,cand.vtxmass),"VtxPtMass",(100,300),(0,0),(100,30),w=None,title="%s ; vtx pt ; vtx mass" %self.collection)	
			#self.book.fill((cand.vtxdR,cand.vtxmass),"VtxdRMass",(50,300),(0,0),(4,30),w=None,title="%s ; vtx dR ; vtx mass" %self.collection)	
			#self.book.fill((cand.vtxCharge,cand.vtxmass),"VtxChargeMass",(11,300),(-5.5,0),(5.5,30),w=None,title="%s ; vtx Charge ; vtx mass" %self.collection)	
			#self.book.fill((cand.vtxN,cand.vtxCharge),"VtxChargeNTrk",(15,11),(0.5,-5.5),(15.5,5.5),w=None,title="%s ; N Tracks used in Vtx ; vtx Charge" %self.collection)	
			self.book.fill(cand.nAvgHitsBefVert,"nAvgHitsBefVert",12,0.,6.,w=None,title="%s ; nAvgHitsBefVert ; candidates / bin" %self.collection)	
			self.book.fill(cand.nAvgMissHitsAfterVert,"nAvgMissHitsAfterVert",12,0.,6,w=None,title="%s ; nAvgMissHitsAfterVert ; candidates / bin" %self.collection)	

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
