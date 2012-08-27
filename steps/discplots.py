from supy import analysisStep

class general(analysisStep):
	def __init__(self,collection):
		self.collection = "%s" %collection

	def uponAcceptance(self,e):
		for cand in e[self.collection]:
			self.book.fill(cand.discpromptness,"discpromptness",100,0.98,1.001,None,"%s ; promptness ;cands / bin" %self.collection)
			self.book.fill(cand.discvtxQual,"discvtxQual",100,0.98,1.001,None,"%s ; vtxQual ;cands / bin" %self.collection)
			self.book.fill(cand.disckin,"disckin",100,0.96,1.001,None,"%s ; kin ;cands / bin" %self.collection)
			self.book.fill((cand.discpromptness,cand.discvtxQual),"discpromptnessvtxQual",(15,15),(0,0),(1.01,1.01),None,"%s ; promptness ; vtxQual" %self.collection)
			self.book.fill((cand.discpromptness,cand.disckin),"discpromptnesskin",(15,15),(0,0),(1.01,1.01),None,"%s ; promptness ; kin" %self.collection)
			self.book.fill((cand.disckin,cand.discvtxQual),"disckinvtxQual",(15,15),(0,0),(1.01,1.01),None,"%s ; kin ; vtxQual" %self.collection)
