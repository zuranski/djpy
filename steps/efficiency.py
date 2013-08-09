from supy import analysisStep,whereami
import math,pickle,os

class eff(analysisStep):
	def __init__(self,indicesAcc='',indicesRecoLow='',indicesRecoHigh='',pdfweights=None):
		for item in ['indicesAcc','indicesRecoLow','indicesRecoHigh','pdfweights']: setattr(self,item,eval(item))
		self.trigweights = pickle.load(open(whereami()+"/../data/trigw"))
		self.flavorMap={1:'uds',2:'uds',3:'uds',4:'c',5:'b',11:'e',13:'mu',1.5:'ud',7:'umu',7.5:'dmu'}
		self.fs = [0.4,0.6,1.,1.4]

	def ctau(self,file):
		file=os.path.basename(file)
		masses = [a.replace(a[a.find('.'):],"") if '.' in a else a for a in file.split('_')]
		map={
			# Hidden Valley samples
            '1000_350':35,'1000_150':10,'1000_50':4,
            '400_150':40,'400_50':8,'200_50':20,'120_50':50,
			# Chi0 samples
			'1500_494':18.1,'1000_148':5.85,'350_148':18.8,'120_48':15.5
        }
		key = masses[1]+'_'+masses[3]
		return map[key]

	def ctau_cand_w(self,ct,ctau,f):
		return (1./f) * math.exp(-(ct/ctau)*(1./f - 1.))

	### obsolete 
	def X2qqIndices(self,Xs):
		pdgIds=[6001114,6002114,6003114,1000022]
		return [i for i in range(2) if Xs[i] in pdgIds]
	
	def X2qqFlavors(self,X2qqIndices,qFlavors):
		return [qFlavors[len(qFlavors)/2*i+1] for i in X2qqIndices]
	### end obsolete

	def eweights(self,XCandIndices,ctau,e):
		nCandsPerX = math.factorial(len(e['genqPt'])/2)/2
		ev_w = e['weight']
		pdf_w = e[self.pdfweights] if self.pdfweights is not None else 1.
		tot_w = ev_w*pdf_w
		ctau_ws = [1]*len(self.fs)
		for i,f in enumerate(self.fs):
			for idx in XCandIndices:
				if idx % nCandsPerX == 0: # weight only one candidate per X
					ctau_ws[i]*=self.ctau_cand_w(e['gendijetCtau'][idx],ctau,f)

		weights = [tot_w*ctau_w for ctau_w in ctau_ws]
		return weights

class NX(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		if e['XpdgId'][0]>6000000:
			bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
			ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)
			NSamples=3
		else: bin,ctau,NSamples=0,self.ctau(self.inputFileName),1

		# determine which Xs decay with at least one jet
		XCandIndices = [i for i in e['gendijetIndices'] if e['gendijetFlavor'][i] not in [11,13]]
		XCandFlavors = [e['gendijetFlavor'][i] for i in XCandIndices]

		N=len(self.fs)
		weights = self.eweights(XCandIndices,ctau,e)

		for i in range(len(self.fs)):
			for idx in XCandIndices:
				self.book.fill(bin*N+i,'NX',NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'NX'+self.flavorMap[XCandFlavors[idx]],NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])

		for idx in XCandIndices:
			self.book.fill(e['HPt'],'HPt',10,0,500)
			self.book.fill(e['HPt'],'HPt'+self.flavorMap[XCandFlavors[idx]],10,0,500)
			self.book.fill(e['gendijetXDR'][idx],'XDR',10,0,1)
			self.book.fill(e['gendijetXDR'][idx],'XDR'+self.flavorMap[XCandFlavors[idx]],10,0,1)
			self.book.fill(e['gendijetXPt'][idx],'XPt',20,0,700)
			self.book.fill(e['gendijetXPt'][idx],'XPt'+self.flavorMap[XCandFlavors[idx]],20,0,700)
			self.book.fill(e['gendijetLxy'][idx],'Lxy',10,0,50)
			self.book.fill(e['gendijetLxy'][idx],'Lxy'+self.flavorMap[XCandFlavors[idx]],10,0,50)
			self.book.fill(e['gendijetIP2dMin'][idx],'IP2dMin',10,0,30)
			self.book.fill(e['gendijetIP2dMin'][idx],'IP2dMin'+self.flavorMap[XCandFlavors[idx]],10,0,30)
			self.book.fill(e['gendijetIP2dMax'][idx],'IP2dMax',10,0,30)
			self.book.fill(e['gendijetIP2dMax'][idx],'IP2dMax'+self.flavorMap[XCandFlavors[idx]],10,0,30)
			self.book.fill(e['gendijetNLep'][idx],'NLep',5,-0.5,4.5)
			self.book.fill(e['gendijetNLep'][idx],'NLep'+self.flavorMap[XCandFlavors[idx]],5,-0.5,4.5)
			self.book.fill(e['gendijetBlxyz'][idx],'Blxyz',5,-0.,5.)
			self.book.fill(e['gendijetBlxyz'][idx],'Blxyz'+self.flavorMap[XCandFlavors[idx]],5,0.,5.)


