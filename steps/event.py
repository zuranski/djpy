from supy import analysisStep

class general(analysisStep):
	def uponAcceptance(self,e): 
		self.book.fill(e['pfHT'],'pfHT',100,0,1e3,None,title = 'PfJets ; pfHT [GeV] ; events / bin')
		self.book.fill(e['caloHT'],'caloHT',100,0,1e3,None,title = 'CaloJets ; caloHT [GeV] ; events / bin')
		self.book.fill(e['nPfJets'],'nPfJets',16,-0.5,15.5,None,title='nPfJets ; nPfJets ; events / bin')
		self.book.fill(e['nPV'],'nPV',50,-0.5,49.5,None,title='nPV ; nPV ; events / bin')
		self.book.fill(e['nTrks'],'nTrks',100,0,2500,None, title='nTrks ; nTrks ; events / bin')

class effDenom(analysisStep):
	def uponAcceptance(self,e):
		bin = (e["XpdgId"][0]-6000114)/1000 - 1
		self.book.fill(bin,'effDenom',3,-0.5,2.5,w=2)

class effNum(analysisStep):
	def __init__(self,indices):
		self.indices = indices

	def uponAcceptance(self,e):
		bin = (e["XpdgId"][0]-6000114)/1000 - 1
		self.book.fill(bin,'effNum',3,-0.5,2.5,w=len(e[self.indices]))
