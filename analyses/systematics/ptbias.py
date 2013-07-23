import supy,samples,calculables,steps,ROOT as r

class ptbias(supy.analysis) :

	MH = [1000,1000,1000,1000,400,400,400,200,200,120,120]
	MX = [350,150,50,20,150,50,20,50,20,50,20]
	ctau = [35,10,4,1.5,40,8,4,20,7,50,13]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]

	AccCuts=[
		{'name':'gendijet'},
	]
	Cuts=[
		{'name':'jet'},
		{'name':'jetPt','min':40},
		{'name':'jetgenjetLxy','min':0,'max':60},
		{'name':'jetgenjetDeltaR','min':0.5},
		{'name':'jetgenjetAngle','max':100},
		{'name':'jetgenjetN','min':1},
	]
 
	def dijetSteps0(self):
		mysteps = []
		for cut in self.AccCuts[1:]:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
		return([supy.steps.filters.label('Acceptance Cuts')]+mysteps)

	def jetSteps(self):
		mysteps = []
		for cut in self.Cuts[-1:]:
			mysteps.append(steps.plots.genjets(njets=1,indices=cut['name']+'Indices'))
			mysteps.append(steps.plots.genjets(njets=1,indices=cut['name']+'Indices',plot2D=True,plot1D=False))
		return ([supy.steps.filters.label('Jet Cuts')] +mysteps)
	
	def calcsIndices(self):
		calcs = []
		for cutPrev,cutNext in zip(self.AccCuts[:-1],self.AccCuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cutPrev,cutNext in zip(self.Cuts[:-1],self.Cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs


	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]

		### acceptance filters
		+self.dijetSteps0()
	
		+[supy.steps.filters.label('data cleanup'),
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
		
		+[steps.event.general(),steps.event.genevent()]
		+self.jetSteps()

		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
		+self.calcsIndices()
		)

	def listOfSampleDictionaries(self) :
		return [samples.sigmc]
    
	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all
		sig_samples = []

		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles))

		merged_samples=[sig_samples[i] for i in [2,3,6,8,10]]
		nonmerged_samples=[sig_samples[i] for i in [0,1,4,5,7,9]]
		toPlot=[nonmerged_samples[i] for i in [1]]

		#return merged_samples
		#return nonmerged_samples
		return toPlot

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow 2X(350)(X#rightarrow q#bar{q})", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_1000_X_350")                                 
		org.mergeSamples(targetSpec = {"name":"H(400)#rightarrow 2X(150)(X#rightarrow q#bar{q})", "color":r.kGreen,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_400_X_150")                               
		org.mergeSamples(targetSpec = {"name":"H(200)#rightarrow 2X(50)(X#rightarrow q#bar{q})", "color":r.kBlack,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_200_X_50")
		org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow 2X(150)(X#rightarrow q#bar{q})", "color":r.kBlue,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_1000_X_150")
		org.mergeSamples(targetSpec = {"name":"H(400)#rightarrow 2X(50)(X#rightarrow q#bar{q})", "color":r.kMagenta,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_400_X_50")                               
		org.mergeSamples(targetSpec = {"name":"H(120)#rightarrow 2X(50)(X#rightarrow q#bar{q})", "color":r.kYellow,"lineWidth":3,"goptions":"hist","lineStyle":1}, allWithPrefix = "H_120_X_50")                              
		org.scale(lumiToUseInAbsenceOfData=18600)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=False,
			anMode=True,
			showStatBox=True,
			pegMinimum=10,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()

		org.lumi=None
		
		plotter.individualPlots(plotSpecs = [{"plotName":"genjetLxy_h_jetgenjetN",
                                              "stepName":"genjets",
                                              "stepDesc":"genjets",
                                              "newTitle":";L_{xy} [cm] ; jets / bin",
                                              "legendCoords": (0.5, 0.7, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"genjetDeltaR_h_jetgenjetN",
                                              "stepName":"genjets",
                                              "stepDesc":"genjets",
                                              "newTitle":";q#bar{q} #Delta R; jets / bin",
                                              "legendCoords": (0.5, 0.7, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"genjetPtDiff_h_jetgenjetN",
                                              "stepName":"genjets",
                                              "stepDesc":"genjets",
                                              "newTitle":";( jet p_{T} - true p_{T} ) / true p_{T}; jets / bin",
                                              "legendCoords": (0.18, 0.7, 0.48, 0.9),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"genjetAngle_h_jetgenjetN",
                                              "stepName":"genjets",
                                              "stepDesc":"genjets",
                                              "newTitle":";approach Angle [deg]; jets / bin",
                                              "legendCoords": (0.5, 0.7, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"PtFracTh1_h_jetgenjetN",
                                              "stepName":"genjets",
                                              "stepDesc":"genjets",
                                              "newTitle":";jet energy fraction tracks<0.8GeV [%]; jets / bin",
                                              "legendCoords": (0.5, 0.7, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                            ]
                               )
		
		self.profiles(org,plotter)

	def profiles(self,org,plotter):

		plotter.pdfFileName = plotter.pdfFileName.replace(self.name+'.pdf','Profiles_'+self.name+'.pdf')
		plotter.pageNumbers=False
		plotter.canvas.Clear()
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		plotter.flushPage()
		plotter.doLog=False

		neus,chgs=[],[]
		profiles = [] 
		XorY = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'genjetPtDiff' in plotName and issubclass(type(step[plotName][0]),r.TH2) : 
					isX = 0 if plotName.find('genjetPtDiff') == 0 else 1
					XorY.append(isX)
					profiles.append(step[plotName])

		def removeLowStats(histos):
			for histo in histos:
				for i in range(1,histo.GetNbinsX()+1):
					if histo.GetBinEntries(i)<50: 
						histo.SetBinContent(i,0)		
						histo.SetBinError(i,0)		


		for profile,isX in zip(profiles,XorY):
			#plotter.canvas.Divide(3,2)
			histosX = [h.ProfileX('',1,-1,'s').Clone() for h in profile]
			histosY = [h.ProfileY('',1,-1,'s').Clone() for h in profile]
			removeLowStats(histosX)
			removeLowStats(histosY)
			histos = histosX if isX else histosY
			latex=r.TLatex()
			latex.SetNDC()
			latex.SetTextSize(0.035)
			for i,sample in enumerate(org.samples):
				name=sample['name']
				plotter.canvas.cd(i+1)
				r.gPad.SetTopMargin(0.08)
				r.gPad.SetLeftMargin(0.2)
				r.gPad.SetRightMargin(0.05)
				histos[i].SetMarkerStyle(20)
				histos[i].SetMarkerSize(2)
				histos[i].SetStats(False)
				histos[i].SetName(name)
				histos[i].SetTitle(name)
				histos[i].GetYaxis().SetTitle('(jet p_{T} - true p_{T} )/ true p_{T}')
				histos[i].GetYaxis().SetTitleOffset(2.)
				histos[i].Draw()
				latex.DrawLatex(0.22,0.95,name)
			plotter.printCanvas()
			plotter.canvas.Clear()
		plotter.printCanvas("]")
