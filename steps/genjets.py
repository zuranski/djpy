from supy import analysisStep
import math

class general(analysisStep):
	def uponAcceptance(self,e):
		n1=sum([1 if e['genjetPt1'][i]>0 and abs(e['genjetEta1'][i])<5 else 0 for i,lxy in enumerate(e['genjetLxy1']) ])
		n2=sum([1 if e['genjetPt2'][i]>0 and abs(e['genjetEta2'][i])<5 else 0 for i,lxy in enumerate(e['genjetLxy2']) ])

		if e['genqLxy'][0]<50:
			self.book.fill(n1,'n',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 
		if e['genqLxy'][2]<50:
			self.book.fill(n2,'n',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 

		XtoJets=[6001114,6002114,6003114]

		if (e['genqLxy'][0]<50 
		and e['genqPt'][0]>40 
	    and e['genqPt'][1]>40 
        and abs(e['genqEta'][0])<2
        and abs(e['genqEta'][1])<2
		and e['XpdgId'][0] in XtoJets):
			self.book.fill(len(e['genjetLxy1']),'nnmerging',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 
		if (e['genqLxy'][2]<50 
        and e['genqPt'][2]>40
        and e['genqPt'][3]>40 
        and abs(e['genqEta'][2])<2 
        and abs(e['genqEta'][3])<2
		and e['XpdgId'][1] in XtoJets):
			self.book.fill(len(e['genjetLxy2']),'nnmerging',4,-0.5,3.5,None,title='genJets ; n ; events/bin') 
