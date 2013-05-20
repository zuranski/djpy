from supy import analysisStep
import math
from calculables.utils import DeltaR,DeltaPhi

class general(analysisStep):
	def uponAcceptance(self,e):

		XtoJets=[6001114,6002114,6003114]

		dR1 = DeltaR(e['genqEta'][0],e['genqPhi'][0],e['genqEta'][1],e['genqPhi'][1])
		dR2 = DeltaR(e['genqEta'][2],e['genqPhi'][2],e['genqEta'][3],e['genqPhi'][3])
		dPhi1 = DeltaPhi(e['genqPhi'][0],e['genqPhi'][1])
		dPhi2 = DeltaPhi(e['genqPhi'][2],e['genqPhi'][3])

		idx1,idx2=None,None
		try:
			idx1=e['dijetTrueLxy'].index(e['genqLxy'][0])
		except ValueError: pass
		try:
			idx2=e['dijetTrueLxy'].index(e['genqLxy'][2])
		except ValueError: pass

		w1 = 1 if idx1 is not None else 0
		w2 = 1 if idx2 is not None else 0

		if (e['genqLxy'][0]<60 
		and e['genqPt'][0]>50 
	    and e['genqPt'][1]>50
		and dR1<0.8 
        and abs(e['genqEta'][0])<1.8
        and abs(e['genqEta'][1])<1.8
		and e['XpdgId'][0] in XtoJets):
			self.book.fill(len(e['genjetLxy1']),'nnmerging',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 
			self.book.fill((len(e['genjetLxy1']),dR1),'ndR',(4,20),(-0.5,0.),(3.5,5.),None,title='genJets ; n ; events/bin') 
			self.book.fill(dR1,'dRnum',12,0.2,.8,w=w1,title='')
			self.book.fill(dR1,'dRdenom',12,0.2,.8,w=None,title='')
			if idx1 is not None:
				self.book.fill(DeltaPhi(e['dijetPhi'][idx1],e['XPhi'][0]),'dPhi',50,-1.,1.,None,title=' ; #Delta #phi (dijet, X); dijets/bin')
				self.book.fill(DeltaPhi(e['dijetPhi'][idx1],e['XPhi'][0])/dPhi1,'dPhiReduced',50,-1.,1.,None,title=' ; #Delta #phi (dijet, X) / #Delta #phi (q#bar{q}); dijets/bin')
				self.book.fill((DeltaPhi(e['dijetPhi'][idx1],e['XPhi'][0]),e['genqLxy'][0]),'dPhiLxy',(50,25),(-1.,0),(1.,50),None,title='X^{0} / bin ; #Delta #phi (dijet, X); L_{xy}[cm]')

		if (e['genqLxy'][2]<60 
        and e['genqPt'][2]>50
        and e['genqPt'][3]>50 
		and dR2<0.8 
        and abs(e['genqEta'][2])<1.8 
        and abs(e['genqEta'][3])<1.8
		and e['XpdgId'][1] in XtoJets):
			self.book.fill(len(e['genjetLxy2']),'nnmerging',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 
			self.book.fill((len(e['genjetLxy2']),dR2),'ndR',(4,20),(-0.5,0.),(3.5,5.),None,title='genJets ; n ; events/bin') 
			self.book.fill(dR2,'dRnum',12,0.2,.8,w=w2,title='')
			self.book.fill(dR2,'dRdenom',12,0.2,.8,w=None,title='')
			if idx2 is not None:
				self.book.fill(DeltaPhi(e['dijetPhi'][idx2],e['XPhi'][1]),'dPhi',50,-1.,1.,None,title=' ; #Delta #phi (dijet, X); dijets/bin')
				self.book.fill(DeltaPhi(e['dijetPhi'][idx2],e['XPhi'][1])/dPhi2,'dPhiReduced',50,-1.,1.,None,title=' ; #Delta #phi (dijet, X) / #Delta #phi (q#bar{q}); dijets/bin')
				self.book.fill((DeltaPhi(e['dijetPhi'][idx2],e['XPhi'][1]),e['genqLxy'][2]),'dPhiLxy',(50,25),(-1.,0),(1.,50),None,title='X^{0} / bin ; #Delta #phi (dijet, X); L_{xy}[cm]')
