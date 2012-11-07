from supy import analysisStep
import itertools

class plots(analysisStep):
	def __init__(self,njets=2,indices=None,plot2D=False,plot1D=True):
		self.prefix = ['jet','dijet'][njets-1]
		self.indices = indices if indices is not None else self.prefix+'Indices'
		self.tag = self.indices[:self.indices.find('Indices')]
		self.plot1D = plot1D
		self.plot2D = plot2D

	def uponAcceptance(self,e):
		if self.plot1D:
			for var in self.vars:
				for idx in e[self.indices]:
					self.book.fill(e[self.prefix+var['name']][idx],var['name']+'_h_'+self.tag,var['bins'],var['low'],
								   var['high'],w=None,title="%s; %s%s ; %s / bin "
								   %(self.prefix,var['name'],var['unit'],self.prefix))

		if self.plot2D:
			for var1,var2 in itertools.combinations(self.vars,2):
				for idx in e[self.indices]:
					self.book.fill((e[self.prefix+var1['name']][idx],e[self.prefix+var2['name']][idx]),
                                   var1['name']+'_'+var2['name']+'_h_'+self.tag,(var1['bins'],var2['bins']),
                                   (var1['low'],var2['low']),(var1['high'],var2['high']),
								   w=None,title="%s ; %s%s; %s%s" 
								   %(self.prefix,var1['name'],var1['unit'],var2['name'],var2['unit']))

class ABCDplots(analysisStep):
	def __init__(self,indices=None):
		self.indices = indices
		self.collection=indices[:indices.find('_ABCDIndices')]+indices[indices.find('_ABCDIndices')+12:]
		self.cut0,self.cut1,self.cut2 = indices.split('_')[:3]

	def uponAcceptance(self,e):
		indicesDict = e[self.indices]
		self.book.fill((0,0),self.collection+'ABCDcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['A']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((0,1),self.collection+'ABCDcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['B']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,0),self.collection+'ABCDcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['C']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,1),self.collection+'ABCDcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['D']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((0,0),self.collection+'EFGHcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['E']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((0,1),self.collection+'EFGHcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['F']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,0),self.collection+'EFGHcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['G']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])
		self.book.fill((1,1),self.collection+'EFGHcounts',(2,2),(-0.5,-0.5),(1.5,1.5),w=len(indicesDict['H']),
		title=self.collection + " ; " + self.cut1 +";"+ self.cut2+"; counts",
		xAxisLabels=['False','True'],yAxisLabels=['False','True'])


class general(plots):
	vars = [
            {'name':'Pt','bins':100,'low':0,'high':300,'unit':'[GeV]'},
            {'name':'Eta','bins':50,'low':-3,'high':3,'unit':''},
            {'name':'Phi','bins':50,'low':-3.5,'high':3.5,'unit':''},
            {'name':'Energy','bins':50,'low':40,'high':500,'unit':'[GeV]'},
            {'name':'Mass','bins':100,'low':0,'high':500,'unit':'[GeV]'},
            {'name':'NConstituents','bins':100,'low':0.5,'high':100.5,'unit':''},
           ]

class fractions(plots):
	vars = [
            {'name':'NeuHadFrac','bins':50,'low':0,'high':1,'unit':''},
            {'name':'NeuHadN','bins':50,'low':-0.5,'high':99.5,'unit':''},
            {'name':'ChgHadFrac','bins':50,'low':0,'high':1,'unit':''},
            {'name':'ChgHadN','bins':50,'low':-0.5,'high':99.5,'unit':''},
            {'name':'MuFrac','bins':50,'low':0,'high':1,'unit':''},
            {'name':'MuN','bins':10,'low':-0.5,'high':9.5,'unit':''},
            {'name':'EleFrac','bins':50,'low':0,'high':1,'unit':''},
            {'name':'EleN','bins':10,'low':-0.5,'high':9.5,'unit':''},
            {'name':'PhFrac','bins':50,'low':0,'high':1,'unit':''},
            {'name':'PhN','bins':50,'low':-0.5,'high':99.5,'unit':''},
           ]

