import pickle,os,sys,ROOT as r
from operator import itemgetter
from supy.__plotter__ import setupTdrStyle
from supy.utils import cmsStamp

def stylize(obs,exp):
	for e in exp: e.SetFillColor(3)
	for i,o in enumerate(obs): 
		o.SetLineWidth(2); o.SetMarkerStyle(20+i)
		o.SetMarkerColor(i+1); o.SetLineColor(i+1)

def makePlot(data):
	c=r.TCanvas();c.SetLogx();c.SetLogy()
	r.gPad.SetTopMargin(0.06)
	r.gPad.SetBottomMargin(0.15)
	r.gPad.SetLeftMargin(0.2)
	mg=r.TMultiGraph()
	obs=[r.TGraph() for i in range(len(data['graphs']))]
	exp=[r.TGraph() for i in range(len(data['graphs']))]
	stylize(obs,exp)
	leg=r.TLegend(0.23,0.62 - (0.13 if H in [350,700] else 0),0.55,0.82 - (0.13 if H in [350,700] else 0))
	leg2=r.TLegend(0.58,0.7 - (0.13 if H in [350,700] else 0),0.9,0.82 - (0.13 if H in [350,700] else 0))
	leg.SetFillColor(0);leg2.SetFillColor(0)
	leg.SetHeader("95% CL limits:")
	leg2.SetTextFont(62)
	gempty=r.TGraph()
	gempty.SetMarkerColor(0)
	leg2.AddEntry(gempty,'m_{H^{0}} = '+str(data['H'])+' GeV','P')

	for i,graph in enumerate(data['graphs']):
		points = graph['points']
		n=len(points)
		for j,(ctau,lim) in enumerate(points):
			obs[i].SetPoint(j,ctau,lim['obs'])
			exp[i].SetPoint(j,ctau,lim['1ps'])
			exp[i].SetPoint(2*n-1-j,ctau,lim['1ms'])
		
		leg.AddEntry(obs[i],'m_{X^{0}}=%s GeV' %graph['X'],'PL')

	for i in range(len(data['graphs'])): mg.Add(exp[i],'F')
	for i in range(len(data['graphs'])): mg.Add(obs[i],'PL')
	
	leg.AddEntry(exp[0],'Exp. limits (\\pm 1\\sigma)','F')
	cmsStamp(lumi=18510,coords=(0.5,0.87),preliminary=False)
	mg.Draw('A')
	mg.SetMaximum(40*max([r.TMath.MaxElement(e.GetN(),e.GetY()) for e in exp]))
	mg.GetYaxis().SetTitle('#sigma(H^{0} #rightarrow X^{0}X^{0}) B^{2}(X^{0} #rightarrow q#bar{q}) [pb]')
	mg.GetXaxis().SetTitle('X^{0} c#tau [cm]')
	mg.GetXaxis().SetTitleOffset(1.4)
	mg.GetYaxis().SetTitleOffset(1.8)
	leg.Draw('same')
	leg2.Draw('same')

	name=str(data['H'])
	c.SaveAs(name+'.eps')
	os.system('epstopdf '+name+'.eps && rm '+name+'.eps && mv '+name+'.pdf '+plotDir)

limDir=sys.argv[1]+'/limitse/'
plotDir=sys.argv[1]+'/plots/'
setupTdrStyle()

CTAUS={(1000,350):35,(1000,150):10,(400,150):40, \
	  (400,50):8, (200,50):20}
MH = [1000, 400, 200]
MX = [350, 150, 50]

35,10,40,8,20

alldata = {}
for f in os.listdir(limDir):
	_, H, _, X, factor = f.replace('.pkl','').split('_') # extract numbers
	key = (eval(H), eval(X), eval(factor)*CTAUS[(eval(H),eval(X))]) # construct a key
	alldata[key] = pickle.load(open(limDir + f))

for i,H in enumerate(MH):

	graphs = []
	for X in reversed(MX):
		if 2*X>H or X/float(H)<0.1: continue
		keys = sorted([k for k in alldata.keys() if H in k and X in k] , key=itemgetter(2))
		graphs.append({'X':X, 'points':[(k[2],alldata[k]) for k in keys]})
	
	data = {'H':H,'graphs':graphs}

	makePlot(data)
