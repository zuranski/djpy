from supy import analysisStep
import math

class general(analysisStep):
	def __init__(self,tag=''):
		self.tag=tag

	def uponAcceptance(self,e): 
		self.book.fill(e['pfHT'],self.tag+'pfHT',100,0,1e3,None,title = 'PfJets ; pfHT [GeV] ; events / bin')
		self.book.fill(e['caloHT'],self.tag+'caloHT',50,0,1.5e3,None,title = 'CaloJets ; caloHT [GeV] ; events / bin')
		self.book.fill(e['nPfJets'],self.tag+'nPfJets',16,-0.5,15.5,None,title='nPfJets ; nPfJets ; events / bin')
		self.book.fill(e['nPV'],self.tag+'nPV',26,4.5,30.5,None,title='nPV ; nPV ; events / bin')
		self.book.fill(e['nTrks'],self.tag+'nTrks',100,0,2500,None, title='nTrks ; nTrks ; events / bin')

class genevent(analysisStep):
	def uponAcceptance(self,e):
		self.book.fill(e['HPt'],'HPt',100,0,1000,None,title=' ; H p_{T} [GeV] ; events / bin' )
		self.book.fill(e['HEta'],'HEta',30,-5,5,None,title=' ; H #eta ; events / bin' )
		self.book.fill(e['HMass'],'HMass',1000,100,1100,None,title=' ; H mass [GeV] ; events / bin' )
		betagamma=e['HPt']*math.cosh(e['HEta'])/e['HMass']
		self.book.fill(betagamma,'betagamma',100,0,10,None,title=' ; H #beta#gamma; events / bin' )
		for i in range(len(e['XPt'])):
			self.book.fill(e['XPt'][i],'XPt',100,0,800,None,title=' ; X p_{T} [GeV] ; events / bin' )
			self.book.fill(e['XEta'][i],'XEta',30,-5,5,None,title=' ; X #eta ; events / bin' )
			self.book.fill(e['gendijetDR'][i],'XDR',30,0,3,None,title=' ; q#bar{q} #Delta R ; events / bin' )

class runModulo(analysisStep):
	def __init__(self,modulo,inverted=False):
		self.modulo = modulo
		self.inverted = inverted

	def select(self,e):
		passed = (e['run'] % self.modulo == 0)
		return ((not passed) if self.inverted else passed)

class efftrk(analysisStep):
	def __init__(self,indices):
		self.indices=indices

	def uponAcceptance(self,e):
		ev_w = e['weight']
		pt_ws = [a for a in e['ksPtRatio']]
		eta_ws = [a for a in e['ksEtaRatio']]
		ctau_ws = [ev_w*a*b for a,b in zip(pt_ws,eta_ws)]
		for idx in e[self.indices]:
			self.book.fill(e['ksLxy'][idx],'ksLxy',100,0,60,w=ctau_ws[idx],title=';L_{xy} [cm]; K_{s} / bin')
			self.book.fill(e['ksLxyz'][idx],'ksLxyz',100,0,120,w=ctau_ws[idx],title=';L_{xyz} [cm]; K_{s} / bin')
			self.book.fill(e['ksCtau'][idx],'ksCtau',100,0,12,w=ctau_ws[idx],title=';c#tau [cm]; K_{s} / bin')
			self.book.fill(e['ksPt'][idx],'ksPt',50,0,40,w=ctau_ws[idx],title=';p_T [GeV/c]; K_{s} / bin')
			self.book.fill(e['ksTrk1Pt'][idx],'ksTrkPt',30,0,20,w=ctau_ws[idx],title=';track p_T [GeV/c]; K_{s} / bin')
			self.book.fill(e['ksTrk2Pt'][idx],'ksTrkPt',30,0,20,w=ctau_ws[idx],title=';track p_T [GeV/c]; K_{s} / bin')
			self.book.fill(e['ksP'][idx],'ksP',50,0,100,w=ctau_ws[idx],title=';momentum [GeV/c]; K_{s} / bin')
			self.book.fill(e['ksPhi'][idx],'ksPhi',50,-3.15,3.15,w=ctau_ws[idx],title=';#phi; K_{s} / bin')
			self.book.fill(e['ksEta'][idx],'ksEta',50,-2.,2.,w=ctau_ws[idx],title=';#eta; K_{s} / bin')
			self.book.fill(abs(e['ksTrk1IP2d'][idx]),'kstrkip2d',50,0,20,w=ctau_ws[idx],title=';track IP 2-d [cm]; K_{s} / bin')
			self.book.fill(abs(e['ksTrk2IP2d'][idx]),'kstrkip2d',50,0,20,w=ctau_ws[idx],title=';track IP 2-d [cm]; K_{s} / bin')
			self.book.fill(e['ksTrk1IP3d'][idx],'kstrkip3d',50,0,25,w=ctau_ws[idx],title=';track IP 3-d [cm]; K_{s} / bin')
			self.book.fill(e['ksTrk2IP3d'][idx],'kstrkip3d',50,0,25,w=ctau_ws[idx],title=';track IP 3-d [cm]; K_{s} / bin')
			if e['ksJetPt'][idx]>0:
				self.book.fill(e['ksJetPt'][idx],'numksJetPt',50,40,300,w=ctau_ws[idx],title=';jet p_T [GeV/c]; K_{s} / bin')
			self.book.fill(e['nPV'],'numnPV',26,4.5,30.5,w=ctau_ws[idx],title=';pile-up vertices; K_{s} / bin')
			if e['ksLxy'][idx]>2:
				self.book.fill(e['ksLxysig'][idx],'ksLxysig',100,0,1000,w=ctau_ws[idx],title=';L_{xy} significance; K_{s} / bin')
				self.book.fill(e['ksChi2'][idx],'ksChi2',50,0,7,w=ctau_ws[idx],title=';#chi^{2}/dof ; K_{s} / bin')

