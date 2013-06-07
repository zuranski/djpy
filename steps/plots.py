from supy import analysisStep
import itertools

class plots(analysisStep):
	def __init__(self,njets=2,indices=None,plot2D=False,plot1D=True,ks=False):
		self.prefix = ['jet','dijet'][njets-1]
		if ks: self.prefix='ks'
		self.indices = indices if indices is not None else self.prefix+'Indices'
		self.tag = ''.join(self.indices.split('Indices'))
		self.plot1D = plot1D
		self.plot2D = plot2D

	def uponAcceptance(self,e):
		if self.plot1D:
			for var in self.vars:
				for idx in e[self.indices]:
					self.book.fill(e[self.prefix+var['name']][idx],var['name']+'_h_'+self.tag,var['bins'],var['low'],
								   var['high'],w=None,title="%s; %s ; %s / bin "
								   %(self.prefix,var['label'],self.prefix))

		if self.plot2D:
			for var1,var2 in itertools.combinations(self.vars,2):
				for idx in e[self.indices]:
					self.book.fill((e[self.prefix+var1['name']][idx],e[self.prefix+var2['name']][idx]),
                                   var1['name']+'_'+var2['name']+'_h_'+self.tag,(var1['bins'],var2['bins']),
                                   (var1['low'],var2['low']),(var1['high'],var2['high']),
								   w=None,title="%s ; %s; %s" 
								   %(self.prefix,var1['label'],var2['label']))

class ABCDplots(analysisStep):
	def __init__(self,indices=None):
		self.indices = indices
		self.collection = ''.join(self.indices.split('ABCDIndices'))

	def uponAcceptance(self,e):
		indicesDict = e[self.indices]
		for key,value in sorted(indicesDict.iteritems()):
			self.book.fill(key,self.collection+'ABCDcounts',4,0.5,4.5,w=len(indicesDict[key]))

class ABCDEFGHplots(analysisStep):
	def __init__(self,indices=None):
		self.indices = indices
		self.collection = ''.join(self.indices.split('ABCDEFGHIndices'))

	def uponAcceptance(self,e):
		indicesDict = e[self.indices]
		for key,value in sorted(indicesDict.iteritems()):
			self.book.fill(key,self.collection+'ABCDEFGHcounts',8,0.5,8.5,w=len(indicesDict[key]))

class general(plots):
	vars = [
            {'name':'Pt','bins':50,'low':40,'high':300,'label':'p_{T} [GeV]'},
            {'name':'Eta','bins':50,'low':-3,'high':3,'label':'#eta'},
            {'name':'Phi','bins':50,'low':-3.5,'high':3.5,'label':'#phi'},
            {'name':'Energy','bins':50,'low':40,'high':500,'label':'Energy [GeV]'},
            {'name':'Mass','bins':100,'low':0,'high':500,'label':'mass [GeV]'},
            {'name':'NConstituents','bins':100,'low':0.5,'high':100.5,'label':'N constituents'},
           ]

class fractions(plots):
	vars = [
            {'name':'NeuHadFrac','bins':50,'low':0,'high':1,'label':'neutral Had Fraction'},
            {'name':'NeuHadN','bins':15,'low':-0.5,'high':29.5,'label':'neutral Had Multiplicity'},
            {'name':'ChgHadFrac','bins':50,'low':0,'high':1,'label':'charged Had Fraction'},
            {'name':'ChgHadN','bins':50,'low':-0.5,'high':99.5,'label':'charged Had Multiplicity'},
            {'name':'MuFrac','bins':50,'low':0,'high':1,'label':'muon Fraction'},
            {'name':'MuN','bins':10,'low':-0.5,'high':9.5,'label':'muon Multplicity'},
            {'name':'EleFrac','bins':50,'low':0,'high':1,'label':'electron Fraction'},
            {'name':'EleN','bins':10,'low':-0.5,'high':9.5,'label':'electron Multplicity'},
            {'name':'PhFrac','bins':50,'low':0,'high':1,'label':'photon Fraction'},
            {'name':'PhN','bins':50,'low':-0.5,'high':99.5,'label':'photon Multiplicity'},
           ]

