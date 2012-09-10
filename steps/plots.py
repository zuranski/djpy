from supy import analysisStep
import itertools

class plots(analysisStep):
	def __init__(self,njets=2,indices=None):
		self.prefix = ['jet','dijet'][njets-1]
		self.indices = indices if indices is not None else self.prefix+'Indices'

	def uponAcceptance(self,e):
		for var in self.vars:
			for idx in e[self.indices]:
				self.book.fill(e[self.prefix+var['name']][idx],var['name']+'_h',var['bins'],var['low'],
							   var['high'],w=None,title="%s; %s%s ; %s / bin "
							   %(self.prefix,var['name'],var['unit'],self.prefix))

		if hasattr(self,'correlations'):
			for var1,var2 in itertools.combinations(self.vars,2):
				for idx in e[self.indices]:
					self.book.fill((e[self.prefix+var1['name']][idx],e[self.prefix+var2['name']][idx]),
                                   var1['name']+'_'+var2['name']+'_h',(var1['bins'],var2['bins']),
                                   (var1['low'],var2['low']),(var1['high'],var2['high']),
								   w=None,title="%s%s; %s%s; / bin" 
								   %(var1['name'],var1['unit'],var2['name'],var2['unit']))


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
            {'name':'VtxptRatio','bins':50,'low':0,'high':1,'unit':''},
            {'name':'VtxNTotRatio','bins':20,'low':0,'high':1,'unit':''},
            {'name':'Posip2dFrac','bins':10,'low':0,'high':1,'unit':''},
            {'name':'NAvgMissHitsAfterVert','bins':6,'low':0,'high':6,'unit':''},
           ]

class clusters(plots):
	vars = [
            {'name':'glxyrmsclr','bins':50,'low':0,'high':2.5,'unit':''},
            {'name':'bestclusterN','bins':15,'low':1.5,'high':16.5,'unit':''},
           ]

class discriminants(plots):
	correlations=True
	vars = [
            {'name':'DiscriminantVtx','bins':50,'low':0.99,'high':1,'unit':''},
            {'name':'DiscriminantPromptness','bins':50,'low':0.99,'high':1,'unit':''},
           ]    
