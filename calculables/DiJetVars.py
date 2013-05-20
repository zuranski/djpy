from supy import wrappedChain

class dijetJetVar(wrappedChain.calculable):
	fixes=('dijet','')
	def update(self,ignored):
		self.value = [self.source['jet'+self.var][self.source['dijetIdx'+str(self.jet)][idx]] for idx in self.source['dijetIndices']]

class Pt1(dijetJetVar): var='Pt';jet=1
class Pt2(dijetJetVar): var='Pt';jet=2
class dijetPt1Up(dijetJetVar): var='PtUp';jet=1
class dijetPt2Up(dijetJetVar): var='PtUp';jet=2
class dijetPt1Down(dijetJetVar): var='PtDown';jet=1
class dijetPt2Down(dijetJetVar): var='PtDown';jet=2
class dijetPt1Bias(dijetJetVar): var='PtBias';jet=1
class dijetPt2Bias(dijetJetVar): var='PtBias';jet=2
class PromptEnergyFrac1(dijetJetVar): var='PromptEnergyFrac';jet=1
class PromptEnergyFrac2(dijetJetVar): var='PromptEnergyFrac';jet=2
class NPromptTracks1(dijetJetVar): var='NPromptTracks';jet=1
class NPromptTracks2(dijetJetVar): var='NPromptTracks';jet=2

class dijetVar(wrappedChain.calculable):
	fixes=('dijet','')
	def update(self,ignored): self.value=[self.calculate(idx) for idx in self.source['dijetIndices']]

class VtxNRatio(dijetVar):
	def calculate(self,idx):
		VtxN=self.source['dijetVtxN'][idx]
		N=self.source['dijetNDispTracks'][idx]
		return VtxN/N if N>0 else -1

class VtxDelta(dijetVar):
	def calculate(self,idx):
		VtxN1=self.source['dijetVtxN1'][idx]
		VtxN2=self.source['dijetVtxN2'][idx]
		VtxN=self.source['dijetVtxN'][idx]
		return abs(VtxN1-VtxN2)/VtxN if VtxN>0 else -1

class VtxptRatio(dijetVar):
	def calculate(self,idx):
		vtxPt=self.source['dijetVtxPt'][idx]
		dijetPt=self.source['dijetPt'][idx]
		return vtxPt/dijetPt

class DR(dijetVar):
	def calculate(self,idx):
		return DeltaR(
                      self.source['jetEta'][self.source['dijetIdx1'][idx]],
                      self.source['jetPhi'][self.source['dijetIdx1'][idx]],
                      self.source['jetEta'][self.source['dijetIdx2'][idx]],
                      self.source['jetPhi'][self.source['dijetIdx2'][idx]]
                     ) 

class Ctau(dijetVar):
	def calculate(self,idx):
		x=self.source['dijetVtxX'][idx]
		y=self.source['dijetVtxY'][idx]
		z=self.source['dijetVtxZ'][idx]
		pt=self.source['dijetPt'][idx]
		eta=self.source['dijetEta'][idx]
		m=self.source['dijetMass'][idx]
		R=math.sqrt(x*x+y*y+z*z)
		return R*m/(pt*math.cosh(eta))
