import pickle,os,sys,ROOT as r
from operator import itemgetter
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def stylize(gs,obs,exp):
	gs.SetLineWidth(3); gs.SetLineColor(r.kBlue)
	gs.SetFillStyle(3003); gs.SetFillColor(r.kBlue)
	for e in exp: e.SetFillColor(3)
	for i,o in enumerate(obs): 
		o.SetLineWidth(2); o.SetMarkerStyle(20+i)
		o.SetMarkerColor(i+1); o.SetLineColor(i+1)

def makePlot(data):
	c=r.TCanvas();c.SetLogx();c.SetLogy()
	mg=r.TMultiGraph()
	gs=r.TGraphErrors()
	obs=[r.TGraph() for i in range(len(data['graphs']))]
	exp=[r.TGraph() for i in range(len(data['graphs']))]
	stylize(gs,obs,exp)
	leg=r.TLegend(0.23,0.6 - (0.13 if H in [350,700] else 0),0.55,0.82 - (0.13 if H in [350,700] else 0))
	leg2=r.TLegend(0.58,0.7 - (0.13 if H in [350,700] else 0),0.9,0.82 - (0.13 if H in [350,700] else 0))
	leg.SetFillColor(0);leg2.SetFillColor(0)
	leg.SetHeader("95% CL limits:")
	leg2.SetTextFont(62)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg2.AddEntry(gempty,'m_{#tilde{q}} = '+str(data['H'])+' GeV','P')

	for i,graph in enumerate(data['graphs']):
		points = graph['points']
		n=len(points)
		for j,(ctau,lim) in enumerate(points):
			gs.SetPoint(gs.GetN(),ctau,data['sigma'])
			gs.SetPointError(gs.GetN()-1,0,data['sigmaErr'])
			obs[i].SetPoint(j,ctau,lim['obs'])
			print data['H'], graph['X'], ctau, lim['obs']*1000
			exp[i].SetPoint(j,ctau,lim['1ps'])
			exp[i].SetPoint(2*n-1-j,ctau,lim['1ms'])
		
		leg.AddEntry(obs[i],'m_{#tilde{#chi}^{0}_{1}}=%s GeV' %graph['X'],'PL')

	for i in range(len(data['graphs'])): mg.Add(exp[i],'F')
	for i in range(len(data['graphs'])): mg.Add(obs[i],'LP')
	
	leg.AddEntry(exp[0],'Exp. limits (\\pm 1\\sigma)','F')
	leg.AddEntry(gs,'#sigma_{#tilde{q}#tilde{q}*+#tilde{q}#tilde{q}} \\pm 1\\sigma_{theory}','LF')
	mg.Add(gs,'LE3')
	cmsStamp(lumi=18510,coords=(0.5,0.87),preliminary=False)
	mg.Draw('A')
	mg.SetMaximum((8 if H in [350,700] else 40)*max(data['sigma'],max([r.TMath.MaxElement(e.GetN(),e.GetY()) for e in exp])))
	gmin,gmax = r.TMath.MinElement(gs.GetN(),gs.GetX()),r.TMath.MaxElement(gs.GetN(),gs.GetX())
	mg.GetXaxis().SetRangeUser(0.95*gmin,2*gmax)
	mg.GetXaxis().SetMoreLogLabels()
	mg.GetYaxis().SetTitle("#sigma(#tilde{q}#tilde{q}*+#tilde{q}#tilde{q}) \
    B^{2}(#tilde{#chi}^{0}_{1} #rightarrow u#bar{d}#mu) [pb]")
	mg.GetXaxis().SetTitle('#tilde{#chi}^{0}_{1} c#tau [cm]')
	leg.Draw('same')
	leg2.Draw('same')

	name=str(data['H'])
	c.SaveAs(name+'.eps')
	os.system('epstopdf '+name+'.eps && rm '+name+'.eps && mv '+name+'.pdf '+plotDir)

limDir=sys.argv[1]+'/limitse/'
plotDir=sys.argv[1]+'/plots/'
setupTdrStyle()

CTAUS={(1500,500):17.3,(1000,150):5.9,(350,150):17.8, \
	  (700,150):8.1, (700,500):27.9, (1000,500):22.7, (1500,150):4.5}
MH = [1500, 1000, 700, 350]
THS = [0.00067, 0.0144, 0.139, 9.97]
THERRS = [0.38, 0.24, 0.2, 0.16]
MX = [150, 500]

alldata = {}
for f in os.listdir(limDir):
	_, H, _, X, factor = f.replace('.pkl','').split('_') # extract numbers
	key = (eval(H), eval(X), eval(factor)*CTAUS[(eval(H),eval(X))]) # construct a key
	alldata[key] = pickle.load(open(limDir + f))

for i,H in enumerate(MH):

	graphs = []
	for X in MX:
		if X>H: continue
		keys = sorted([k for k in alldata.keys() if H in k and X in k] , key=itemgetter(2))
		graphs.append({'X':X, 'points':[(k[2],alldata[k]) for k in keys]})
	
	data = {'H':H,'sigma':THS[i],'sigmaErr':THERRS[i]*THS[i], 'graphs':graphs}

	makePlot(data)
