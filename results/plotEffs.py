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
	c.SaveAs('eff'+name+'.eps')
	os.system('epstopdf eff'+name+'.eps')
	os.system('rm eff'+name+'.eps')
	os.chdir('../../')

effDir=sys.argv[1]+'/efficiencies/'
plotDir=sys.argv[1]+'/plots/'
files=[f for f in os.listdir(effDir) if '.pkl' in f]
setupTdrStyle()

MH=[1000,1000,400,400,200]
MX=[350,150,150,50,50]
CTAUS=[35,10,4,40,8,20]

for H,X,CTAU in zip(MH,MX,CTAUS):
	data=[]
	for f in files:
		items=f[:-4].split('_')
		h,x,factor=eval(items[1]),eval(items[3]),eval(items[4])
		if h!=H or x!=X : continue
		ctau=factor*CTAU
		dict=pickle.load(open(effDir+f))
		dict['ctau']=ctau
		data.append(dict)
	from operator import itemgetter
	data=sorted(data,key=itemgetter('ctau'))
	for obj in data:
		print obj['ctau']
	effPlot(H,X,data)	