class promptness(plots):
	vars = [
            {'name':'NPromptTracks','bins':50,'low':-0.5,'high':49.5,'unit':''},
            {'name':'NDispTracks','bins':50,'low':-0.5,'high':49.5,'unit':''},
            {'name':'PromptEnergyFrac','bins':50,'low':0,'high':1,'unit':''},
           ]

class vertices(plots):
	vars = [
            {'name':'Lxysig','bins':50,'low':0,'high':100,'unit':''},
            {'name':'VtxN','bins':15,'low':1.5,'high':16.5,'unit':''},
            {'name':'Vtxmass','bins':50,'low':0,'high':100,'unit':'[GeV]'},
            {'name':'Vtxpt','bins':50,'low':0,'high':200,'unit':'[GeV]'},
            {'name':'VtxNRatio','bins':20,'low':0,'high':1,'unit':''},
            {'name':'Posip2dFrac','bins':10,'low':0,'high':1.001,'unit':''},
            {'name':'NAvgMissHitsAfterVert','bins':6,'low':0,'high':6,'unit':''},
           ]

class clusters(plots):
	vars = [
            {'name':'glxyrmsclr','bins':50,'low':0,'high':2.5,'unit':''},
            {'name':'bestclusterN','bins':15,'low':1.5,'high':16.5,'unit':''},
           ]

class ABCDvars(plots):
	vars = [
            {'name':'Discriminant','bins':14,'low':0.,'high':1.,'unit':''},
            {'name':'Promptness1','bins':50,'low':0.,'high':20,'unit':''},
            {'name':'Promptness2','bins':50,'low':0.,'high':20,'unit':''},
            {'name':'Mass','bins':20,'low':0,'high':800,'unit':'[GeV]'},
           ]

class cutvars(plots):
	vars = [
            {'name':'Lxysig','bins':50,'low':0,'high':100,'unit':''},
            {'name':'Promptness1','bins':50,'low':0.,'high':20,'unit':''},
            {'name':'Promptness2','bins':50,'low':0.,'high':20,'unit':''},
            {'name':'VtxN','bins':15,'low':1.5,'high':16.5,'unit':''},
            {'name':'Vtxmass','bins':50,'low':0,'high':100,'unit':'[GeV]'},
            {'name':'Vtxpt','bins':50,'low':0,'high':200,'unit':'[GeV]'},
            {'name':'Posip2dFrac','bins':10,'low':0,'high':1.001,'unit':''},
            {'name':'NAvgMissHitsAfterVert','bins':12,'low':0,'high':6,'unit':''},
            {'name':'glxyrmsclr','bins':50,'low':0,'high':2.5,'unit':''},
            {'name':'bestclusterN','bins':15,'low':1.5,'high':16.5,'unit':''},
	       ]

class observables(plots):
	vars = [
            {'name':'Mass','bins':100,'low':0,'high':500,'unit':'[GeV]'},
            {'name':'Lxy','bins':50,'low':0,'high':60,'unit':'[GeV]'},
            {'name':'TrueLxy','bins':50,'low':0,'high':60,'unit':'[GeV]'},
	       ]

class trigvars(plots):
	vars = [
            {'name':'Pt','bins':10,'low':60,'high':300,'unit':'[GeV]'},
            {'name':'Eta','bins':20,'low':-2,'high':2,'unit':''},
            {'name':'Phi','bins':20,'low':-3.15,'high':3.15,'unit':''},
            {'name':'Promptness','bins':50,'low':0.,'high':5,'unit':''},
            {'name':'NPromptTracks','bins':11,'low':-0.5,'high':10.5,'unit':''},
            {'name':'PromptEnergyFrac','bins':25,'low':0.,'high':0.5,'unit':''},
           ]
