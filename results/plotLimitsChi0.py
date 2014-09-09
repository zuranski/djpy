import pickle,os,sys,ROOT as r
from operator import itemgetter
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def stylize(g):
	g[0].SetLineWidth(2)
	g[1].SetLineWidth(2)
	g[1].SetLineStyle(2)
	g[2].SetFillColor(3)
	g[3].SetFillColor(5)
	g[0].SetMarkerStyle(8)
	g[4].SetLineWidth(3)
	g[4].SetLineColor(r.kBlue)
	g[4].SetFillStyle(3003)
	g[4].SetFillColor(r.kBlue)
	for graph in g: graph.SetDrawOption('L')

def limitPlot(MH = None,MX = None,list = None,observed=False):
	if MX==148: MX=150
	elif MX==494: MX=500
	print MX
	c=r.TCanvas()
	n=len(list)
	g=[r.TGraph(n),r.TGraph(n),r.TGraph(2*n),r.TGraph(2*n),r.TGraphErrors(n)]
	mg=r.TMultiGraph()
	for i,obj in enumerate(list):
		if observed : g[0].SetPoint(i,obj['ctau'],obj['obs'])
		g[1].SetPoint(i,obj['ctau'],obj['exp'])
		g[2].SetPoint(i,obj['ctau'],obj['1ps'])
		g[2].SetPoint(2*n-1-i,obj['ctau'],obj['1ms'])
		g[3].SetPoint(i,obj['ctau'],obj['2ms'])
		g[3].SetPoint(2*n-1-i,obj['ctau'],obj['2ps'])
		g[4].SetPoint(i,obj['ctau'],obj['sigma'])
		g[4].SetPointError(i,0,obj['sigmaErr']*obj['sigma'])

	stylize(g)
	mg.Add(g[3],'F')
	mg.Add(g[2],'F')
	mg.Add(g[1],'L')
	mg.Add(g[4],'LE3')
	maxg=r.TMath.MaxElement(g[3].GetN(),g[3].GetY())
	ming=r.TMath.MinElement(g[3].GetN(),g[3].GetY())
	mg.SetMaximum((6 if MH in [350,700] else 40)*max(maxg,obj['sigma']))
	mg.SetMinimum(0.5*min(ming,obj['sigma']))
	if observed : mg.Add(g[0],'PL')
	c.SetLogy()
	c.SetLogx()
	mg.Draw('A')
	mg.GetXaxis().SetTitle('#tilde{#chi}^{0}_{1} c#tau [cm]')
	mg.GetXaxis().SetMoreLogLabels()
	mg.GetXaxis().SetNdivisions(303)
	ctaus=sorted([obj['ctau'] for obj in list])
	mg.GetXaxis().SetRangeUser(ctaus[0]*0.95,ctaus[-1]*2)
	if option=='ea':
		#mg.GetYaxis().SetTitle('#sigma #times BR #times Acceptance [pb] (95% CL)')
		mg.GetYaxis().SetTitle('#sigma #times Acceptance [pb] (95% CL)')
	else:
		#mg.GetYaxis().SetTitle('#sigma #times BR [pb] (95% CL)')
		mg.GetYaxis().SetTitle("#sigma(#tilde{q}#tilde{q}*+#tilde{q}#tilde{q}) \
		B^{2}(#tilde{#chi}^{0}_{1} #rightarrow u#bar{d}#mu) [pb]")

	leg=r.TLegend(0.23,0.6 - (0.13 if MH in [350,700] else 0),0.55,0.82 - (0.13 if MH in [350,700] else 0))
	leg.SetFillColor(0)
	leg2=r.TLegend(0.58,0.6 - (0.13 if MH in [350,700] else 0),0.9,0.82 - (0.13 if MH in [350,700] else 0))
	leg2.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg2.AddEntry(gempty,'m_{#tilde{q}} = '+str(MH)+' GeV','P')
	leg2.AddEntry(gempty,'m_{#tilde{#chi}^{0}_{1}} = '+str(MX)+' GeV','P')
	leg2.AddEntry(g[4],'#sigma_{#tilde{q}#tilde{q}*+#tilde{q}#tilde{q}} \\pm 1\\sigma_{theory}','LF')

	
	if observed : leg.AddEntry(g[0],'Observed','PL')
	leg.SetHeader("95% CL limits:")
	leg.AddEntry(g[1],'Expected','L')
	leg.AddEntry(g[2],'Expected \\pm 1\\sigma','F')
	leg.AddEntry(g[3],'Expected \\pm 2\\sigma','F')
	leg.Draw('same')
	leg2.Draw('same')
	cmsStamp(lumi=18510,coords=(0.5,0.87),preliminary=False)
	name=str(MH)+'_'+str(MX)+option
	os.chdir(plotDir)
	c.SaveAs(name+'.eps')
	os.system('epstopdf '+name+'.eps')
	os.system('rm '+name+'.eps')
	os.chdir('../../')

option=sys.argv[3]
limDir=sys.argv[1]+'/limits'+option+'/'
files = [f for f in os.listdir(limDir)]
plotDir=sys.argv[1]+'/plots/'
setupTdrStyle()

CTAUS={(1500,500):17.3,(1000,150):5.9,(350,150):17.8, \
	  (700,150):8.1, (700,500):27.9, (1000,500):22.7, (1500,150):4.5}
MH = [1500, 1000, 700, 350]
THS = [0.00067, 0.0144, 0.139, 9.97]
THERRS = [0.38, 0.24, 0.2, 0.16]
MX = [150, 500]

for i,H in enumerate(MH):
	TH=THS[i]
	THERR=THERRS[i]
	for X in MX:
		if X>H : continue
		print H,X
		CTAU = CTAUS[(H,X)]	
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

