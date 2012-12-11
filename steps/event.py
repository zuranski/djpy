from supy import analysisStep
import math

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
		for i in range(2):	self.book.fill(bin,'effDenom',3,-0.5,2.5,None)

class effNum(analysisStep):
	def __init__(self,indices):
		self.indices = indices
		self.map={
			'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
			'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,
		}

	def weight(self,ct,ctau,expo):
		f = math.pow(10,expo)
		return 1./f * math.exp(-ct/ctau*(1./f - 1))

	def uponAcceptance(self,e):
		inputString = self.inputFileName.split('.')[0].split('/')[-1]
		ctau_base = self.map[inputString]
		bin = (e["XpdgId"][0]-6000114)/1000 - 1
		ctau=ctau_base*pow(10,int(bin-1))
		for idx in e[self.indices]: 
			self.book.fill(bin,'effNum0',3,-0.5,2.5,None)
			self.book.fill(bin,'effNump',3,-0.5,2.5,w=self.weight(e['dijetTrueCtau'][idx],ctau,0.33))
			self.book.fill(bin,'effNumm',3,-0.5,2.5,w=self.weight(e['dijetTrueCtau'][idx],ctau,-0.33))
