from supy import analysisStep,whereami
import math,pickle,os

class eff(analysisStep):
	def __init__(self,indicesAcc='',indicesRecoLow='',indicesRecoHigh='',pdfweights=None):
		for item in ['indicesAcc','indicesRecoLow','indicesRecoHigh','pdfweights']: setattr(self,item,eval(item))
		self.trigweights = pickle.load(open(whereami()+"/../data/trigw"))
		self.flavorMap={1:'uds',2:'uds',3:'uds',4:'c',5:'b'}
		self.fs = [0.4,0.6,1.,1.4]

	def ctau(self,file):
		file=os.path.basename(file)
		masses = [a.replace(a[a.find('.'):],"") if '.' in a else a for a in file.split('_')]
		map={
            'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
            'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,'H_120_X_50':50,
        }
		key = 'H_'+masses[1]+'_X_'+masses[3]
		return map[key]

	def ctau_cand_w(self,ct,ctau,f):
		return (1./f) * math.exp(-(ct/ctau)*(1./f - 1.))

	def X2qqIndices(self,Xs):
		pdgIds=[6001114,6002114,6003114]
		return [i for i in range(2) if Xs[i] in pdgIds]
	
	def X2qqFlavors(self,X2qqIndices,qFlavors):
		return [qFlavors[2*i] for i in X2qqIndices]

	def eweights(self,X2qqIndices,ctau,e):
		ev_w = e['weight']
		pdf_w = e[self.pdfweights] if self.pdfweights is not None else 1.
		tot_w = ev_w*pdf_w
		ctau_ws = [1]*len(self.fs)
		for i,f in enumerate(self.fs):
			for idx in X2qqIndices:
				ctau_ws[i]*=self.ctau_cand_w(e['gendijetCtau'][idx],ctau,f)

		weights = [tot_w*ctau_w for ctau_w in ctau_ws]
		return weights

class NX(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
		ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)

		# determine which Xs decay to dijets
		X2qqIndices = self.X2qqIndices(e['XpdgId'])
		X2qqFlavors = self.X2qqFlavors(X2qqIndices,e['genqFlavor'])

		#print X2qqIndices,X2qqFlavors

		N=len(self.fs)
		weights = self.eweights(X2qqIndices,ctau,e)

		for i in range(len(self.fs)):
			for idx in X2qqIndices:
				self.book.fill(bin*N+i,'NX',3*N,-0.5,3*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'NX'+self.flavorMap[X2qqFlavors[idx]],3*N,-0.5,3*N-0.5,w=weights[i])


class NXAcc(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
		ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)

		# determine which Xs decay to dijets
		X2qqIndices = self.X2qqIndices(e['XpdgId'])
		X2qqFlavors = self.X2qqFlavors(X2qqIndices,e['genqFlavor'])

		N=len(self.fs)
		weights = self.eweights(X2qqIndices,ctau,e)

		for i in range(len(self.fs)):
			for idx in e[self.indicesAcc]:
				self.book.fill(bin*N+i,'NXAcc',3*N,-0.5,3*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'NXAcc'+self.flavorMap[X2qqFlavors[idx]],3*N,-0.5,3*N-0.5,w=weights[i])

class NXReco(eff):
	def uponAcceptance(self,e):

		# determine the ctau of the event in the sample
		bin = round((e["XpdgId"][0]-6000114)/1000.,0) - 1
		ctau=self.ctau(self.inputFileName)*pow(10,int(bin)-1)

		# determine which Xs decay to dijets
		X2qqIndices = self.X2qqIndices(e['XpdgId'])

		N=len(self.fs)
		weights = self.eweights(X2qqIndices,ctau,e)

		indicesLow = e[self.indicesRecoLow]['H'] if type(e[self.indicesRecoLow])==dict else e[self.indicesRecoLow]
		indicesHigh = e[self.indicesRecoHigh]['H'] if type(e[self.indicesRecoHigh])==dict else e[self.indicesRecoHigh]

		for i in range(len(self.fs)):
			for idx in indicesLow:
				self.book.fill(bin*N+i,'NXRecoLow',3*N,-0.5,3*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'NXRecoLow'+self.flavorMap[e['dijetTrueFlavor'][idx]],3*N,-0.5,3*N-0.5,w=weights[i])
			for idx in indicesHigh:
				self.book.fill(bin*N+i,'NXRecoHigh',3*N,-0.5,3*N-0.5,w=weights[i])
				self.book.fill(bin*N+i,'NXRecoHigh'+self.flavorMap[e['dijetTrueFlavor'][idx]],3*N,-0.5,3*N-0.5,w=weights[i])
				
