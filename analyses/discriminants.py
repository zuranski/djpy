import itertools,supy,samples,calculables,steps,ROOT as r
from calculables.utils import getCounts,listdiff

class discriminants(supy.analysis) :
    
	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate=['dijetVtxNRatio']
	ToCalculate += ['dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']

	IniCuts=[
        {'name':'dijet'},
        {'name':'dijetTrueLxy','min':0},
        # vertex minimal
        {'name':'dijetVtxChi2','min':0,'max':4},
        {'name':'dijetVtxN1','min':1},
        {'name':'dijetVtxN2','min':1},
        # cluster minimal
        {'name':'dijetbestclusterN','min':2},
    ]
	Cuts=[
        # clean up cuts 
        #{'name':'dijetNAvgMissHitsAfterVert','max':1.99},
        {'name':'dijetVtxmass','min':5},
        {'name':'dijetVtxpt','min':10},
        {'name':'dijetVtxNRatio','min':0.1},
        {'name':'dijetLxysig','min':8},
        {'name':'dijetNoOverlaps','val':True},
    ]
	ABCDCutsSets = []
	scanPrompt = [(5,0.35),(4,0.3),(3,0.2),(2,0.15)]
	scanVtx = [0.01,0.05,0.1,0.2,0.4,0.65,0.9]

	scan = [obj for obj in itertools.product(scanPrompt,scanPrompt,scanVtx)]

	for val in scan :
		ABCDCutsSets.append([
		{'name':'Prompt1','vars':({'name':'dijetNPromptTracks1','max':val[0][0]},
   	                              {'name':'dijetPromptEnergyFrac1','max':val[0][1]})
		},
		{'name':'Prompt2','vars':({'name':'dijetNPromptTracks2','max':val[1][0]},
	                              {'name':'dijetPromptEnergyFrac2','max':val[1][1]})
		},
		{'name':'Disc','vars':({'name':'dijetDiscriminant','min':val[2]},)},
		])	
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut is self.Cuts[-1]:
				mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.ABCDvars(indices=cut['name']+'Indices',plot2D=True))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for i in range(len(self.ABCDCutsSets)) :
			mysteps.append(steps.plots.ABCDEFGHplots(indices='ABCDEFGHIndices'+str(i)))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts + self.ABCDCutsSets[-1]
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for i in range(len(self.ABCDCutsSets)) :
			calcs.append(calculables.Indices.ABCDEFGHIndices(indices=self.Cuts[-1]['name']+'Indices',
															 cuts=self.ABCDCutsSets[i],suffix=str(i)))
		return calcs

	def discs(self):
		discSamplesRight=[name+'.pileupPUInteractionsBX0Target' for name in self.sig_names]
		discSamplesLeft=[name+'.pileupPUInteractionsBX0Target' for name in self.qcd_names]
		return([supy.calculables.other.Discriminant(fixes=("dijet",""),
													right = {"pre":"H","tag":"","samples":discSamplesRight},
													left = {"pre":"qcd","tag":"","samples":discSamplesLeft},
													dists = {"dijetVtxN":(7,1.5,8.5),
															 "dijetglxyrmsclr": (10,0,1),
															 "dijetbestclusterN": (7,1.5,8.5),
															 "dijetPosip2dFrac": (5,0.5001,1.001),
															},
													indices=self.Cuts[-1]['name']+'Indices',
													bins = 14),
			   ])

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)('dijetVtxChi2Indices'))
		calcs.append(calculables.Overlaps.dijetNoOverlaps('dijetLxysigIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),

			### filters
			supy.steps.filters.label('data cleanup'),
			supy.steps.filters.value('primaryVertexFilterFlag',min=1),
            supy.steps.filters.value('physicsDeclaredFilterFlag',min=1).onlyData(),
            supy.steps.filters.value('beamScrapingFilterFlag',min=1),
            supy.steps.filters.value('beamHaloTightFilterFlag',min=1),
            supy.steps.filters.value('hbheNoiseFilterFlag',min=1),
            supy.steps.filters.value('hcalLaserEventFilterFlag',min=1),
            supy.steps.filters.value('ecalLaserCorrFilterFlag',min=1),
            supy.steps.filters.value('eeBadScFilterFlag',min=1),
            supy.steps.filters.value('ecalDeadCellTPFilterFlag',min=1),
            supy.steps.filters.value('trackingFailureFilterFlag',min=1),
			]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupPUInteractionsBX0",thisSample=config['baseSample'],
				target=("data//HT300_R12BC_observed.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT300_v"),
			supy.steps.filters.value("caloHT",min=325),]

			### plots
			+[steps.event.general()]
			+self.dijetSteps1()
			+self.discs()
			+self.dijetSteps2()
			)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
			+self.calcsIndices()
			+self.calcsVars()
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all

		qcd_samples = []
		sig_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupPUInteractionsBX0Target']))
		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupPUInteractionsBX0Target']))

		return (qcd_samples
			    + sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		#plotter.plotAll()
		self.plotABCDscan(org,plotter)

	def plotABCDscan(self,org,plotter):
		plotter.pdfFileName = plotter.pdfFileName.replace(self.name+'.pdf','abcd_scan.pdf')
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		text2 = plotter.printNEventsIn()
		plotter.flushPage()
		r.gPad.SetLogy()
		if not plotter.anMode : r.gPad.SetRightMargin(0.15)
		# get all the counts
		counts = [[0]*len(self.scan) for sample in org.samples]
		for step in org.steps : 
			for plotName in sorted(step.keys()) :
				if 'ABCDEFGHcounts' not in plotName: continue
				i = eval(plotName[:plotName.find('ABCDEFGH')])
				for j in range(len(org.samples)): counts[j][i] = getCounts(step[plotName][j])

		# plot scans
		scans=[(self.scanPrompt[0],self.scanPrompt[0],None),
               (self.scanPrompt[0],None,self.scanVtx[0]),
               (None,self.scanPrompt[0],self.scanVtx[0])]
		names = ['observed','FG/B','EG/C','DG/A','BE/A','CF/A','EF/D']
		for i,scan in enumerate(scans):
			list = [(a,obj[scan.index(None)]) for a,obj in enumerate(self.scan) if len(listdiff(obj,scan))<=1]
			labels = ['('+','.join(str(a) for a in obj[1])+')' if type(obj[1])==tuple else str(obj[1]) for obj in list]
			graphs = [tuple([r.TGraphErrors(len(list)) for sample in org.samples]) for i in range(7)]
			for j in range(len(org.samples)):
				for k in range(len(list)):
					for l in range(7):
						graphs[l][j].SetPoint(k,k+1,counts[j][list[k][0]][l][0])
						graphs[l][j].SetPointError(k,0,counts[j][list[k][0]][l][1])

				mg = r.TMultiGraph()
				legend = r.TLegend(0.86, 0.60, 1.00, 0.10)
				for l in reversed(range(7)):
					graphs[l][j].SetMarkerStyle(8)
					graphs[l][j].SetMarkerColor(l+1)
					graphs[l][j].SetName(names[l])
					graphs[l][j].SetFillColor(0)
					legend.AddEntry(graphs[l][j],names[l])
					mg.Add(graphs[l][j])

				mg.SetTitle(org.samples[j]['name'])
				mg.Draw("AP")
				for k in range(len(list)):
					mg.GetXaxis().SetBinLabel(mg.GetXaxis().FindFixBin(k+1),labels[k])
				mg.GetYaxis().SetTitle('Number of Events')
				mg.GetXaxis().SetTitle('cut Index')
				legend.Draw("same")
				plotter.printCanvas()
				plotter.canvas.Clear()

		plotter.printCanvas("]")
		print plotter.pdfFileName, "has been written."
