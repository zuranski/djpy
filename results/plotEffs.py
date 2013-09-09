import pickle,os,sys,ROOT as r
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def effPlot(MH = None,MX = None,list = None):
	c=r.TCanvas()
	g=r.TGraphErrors(len(list))
	for i,obj in enumerate(list):
		print obj
		g.SetPoint(i,obj['ctau'],obj['eff'][0])
		g.SetPointError(i,0,obj['eff'][1])
	
	g.SetMarkerStyle(8)
	c.SetLogy()
	c.SetLogx()
	g.Draw('AP')
	g.GetXaxis().SetTitle('c#tau [cm]')
	ctaus=sorted([obj['ctau'] for obj in list])
	g.GetXaxis().SetRangeUser(ctaus[0]*0.95,ctaus[-1]*2)
	if 'acceptance' in plotDir:
		g.GetYaxis().SetTitle('efficiency in acceptance')
	else:
		g.GetYaxis().SetTitle('efficiency')

	leg=r.TLegend(0.2,0.31,0.5,0.49)
	leg.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg.AddEntry(gempty,'m_{H} = '+str(MH)+' GeV/c^{2}','P')
	leg.AddEntry(gempty,'m_{X} = '+str(MX)+' GeV/c^{2}','P')
	leg.Draw('same')

	name=str(MH)+'_'+str(MX)
	os.chdir(plotDir)
	fname=dictionary[option][0]+name
	c.SaveAs(fname+'.eps')
	os.system('epstopdf '+fname+'.eps')
	os.system('rm '+fname+'.eps')
	os.chdir('../../')

option=sys.argv[2]
dictionary={'e':('eff',1),'a':('acc',0),'ea':('effacc',2)}

effDir=sys.argv[1]+'/efficiencies/'
plotDir=sys.argv[1]+'/plots/'
files=[f for f in os.listdir(effDir) if '.pkl' in f]
setupTdrStyle()

MH=[1000,1000,400,400,200]
MX=[350,150,150,50,50]
CTAUS=[35,10,4,40,8,20]

MH=[1500,1000,350,120]
MX=[494,148,148,48]
CTAUS=[1,1,1,1]

for H,X,CTAU in zip(MH,MX,CTAUS):
	data=[]
	for f in files:
		items=f[:-4].split('_')
		h,x,factor=eval(items[1]),eval(items[3]),eval(items[4])
		if h!=H or x!=X : continue
		ctau=factor*CTAU
		eff=pickle.load(open(effDir+f))[dictionary[option][1]]
		dict={'eff':eff}
		dict['ctau']=ctau
		data.append(dict)
	from operator import itemgetter
	data=sorted(data,key=itemgetter('ctau'))
	for obj in data:
		print obj['ctau']
	effPlot(H,X,data)	


