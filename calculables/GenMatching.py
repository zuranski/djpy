from supy import wrappedChain
from utils import MatchByDR

class jetTrueMatch(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value = MatchByDR(self.source['jetEta'],
							self.source['jetPhi'],
							self.source['genqEta'],
							self.source['genqPhi'],0.5) 

class jetTrue(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['jetIndices']]
			return
		self.value=[self.source[self.var][self.source['jetTrueMatch'][i]]
                    if self.source['jetTrueMatch'][i] is not None else None for i in self.source['jetIndices']]

class dijetTrue(wrappedChain.calculable):
	def update(self,ignored):
		if self.source['realData'] or len(self.source['XpdgId']) == 0: 
			self.value = [True for i in self.source['dijetIndices']]
			return
		self.value = [None for i in self.source['dijetIndices']]
		for i in self.source['dijetIndices']:
			Lxy1=self.source['jetTrueLxy'][self.source['dijetIdx1'][i]]
			Lxy2=self.source['jetTrueLxy'][self.source['dijetIdx2'][i]]
			if Lxy1 is None or Lxy2 is None or Lxy1!=Lxy2: continue
			val1=self.source[self.var][self.source['dijetIdx1'][i]]
			val2=self.source[self.var][self.source['dijetIdx2'][i]]
			self.value[i]={'avg':(val1+val2)/2.,
						   'min':min(val1,val2),
 						   'max':max(val1,val2),
						   'sum':(val1+val2)}[self.calc]

#  special case
class genqXPt(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[self.source['XPt'][i/2] for i in range(len(self.source['genqPt']))]

class genqHPt(wrappedChain.calculable):
	def update(self,ignored):
		self.value=[self.source['HPt'] for i in range(len(self.source['genqPt']))]

class jetTrueLxy(jetTrue): var='genqLxy'
class jetTrueCtau(jetTrue): var='genqCtau'
class jetTrueFlavor(jetTrue): var='genqFlavor'
class jetTrueNLep(jetTrue):	var='genqNLep'
class jetTrueBlxyz(jetTrue): var='genqBlxyz'
class jetTrueXPt(jetTrue): var='genqXPt'
class jetTrueHPt(jetTrue): var='genqHPt'
class jetTrueIP2d(jetTrue): var='genqIP2D'
class jetTrueIP3d(jetTrue): var='genqIP3D'

class dijetTrueLxy(dijetTrue): var='jetTrueLxy'; calc='avg'
class dijetTrueCtau(dijetTrue):	var='jetTrueCtau'; calc='avg'
class dijetTrueFlavor(dijetTrue): var='jetTrueFlavor'; calc='avg'
class dijetTrueNLep(dijetTrue):	var='jetTrueNLep'; calc='sum'
class dijetTrueBlxyz(dijetTrue): var='jetTrueBlxyz'; calc='avg'
class dijetTrueXPt(dijetTrue): var='jetTrueXPt'; calc='avg'
class dijetTrueHPt(dijetTrue): var='jetTrueHPt'; calc='avg'
class dijetTrueIP2dMin(dijetTrue): var='jetTrueIp2d'; calc='min'
class dijetTrueIP2dMax(dijetTrue): var='jetTrueIp2d'; calc='max'
class dijetTrueIP3dMin(dijetTrue): var='jetTrueIp3d'; calc='min'
class dijetTrueIP3dMax(dijetTrue): var='jetTrueIp3d'; calc='max'