class promptness(plots):
	vars = [
            {'name':'NPromptTracks','bins':30,'low':-0.5,'high':29.5,'label':'N prompt tracks'},
            {'name':'NDispTracks','bins':30,'low':-0.5,'high':29.5,'label':'N displaced tracks'},
            {'name':'PromptEnergyFrac','bins':50,'low':0,'high':1,'label':'Prompt Energy Fraction'},
           ]

class vertices(plots):
	vars = [
            {'name':'Lxy','bins':50,'low':0,'high':60,'label':'L_{xy} [cm]'},
            {'name':'Lxysig','bins':50,'low':0,'high':100,'label':'L_{xy} significance'},
            {'name':'VtxN','bins':15,'low':1.5,'high':16.5,'label':'Vtx multplicity'},
            {'name':'Vtxmass','bins':50,'low':0,'high':100,'label':'Vtx mass [GeV]'},
            {'name':'Vtxpt','bins':50,'low':0,'high':200,'label':'Vtx p_{T} [GeV]'},
            {'name':'VtxNRatio','bins':20,'low':0,'high':1,'label':'Vtx N ratio'},
            {'name':'Posip2dFrac','bins':10,'low':0,'high':1.001,'label':'Tracks with positive IP Fraction'},
            {'name':'NAvgMissHitsAfterVert','bins':6,'low':0,'high':6,'label':'Missing Hits per track afert Vertex'},
           ]

class clusters(plots):
	vars = [
            {'name':'glxyrmsclr','bins':50,'low':0,'high':2.5,'label':'Cluster RMS'},
            {'name':'bestclusterN','bins':15,'low':1.5,'high':16.5,'label':'Cluster Track Multplicity'},
           ]

class ABCDvars(plots):
	vars = [
            {'name':'Discriminant','bins':14,'low':0.,'high':1.,'label':'Vtx/Cluster Discriminant'},
            {'name':'PromptEnergyFrac1','bins':50,'low':0.,'high':1,'label':'Prompt Energy Fraction 1'},
            {'name':'PromptEnergyFrac2','bins':50,'low':0.,'high':1,'label':'Prompt Energy Fracion 2'},
            {'name':'NPromptTracks1','bins':11,'low':-0.5,'high':10.5,'label':'N Prompt Tracks 1'},
            {'name':'NPromptTracks2','bins':11,'low':-0.5,'high':10.5,'label':'N Prompt Tracks 2'},
            {'name':'Mass','bins':20,'low':0,'high':800,'label':'Dijet Mass [GeV]'},
           ]

class cutvars(plots):
	vars = [
            {'name':'Lxy','bins':50,'low':0,'high':60,'label':'L_{xy} [cm]'},
            {'name':'PromptEnergyFrac1','bins':20,'low':0.,'high':1,'label':'Prompt Energy Fraction 1'},
            {'name':'PromptEnergyFrac2','bins':20,'low':0.,'high':1,'label':'Prompt Energy Fracion 2'},
            {'name':'NPromptTracks1','bins':11,'low':-0.5,'high':10.5,'label':'N Prompt Tracks 1'},
            {'name':'NPromptTracks2','bins':11,'low':-0.5,'high':10.5,'label':'N Prompt Tracks 2'},
            {'name':'Lxysig','bins':25,'low':0,'high':100,'label':'L_{xy} significance'},
            {'name':'VtxN','bins':15,'low':1.5,'high':16.5,'label':'Vtx Track Multiplicity'},
            {'name':'Vtxmass','bins':25,'low':0,'high':100,'label':'Vtx mass [GeV]'},
            {'name':'Vtxpt','bins':25,'low':0,'high':200,'label':'Vtx p_{T} [GeV]'},
            {'name':'Posip2dFrac','bins':10,'low':0,'high':1.001,'label':'Tracks with positive IP Fraction'},
            {'name':'NAvgMissHitsAfterVert','bins':12,'low':0,'high':6,'label':'Missing Hits per track after Vertex'},
            {'name':'glxyrmsclr','bins':10,'low':0,'high':1,'label':'Cluster RMS'},
            {'name':'bestclusterN','bins':15,'low':1.5,'high':16.5,'label':'Cluster Tracks Multiplicity'},
	       ]

