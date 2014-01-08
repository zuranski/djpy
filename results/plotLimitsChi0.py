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

	f=r.TF1('sigma','pol0(0)',1e-5,1e5)
	f.SetParameter(0,obj['sigma'])
	f.SetLineColor(r.kBlue)
	f.SetLineStyle(1)
	f.SetLineWidth(3)
	f.SetMarkerSize(0)
	f1=r.TF1('sigmaup','pol0(0)',1e-5,1e5)
	f1.SetParameter(0,obj['sigma']*(1+obj['sigmaErr']))
	f1.SetLineColor(r.kBlue)
	f1.SetLineStyle(2)
	f1.SetLineWidth(3)
	f2=r.TF1('sigmaup','pol0(0)',1e-5,1e5)
	f2.SetParameter(0,obj['sigma']*(1-obj['sigmaErr']))
	f2.SetLineColor(r.kBlue)
	f2.SetLineStyle(2)
	f2.SetLineWidth(3)

	stylize(g)
	mg.Add(g[3],'F')
	mg.Add(g[2],'F')
	mg.Add(g[1],'L')
	maxg=r.TMath.MaxElement(g[3].GetN(),g[3].GetY())
	ming=r.TMath.MinElement(g[3].GetN(),g[3].GetY())
	mg.SetMaximum(10*max(maxg,obj['sigma']))
	mg.SetMinimum(0.6*min(ming,obj['sigma']))
	if observed : mg.Add(g[0],'PL')
	c.SetLogy()
	c.SetLogx()
	mg.Draw('A')
	f.Draw('Lsame')
	f1.Draw('Lsame')
	f2.Draw('Lsame')
	mg.GetXaxis().SetTitle('c#tau [cm]')
	mg.GetXaxis().SetMoreLogLabels()
	mg.GetXaxis().SetNdivisions(303)
	ctaus=sorted([obj['ctau'] for obj in list])
	mg.GetXaxis().SetRangeUser(ctaus[0]*0.95,ctaus[-1]*2)
	if option=='ea':
		#mg.GetYaxis().SetTitle('#sigma #times BR #times Acceptance [pb] (95% CL)')
		mg.GetYaxis().SetTitle('#sigma #times Acceptance [pb] (95% CL)')
	else:
		#mg.GetYaxis().SetTitle('#sigma #times BR [pb] (95% CL)')
		mg.GetYaxis().SetTitle('#sigma_{#tilde{q}#tilde{q}} B^{2}(#tilde{#chi}^{0} #rightarrow #muq#bar{q}) [pb] (95% CL)')

	leg=r.TLegend(0.23,0.45,0.6,0.62)
	leg.SetFillColor(0)
	leg2=r.TLegend(0.62,0.51,0.85,0.62)
	leg2.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg2.AddEntry(gempty,'m_{#tilde{q}} = '+str(MH)+' GeV','P')
	leg2.AddEntry(gempty,'m_{#tilde{#chi}^{0}} = '+str(MX)+' GeV','P')
	leg.AddEntry(f,'#sigma_{#tilde{q}#tilde{q}} (NLO-NLL) \\pm 1\\sigma_{theory}','L')
	
	if observed : leg.AddEntry(g[0],'Obs. Limit','PL')
	leg.AddEntry(g[1],'Exp. Limit','L')
	leg.AddEntry(g[2],'Exp. \\pm 1\\sigma','F')
	leg.AddEntry(g[3],'Exp. \\pm 2\\sigma','F')
	leg.Draw('same')
	leg2.Draw('same')
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

MH=[1500,1000,350,120]
MX=[494,148,148,48]
CTAUS=[18.1,5.85,18.8,15.5]
THS=[0.00067,0.0144,9.97,284]
#THERRS=[0.15,0.13,0.16,0.10] # scale only
THERRS=[0.38,0.24,0.16,0.10]

for H,X,CTAU,TH,THERR in zip(MH,MX,CTAUS,THS,THERRS):
	data=[]
	for f in files:
		items=f[:-4].split('_')
		h,x,factor=eval(items[1]),eval(items[3]),eval(items[4])
		if h!=H or x!=X : continue
		ctau=factor*CTAU
		dict=pickle.load(open(limDir+f))
		dict['ctau']=ctau
		dict['sigma']=TH
		dict['sigmaErr']=THERR
		data.append(dict)
	from operator import itemgetter
	data=sorted(data,key=itemgetter('ctau'))
	for obj in data:
		print obj['ctau']
	limitPlot(H,X,data,eval(sys.argv[2]))	


