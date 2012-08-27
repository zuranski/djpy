from supy import analysisStep

class general(analysisStep):
	def uponAcceptance(self,e): 
                self.book.fill(e['PfHt'],'PfHt',100,0,1e3,None,title = 'PfJets ; PfHt [GeV] ; events / bin')
		self.book.fill(e['nPfJets'],'nPfJets',16,-0.5,15.5,None,title='nPfJets ; nPfJets ; events / bin')
		self.book.fill(e['nPV'],'nPV',50,-0.5,49.5,None,title='nPV ; nPV ; events / bin')
		self.book.fill(e['nTrks'],'nTrks',100,0,2500,None, title='nTrks ; nTrks ; events / bin')