class NXAcc(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		if e['XpdgId'][0]>6000000:
			bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
			ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)
			NSamples=3
		else: bin,ctau,NSamples=0,self.ctau(self.inputFileName),1

		# determine which Xs decay with at least one jet
		XCandIndices = [i for i in e['gendijetIndices'] if e['gendijetFlavor'][i] not in [11,13]]
		XCandFlavors = [e['gendijetFlavor'][i] for i in XCandIndices]

		N=len(self.fs)
		weights = self.eweights(XCandIndices,ctau,e)

		for i in range(len(self.fs)):
			for idx in e[self.indicesAcc]:
				self.book.fill(bin*N+i,'AccNX',NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'AccNX'+self.flavorMap[XCandFlavors[idx]],NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])

		for idx in e[self.indicesAcc]:
			self.book.fill(e['HPt'],'AccHPt',10,0,500)
			self.book.fill(e['HPt'],'AccHPt'+self.flavorMap[XCandFlavors[idx]],10,0,500)
			self.book.fill(e['gendijetXDR'][idx],'XDR',10,0,1)
			self.book.fill(e['gendijetXDR'][idx],'XDR'+self.flavorMap[XCandFlavors[idx]],10,0,1)
			self.book.fill(e['gendijetXPt'][idx],'AccXPt',20,0,700)
			self.book.fill(e['gendijetXPt'][idx],'AccXPt'+self.flavorMap[XCandFlavors[idx]],20,0,700)
			self.book.fill(e['gendijetLxy'][idx],'AccLxy',10,0,50)
			self.book.fill(e['gendijetLxy'][idx],'AccLxy'+self.flavorMap[XCandFlavors[idx]],10,0,50)
			self.book.fill(e['gendijetIP2dMin'][idx],'AccIP2dMin',10,0,30)
			self.book.fill(e['gendijetIP2dMin'][idx],'AccIP2dMin'+self.flavorMap[XCandFlavors[idx]],10,0,30)
			self.book.fill(e['gendijetIP2dMax'][idx],'AccIP2dMax',10,0,30)
			self.book.fill(e['gendijetIP2dMax'][idx],'AccIP2dMax'+self.flavorMap[XCandFlavors[idx]],10,0,30)
			
			self.book.fill(e['gendijetNLep'][idx],'AccNLep',5,-0.5,4.5)
			self.book.fill(e['gendijetNLep'][idx],'AccNLep'+self.flavorMap[XCandFlavors[idx]],5,-0.5,4.5)
			self.book.fill(e['gendijetBlxyz'][idx],'AccBlxyz',5,-0.,5.)
			self.book.fill(e['gendijetBlxyz'][idx],'AccBlxyz'+self.flavorMap[XCandFlavors[idx]],5,0.,5.)

class NXReco(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		if e['XpdgId'][0]>6000000:
			bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
			ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)
			NSamples=3
		else: bin,ctau,NSamples=0,self.ctau(self.inputFileName),1

		# determine which Xs decay to dijets
		XCandIndices = [i for i in e['gendijetIndices'] if e['gendijetFlavor'][i] not in [11,13]]

		N=len(self.fs)
		weights = self.eweights(XCandIndices,ctau,e)

		indicesLow = e[self.indicesRecoLow]['H'] if type(e[self.indicesRecoLow])==dict else e[self.indicesRecoLow]
		indicesHigh = e[self.indicesRecoHigh]['H'] if type(e[self.indicesRecoHigh])==dict else e[self.indicesRecoHigh]
		indices = indicesLow+indicesHigh
		names = ['Low']*len(indicesLow) + ['High']*len(indicesHigh)		

		#print [e['dijetTrueFlavor'][i] for i in indicesHigh]
		for i in range(len(self.fs)):
			for idx,name in zip(indices,names):
				self.book.fill(bin*N+i,name+'NX',NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,name+'NX'+self.flavorMap[e['dijetTrueFlavor'][idx]],NSamples*N,-0.5,NSamples*N-0.5,w=weights[i])

		for idx,name in zip(indices,names):
			self.book.fill(e['dijetTrueLxy'][idx],name+'Lxy',10,0,50)
			self.book.fill(e['dijetTrueLxy'][idx],name+'Lxy'+self.flavorMap[e['dijetTrueFlavor'][idx]],10,0,50)
			self.book.fill(e['dijetTrueXDR'][idx],name+'XDR',10,0,1)
			self.book.fill(e['dijetTrueXDR'][idx],name+'XDR'+self.flavorMap[e['dijetTrueFlavor'][idx]],10,0,1)
			self.book.fill(e['dijetTrueXPt'][idx],name+'XPt',20,0,700)
			self.book.fill(e['dijetTrueXPt'][idx],name+'XPt'+self.flavorMap[e['dijetTrueFlavor'][idx]],20,0,700)
			self.book.fill(e['dijetTrueHPt'][idx],name+'HPt',10,0,500)
			self.book.fill(e['dijetTrueHPt'][idx],name+'HPt'+self.flavorMap[e['dijetTrueFlavor'][idx]],10,0,500)
			self.book.fill(e['dijetTrueIP2dMin'][idx],name+'IP2dMin',10,0,30)
			self.book.fill(e['dijetTrueIP2dMin'][idx],name+'IP2dMin'+self.flavorMap[e['dijetTrueFlavor'][idx]],10,0,30)
			self.book.fill(e['dijetTrueIP2dMax'][idx],name+'IP2dMax',10,0,30)
			self.book.fill(e['dijetTrueIP2dMax'][idx],name+'IP2dMax'+self.flavorMap[e['dijetTrueFlavor'][idx]],10,0,30)

			self.book.fill(e['dijetTrueNLep'][idx],name+'NLep',5,-0.5,4.5)
			self.book.fill(e['dijetTrueNLep'][idx],name+'NLep'+self.flavorMap[e['dijetTrueFlavor'][idx]],5,-0.5,4.5)
			self.book.fill(e['dijetTrueBlxyz'][idx],name+'Blxyz',5,0.,5.)
			self.book.fill(e['dijetTrueBlxyz'][idx],name+'Blxyz'+self.flavorMap[e['dijetTrueFlavor'][idx]],5,0.,5.)
