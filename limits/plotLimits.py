import pickle,os,sys,ROOT as r
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def stylize(g):
	for graph in g: graph.SetLineWidth(2)
	g[0].SetLineStyle(2)
	g[1].SetFillColor(3)
	g[2].SetFillColor(5)
	for graph in g: graph.SetDrawOption('L')

def limitPlot(MH = None,MX = None):
	c=r.TCanvas()
	list = [obj for obj in dict if (eval(obj['H'])==MH and eval(obj['X'])==MX and obj['eff']>0)]
	n=len(list)
	g=[r.TGraph(n),r.TGraph(2*n),r.TGraph(2*n)]
	mg=r.TMultiGraph()
	for i,obj in enumerate(list):
		g[0].SetPoint(i,obj['ctau'],obj['explim'])
		g[1].SetPoint(i,obj['ctau'],obj['p1s'])
		g[1].SetPoint(2*n-1-i,obj['ctau'],obj['m1s'])
		g[2].SetPoint(i,obj['ctau'],obj['m2s'])
		g[2].SetPoint(2*n-1-i,obj['ctau'],obj['p2s'])

	stylize(g)
	mg.Add(g[2],'F')
	mg.Add(g[1],'F')
	mg.Add(g[0],'L')
	c.SetLogy()
	c.SetLogx()
	mg.Draw('A')
	mg.GetXaxis().SetTitle('c#tau [cm]')
	mg.GetYaxis().SetTitle('#sigma #times BR [pb] (95% CL)')

	leg=r.TLegend(0.2,0.54,0.55,0.75)
	leg.SetFillColor(0)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg.AddEntry(gempty,'m_{H} = '+str(MH)+' GeV/c^{2}','P')
	leg.AddEntry(gempty,'m_{X} = '+str(MX)+' GeV/c^{2}','P')
	leg.AddEntry(g[0],'Exp. Limit','L')
	leg.AddEntry(g[1],'Exp. \\pm 1\\sigma','F')
	leg.AddEntry(g[2],'Exp. \\pm 2\\sigma','F')
	leg.Draw('same')
	cmsStamp(lumi=11317,coords=(0.45,0.89))
	name=str(MH)+'_'+str(MX)
	os.chdir('/scratch/lustre/zuranski/limits/')
	c.SaveAs(name+'.eps')
	os.system('epstopdf '+name+'.eps')
	os.system('rm '+name+'.eps')

dict = pickle.load(open('../data/limits.pkl','r'))
setupTdrStyle()

MH=[1000,1000,1000,400,400,200]
MX=[350,150,50,150,50,50]

for H,X in zip(MH,MX):
        limitPlot(H,X)