class observables(plots):
	vars = [
            {'name':'Mass','bins':50,'low':0,'high':500,'label':'Dijet Invariant Mass [GeV]'},
            {'name':'Lxy','bins':50,'low':0,'high':60,'label':'L_{xy}[GeV]'},
            {'name':'TrkAvgPt','bins':30,'low':0,'high':20,'label':'average track p_{T} [GeV]'},
	       ]

class trigvars(plots):
	vars = [
            {'name':'Pt','bins':10,'low':60,'high':300,'label':'p_{T} [GeV]'},
            {'name':'Eta','bins':10,'low':-2,'high':2,'label':'#eta'},
            {'name':'Phi','bins':10,'low':-3.15,'high':3.15,'label':'#phi'},
            {'name':'NPromptTracks','bins':11,'low':-0.5,'high':10.5,'label':'N Prompt Tracks'},
            {'name':'PromptEnergyFrac','bins':10,'low':0.,'high':0.5,'label':'Prompt Energy Fraction'},
           ]

class kshort(plots):
	vars = [
            {'name':'P','bins':50,'low':0,'high':100,'label':'momentum [GeV]'},
            {'name':'Pt','bins':50,'low':0,'high':40,'label':'p_{T} [GeV]'},
            {'name':'Eta','bins':50,'low':-2,'high':2,'label':'#eta'},
            {'name':'Phi','bins':50,'low':-3.15,'high':3.15,'label':'#phi'},
            {'name':'Mass','bins':100,'low':0.43,'high':0.57,'label':'mass [GeV]'},
            {'name':'Ctau','bins':100,'low':0.,'high':12,'label':'c#tau [cm]'},
            {'name':'Lxy','bins':100,'low':0.,'high':60,'label':'L_{xy} [cm]'},
            {'name':'Lxyz','bins':100,'low':0.,'high':120,'label':'L_{xyz} [cm]'},
            {'name':'JetPt','bins':100,'low':20.,'high':300,'label':'Jet p_{T} [GeV]'},
            {'name':'Trk1IP2d','bins':50,'low':-2.,'high':20,'label':'IP1_{xy} [cm]'},
            {'name':'Trk2IP2d','bins':50,'low':-2.,'high':20,'label':'IP2_{xy} [cm]'},
            {'name':'Trk1IP3d','bins':50,'low':0.,'high':25,'label':'IP1_{xyz} [cm]'},
            {'name':'Trk2IP3d','bins':50,'low':0.,'high':25,'label':'IP2_{xyz} [cm]'},
           ]

class genjets(plots):
	vars = [
            {'name':'Energy','bins':22,'low':60,'high':500,'label':'Energy [GeV]'},
            {'name':'Pt','bins':22,'low':60,'high':500,'label':'p_{T} [GeV]'},
            {'name':'Eta','bins':10,'low':-2,'high':2,'label':'#eta'},
            {'name':'Phi','bins':10,'low':-3.15,'high':3.15,'label':'#phi'},
            {'name':'genjetPtDiff','bins':50,'low':-1.,'high':1,'label':'(jet p_{T} - true p_{T} )/ true p_{T}'},
            {'name':'genjetLxy','bins':30,'low':0.,'high':60,'label':'L_{xy} [cm]'},
            {'name':'genjetAngle','bins':36,'low':0.,'high':12,'label':'approach Angle [deg]'},
            {'name':'genjetDeltaR','bins':30,'low':0.,'high':3.15,'label':'q#bar{q} #Delta R'},
            {'name':'NeuFrac','bins':15,'low':0.1,'high':1,'label':'Neutral Energy Fraction'},
            {'name':'NDispTracks','bins':15,'low':-0.5,'high':29.5,'label':'N tracks'},
		   ]
