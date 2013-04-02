import supy,samples,calculables,steps,ROOT as r

class trigHTeff(supy.analysis) :
    
	IniCuts=[
        {'name':'jet'},
        {'name':'jetPt','min':65},
    ]

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter()]

			### filters
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

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
				target=("data/pileup/HT250_R12BCD_true.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT250_v"),
			#steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v",veto=True),
			steps.trigger.hltIsPresent("HLT_HT300_v"),]
			+self.dijetSteps()
			+[steps.event.general(),
			supy.steps.histos.generic('pfHT',60,250,550,suffix="lower",title='; pfHT [GeV] ; events / bin'),
			supy.steps.histos.generic('caloHT',60,250,550,suffix="lower",title='; caloHT [GeV] ; events / bin'),
			steps.trigger.hltFilterWildcard("HLT_HT300_v"),
			steps.event.general(),
			supy.steps.histos.generic('pfHT',60,250,550,suffix="higher",title='; pfHT [GeV] ; events / bin'),
			supy.steps.histos.generic('caloHT',60,250,550,suffix="higher",title='; caloHT [GeV] ; events / bin'),]
			)

	def dijetSteps(self):
		mysteps = []
		for cut in self.IniCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables)
			+self.calcsIndices()
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]
		qcd_samples = []

		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=["pileupTrueNumInteractionsBX0Target"]))
		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=2.02)
			+ supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.2218)
			+ supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=2.885)
			+ supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=3.213)
			+ qcd_samples[:-3] 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation", "color":r.kBlue, "markerStyle":20,"markerSize":0.4}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20,"markerSize":0.4}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			doLog=True,
			anMode=True,
			showStatBox=False,
			pageNumbers=False,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		self.makeEfficiencyPlots(org,"lower","higher", plotter)

	def makeEfficiencyPlots(self, org, denomName, numName, plotter):

		plotter.doLog=False

		hists_denom = []
		hists_num = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if denomName in plotName: hists_denom.append(step[plotName])
				if numName in plotName: hists_num.append(step[plotName])

		eff_histos = {}
		for num_list,denom_list in zip(hists_num,hists_denom):
			name=num_list[0].GetName()
			ratio_tpl = tuple([r.TGraphAsymmErrors(num,denom,"cl=0.683 cp") for num,denom in zip(num_list,denom_list)])
			for ratio,num in zip(ratio_tpl,num_list):
				ratio.GetXaxis().SetLimits(num.GetXaxis().GetXmin(),num.GetXaxis().GetXmax())
			eff_histos[ratio_tpl[0].GetName()]=ratio_tpl

		#print eff_histos
		'''
		plotter.individualPlots(plotSpecs = [{"plotName":"effHTPF",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; PF H_{T} [GeV]; Trigger Efficiency",
                                              "legendCoords": (0.45, 0.25, 0.8, 0.45),
                                              "stampCoords": (0.67, 0.7),}
                                            ],
                                histos=eff_histos["divide_pfHThigher_by_pfHTlower"],
                               )
		'''
		plotter.individualPlots(plotSpecs = [{"plotName":"effHTCalo",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; Calo H_{T} [GeV]; Trigger Efficiency",
                                              "legendCoords": (0.45, 0.25, 0.8, 0.45),
                                              "stampCoords": (0.67, 0.7),}
                                            ],
                                histos=eff_histos["divide_caloHThigher_by_caloHTlower"],
                               )
			
