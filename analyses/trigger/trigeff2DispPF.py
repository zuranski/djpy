import supy,samples,calculables,steps,ROOT as r

class trigeff2DispPF(supy.analysis) :
    
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	jetCuts=[
        {'name':'jet'},
        {'name':'jetPt','min':55},
        {'name':'jetPromptEnergyFrac','max':0.15},
    ]
	
	def jetPlots(self):
		mysteps = []
		mysteps.append(steps.plots.trigvars(indices='jetPtIndices',njets=1))
		mysteps.append(steps.plots.trigvars(indices='jetPromptEnergyFracIndices',njets=1))
		mysteps.append(steps.plots.trigvars(indices='jetTrigPromptIndices1',njets=1))
		mysteps.append(steps.plots.trigvars(indices='jetTrigPromptIndices2',njets=1))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.jetCuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		# before cut
		calcs.append(calculables.Indices.Indices(indices='jetPtIndices',
                                                 cut={'name':'jetTrigPrompt','val':1},
                                                 tag='1')
                    )
        # after cut
		calcs.append(calculables.Indices.Indices(indices='jetPromptEnergyFracIndices',
                                                 cut={'name':'jetTrigPrompt','val':True},
                                                 tag='2')
                    )
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
			+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
				target=(supy.whereami()+"/../data/pileup/HT300_R12BCD_true.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT300_v"),
			#steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v",veto=True),
			steps.trigger.hltTriggerObjectMultiplicity('hlt2DisplacedHT300L1FastJetL3Filter',min=2)
			]

			### plots
			+[steps.event.general()]
			+self.jetPlots()
			)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
			+self.calcsIndices()
			+[calculables.TrigMatching.jetTrigPrompt('hlt2PFDisplacedJetsPt50')]
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all

		qcd_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.04)
			+ supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.4437)
			+ supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=5.769)
			+ supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6.427)
			+ qcd_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation", "color":r.kBlue,"markerStyle":21,"markerSize":0.6}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":21,"markerSize":0.6}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			doLog=True,
			anMode=True,
			pageNumbers=False,
			pushLeft=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		plotter.doLog=False
		self.makeEfficiencyPlots1(org,"jetPt","jetTrigPrompt1", plotter)
		self.makeEfficiencyPlots2(org,"jetPromptEnergyFrac","jetTrigPrompt2",plotter)

	def makeEfficiencyPlots1(self, org, denomName, numName, plotter):

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

		print eff_histos
		plotter.individualPlots(plotSpecs = [{"plotName":"effPromptEnergyFrac",
                                              "histos":eff_histos["divide_PromptEnergyFrac_h_jetTrigPrompt1_by_PromptEnergyFrac_h_jetPt"],
                                              "newTitle":"; Prompt Energy Fraction; Trigger Efficiency",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.67, 0.85),}
                                            ],
                               )

	def makeEfficiencyPlots2(self, org, denomName, numName, plotter):

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

		plotter.individualPlots(plotSpecs = [{"plotName":"effEta",
                                              "histos":eff_histos["divide_Eta_h_jetTrigPrompt2_by_Eta_h_jetPromptEnergyFrac"],
                                              "newTitle":"; jet #eta; Trigger Efficiency",
                                              "legendCoords": (0.4, 0.15, 0.75, 0.35),
                                              "stampCoords": (0.6, 0.65),},
											 {"plotName":"effPt",
                                              "histos":eff_histos["divide_Pt_h_jetTrigPrompt2_by_Pt_h_jetPromptEnergyFrac"],
                                              "newTitle":"; jet p_{T} [GeV]; Trigger Efficiency",
                                              "legendCoords": (0.4, 0.15, 0.75, 0.35),
                                              "stampCoords": (0.6, 0.65),},
											 {"plotName":"effPhi",
                                              "histos":eff_histos["divide_Phi_h_jetTrigPrompt2_by_Phi_h_jetPromptEnergyFrac"],
                                              "newTitle":"; jet #phi; Trigger Efficiency",
                                              "legendCoords": (0.4, 0.15, 0.75, 0.35),
                                              "stampCoords": (0.6, 0.65),}
                                            ],
                               )
