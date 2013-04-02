import math,os,sys,pickle,ROOT as r
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def rnd(num,sig_figs):
	if num != 0:
		return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
	else:
		return 0

def stylize(g):
	g[0].SetLineWidth(2)
	g[1].SetLineWidth(2)
	g[1].SetLineStyle(2)
	g[2].SetFillColor(3)
	g[3].SetFillColor(5)
	g[0].SetMarkerStyle(8)
	for graph in g: graph.SetDrawOption('L')

def limitPlot(list = None):
	c=r.TCanvas()
	n=len(list)
	g=[r.TGraph(n),r.TGraph(n),r.TGraph(2*n),r.TGraph(2*n)]
	mg=r.TMultiGraph()
	den=list[0]['exp']
	for i,obj in enumerate(list):
		g[1].SetPoint(i,obj['relErr'],obj['exp']/den)
		g[2].SetPoint(i,obj['relErr'],obj['1ps']/den)
		g[2].SetPoint(2*n-1-i,obj['relErr'],obj['1ms']/den)
		g[3].SetPoint(i,obj['relErr'],obj['2ms']/den)
		g[3].SetPoint(2*n-1-i,obj['relErr'],obj['2ps']/den)

	stylize(g)
	func=r.TF1('func','1+[0]*x + [1]*x*x',0,90)
	func.SetLineWidth(2)
	func.SetMarkerSize(0)
	g[1].Fit('func')
	#mg.Add(g[3],'F')
	mg.Add(g[2],'F')
	mg.Add(g[1],'L')
	mg.SetMaximum(1.2*r.TMath.MaxElement(g[2].GetN(),g[2].GetY()))
	#c.SetLogy()
	#c.SetLogx()
	mg.Draw('A')
	mg.GetXaxis().SetTitle('Systematic uncertainty [%]')
	ctaus=sorted([obj['relErr'] for obj in list])
	mg.GetXaxis().SetRangeUser(ctaus[0]*0.95,ctaus[-1]*2)
	mg.GetYaxis().SetTitle('Limit / Limit (no uncertainty)')

	leg=r.TLegend(0.2,0.61,0.6,0.79)
	leg.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	gempty.SetFillColor(0)
	gempty.SetLineColor(0)
	leg.AddEntry(gempty,'signal efficiency = '+str(dict['eff']*100)+'%')
	leg.AddEntry(g[1],'Exp. Limit','L')
	leg.AddEntry(g[2],'Exp. \\pm 1\\sigma','F')
	#leg.AddEntry(g[3],'Exp. \\pm 2\\sigma','F')
	leg.AddEntry(func,'1 + '+str(rnd(func.GetParameter(0),2))+' x + '+str(rnd(func.GetParameter(1),2))+' x^{2}')
	leg.Draw('same')
	cmsStamp(lumi=None,coords=(0.45,0.89))
	name=str(100*eff)
	os.chdir(plotDir)
	c.SaveAs(name+'percent.eps')
	os.system('epstopdf '+name+'percent.eps')
	os.system('rm '+name+'percent.eps')
	os.chdir('../../')

limDir=sys.argv[1]
plotDir=sys.argv[1]+'/plots'
setupTdrStyle()
r.tdrStyle.SetOptFit(0)

effs=[0.001,0.01,0.1,0.2]

files=[f for f in os.listdir(limDir)]

for eff in effs:
	data=[]
	for f in files:
		items=f.split('_')
		if str(eff)!=items[0] : continue
		dict=pickle.load(open(limDir+'/'+f))
		dict['relErr']=eval(items[1])
		dict['eff']=eff
		data.append(dict)
	from operator import itemgetter
	data=sorted(data,key=itemgetter('relErr'))
        for obj in data:
                print obj['relErr'],obj['eff']

	limitPlot(data)
