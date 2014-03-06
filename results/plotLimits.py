import pickle,os,sys,ROOT as r
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def stylize(g):
	g[0].SetLineWidth(2)
	g[1].SetLineWidth(2)
	g[1].SetLineStyle(2)
	g[2].SetFillColor(3)
	g[3].SetFillColor(5)
	g[0].SetMarkerStyle(8)
	for graph in g: graph.SetDrawOption('L')

def limitPlot(MH = None,MX = None,list = None,observed=False):
	c=r.TCanvas()
	n=len(list)
	g=[r.TGraph(n),r.TGraph(n),r.TGraph(2*n),r.TGraph(2*n)]
	mg=r.TMultiGraph()
	for i,obj in enumerate(list):
		if observed : g[0].SetPoint(i,obj['ctau'],obj['obs'])
		g[1].SetPoint(i,obj['ctau'],obj['exp'])
		g[2].SetPoint(i,obj['ctau'],obj['1ps'])
		g[2].SetPoint(2*n-1-i,obj['ctau'],obj['1ms'])
		g[3].SetPoint(i,obj['ctau'],obj['2ms'])
		g[3].SetPoint(2*n-1-i,obj['ctau'],obj['2ps'])

	stylize(g)
	mg.Add(g[3],'F')
	mg.Add(g[2],'F')
	mg.Add(g[1],'L')
	mg.SetMaximum(50*r.TMath.MaxElement(g[3].GetN(),g[3].GetY()))
	if observed : mg.Add(g[0],'PL')
	c.SetLogy()
	c.SetLogx()
	mg.Draw('A')
	mg.GetXaxis().SetTitle('X^{0} c#tau [cm]')
	ctaus=sorted([obj['ctau'] for obj in list])
	mg.GetXaxis().SetRangeUser(ctaus[0]*0.95,ctaus[-1]*2)
	if option=='ea':
		#mg.GetYaxis().SetTitle('#sigma #times BR #times Acceptance [pb] (95% CL)')
		mg.GetYaxis().SetTitle('#sigma B^{2} #times Acceptance [pb] (95% CL)')
	else:
		#mg.GetYaxis().SetTitle('#sigma #times BR [pb] (95% CL)')
		mg.GetYaxis().SetTitle('#sigma(H^{0} #rightarrow X^{0}X^{0}) B^{2}(X^{0} #rightarrow q#bar{q}) [pb]')

	leg=r.TLegend(0.23,0.51,0.60,0.79)
	leg.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg.AddEntry(gempty,'m_{H^{0}} = '+str(MH)+' GeV','P')
	leg.AddEntry(gempty,'m_{X^{0}} = '+str(MX)+' GeV','P')
	if observed : leg.AddEntry(g[0],'Obs. Limit','L')
	leg.AddEntry(g[1],'Exp. Limit','L')
	leg.AddEntry(g[2],'Exp. \\pm 1\\sigma','F')
	leg.AddEntry(g[3],'Exp. \\pm 2\\sigma','F')
	leg.Draw('same')
	cmsStamp(lumi=18510,coords=(0.45,0.87),preliminary=False)
	name=str(MH)+'_'+str(MX)+option
	os.chdir(plotDir)
	c.SaveAs(name+'.eps')
	os.system('epstopdf '+name+'.eps')
	os.system('rm '+name+'.eps')
	os.chdir('../../')

option=sys.argv[3]
limDir=sys.argv[1]+'/limits'+option+'/'
plotDir=sys.argv[1]+'/plots/'
files=[f for f in os.listdir(limDir) if '.pkl' in f]
setupTdrStyle()

MH=[1000,1000,400,400,200]
MX=[350,150,150,50,50]
CTAUS=[35,10,40,8,20]

for H,X,CTAU in zip(MH,MX,CTAUS):
	data=[]
	for f in files:
		items=f[:-4].split('_')
		h,x,factor=eval(items[1]),eval(items[3]),eval(items[4])
		if h!=H or x!=X : continue
		ctau=factor*CTAU
		dict=pickle.load(open(limDir+f))
		dict['ctau']=ctau
		data.append(dict)
	from operator import itemgetter
	data=sorted(data,key=itemgetter('ctau'))
	for obj in data:
		print obj['ctau']
	limitPlot(H,X,data,eval(sys.argv[2]))	


