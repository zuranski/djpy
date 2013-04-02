from supy import analysisStep
import math,pickle

class general(analysisStep):
	def __init__(self,tag=''):
		self.tag=tag

	def uponAcceptance(self,e): 
		self.book.fill(e['pfHT'],self.tag+'pfHT',100,0,1e3,None,title = 'PfJets ; pfHT [GeV] ; events / bin')
		self.book.fill(e['caloHT'],self.tag+'caloHT',50,0,2e3,None,title = 'CaloJets ; caloHT [GeV] ; events / bin')
		self.book.fill(e['nPfJets'],self.tag+'nPfJets',16,-0.5,15.5,None,title='nPfJets ; nPfJets ; events / bin')
		self.book.fill(e['nPV'],self.tag+'nPV',26,4.5,30.5,None,title='nPV ; nPV ; events / bin')
		self.book.fill(e['nTrks'],self.tag+'nTrks',100,0,2500,None, title='nTrks ; nTrks ; events / bin')

class effDenom(analysisStep):
	def __init__(self,indices='gendijetIndices',pdfweights=None,cand=False):
		self.indices = indices
		self.pdfweights = pdfweights
		self.trigweights = pickle.load(open("data/trigw"))
		self.cand = cand
		expos = [-0.67,-0.33,0.,0.33,0.67]
		self.fs = [math.pow(10,a) for a in expos]

	def ctau(self,file):
		masses = file.split('_')
		masses = [a.replace(a[a.find('.'):],"") if '.' in a else a for a in masses]
		map={
            'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
            'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,
        }
		key = 'H_'+masses[1]+'_X_'+masses[3]
		return map[key]

	def ctau_w(self,ct,ctau,f):
		return (1./f) * math.exp(-(ct/ctau)*(1./f - 1.))

	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		bin = (e["XpdgId"][0]-6000114)/1000 - 1
		ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)

		# event weights
		ev_w = e['weight']
		pdf_w = e[self.pdfweights] if self.pdfweights is not None else 1.
		tot_w = ev_w*pdf_w
		N=len(self.fs)

		indices = e[self.indices] if self.cand else [0,1]
		for idx in indices:	
			ctau_event = e['gendijetCtau'][idx]
			for i,f in enumerate(self.fs):
				weight = tot_w*self.ctau_w(ctau_event,ctau,f)
				self.book.fill(bin*N+i,'effDenom',3*N,-0.5,3*N-0.5,w=weight)

class effNum(effDenom):
	def uponAcceptance(self,e):

		# find trigger weight
		trig_w=1
		ht=e['caloHT']
		for i,pair in enumerate(self.trigweights): 
			if ht < pair[0]: 
				trig_w = self.trigweights[i-1][1]
				break

		#print ht,trig_w

		# selection index	
		n = ''.join(self.indices.split('ABCDEFGHIndices'))
		idx_coll = e[self.indices]
		indices = idx_coll['H'] if type(idx_coll)==dict else idx_coll
		
		# determine the ctau of the event in the sample
		bin = (e["XpdgId"][0]-6000114)/1000 - 1
		ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)

		# event weights
		ev_w = e['weight']
		pdf_w = e[self.pdfweights] if self.pdfweights is not None else 1.
		tot_w = ev_w*pdf_w*trig_w
		N=len(self.fs)

		if not self.cand: indices=[0,1]
		for idx in indices: 
			ctau_event = e['dijetTrueCtau'][idx] if self.cand else e['gendijetCtau'][idx]
			for i,f in enumerate(self.fs):
				weight = tot_w*self.ctau_w(ctau_event,ctau,f)
				self.book.fill(bin*N+i,'effNum',3*N,-0.5,3*N-0.5,w=weight)

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

