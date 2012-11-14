import supy,samples,calculables,steps,ROOT as r

class trigHTeff(supy.analysis) :
    
	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),

			### filters
			supy.steps.filters.label('data cleanup'),
			supy.steps.filters.value('isPrimaryVertex',min=1),
			supy.steps.filters.value('isPhysDeclared',min=1).onlyData(),
			supy.steps.filters.value('isBeamScraping',max=0),
			supy.steps.filters.value('passBeamHaloFilterTight',min=1),
			supy.steps.filters.value('passHBHENoiseFilter',min=1)]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupPUInteractionsBX0",thisSample=config['baseSample'],
				target=("data/HT200_R11AB_observed.root","pileup"),
				groups=[('qcd',[]),('Huds',[]),('Hb',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT200_v"),
			steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_v",veto=True),
			steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v",veto=True),
			steps.event.general(),
			supy.steps.histos.generic('pfHT',60,200,500,suffix="lower",title='; pfHT [GeV] ; events / bin'),
			steps.trigger.hltTriggerObjectMultiplicity("hltHT250",min=1),
			steps.event.general(),
			supy.steps.histos.generic('pfHT',60,200,500,suffix="higher",title='; pfHT [GeV] ; events / bin'),]
			)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = 2 # or None for all
		nEvents = None # or None for all

		qcd_bins = [str(q) for q in [50,80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]
		qcd_samples = []

		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=["pileupPUInteractionsBX0Target"]))
		return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=3.3618)
			+ supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.5355)
			+ qcd_samples[:-2] 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation", "color":r.kBlue, "markerStyle":4,"markerSize":0.2}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":4,"markerSize":0.2}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			doLog=False,
			anMode=True,
			showStatBox=False,
			pageNumbers=False,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		self.makeEfficiencyPlots(org,"lower","higher", plotter)

	def makeEfficiencyPlots(self, org, denomName, numName, plotter):

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
		plotter.individualPlots(plotSpecs = [{"plotName":"efficiencyHT",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; PF H_{T} [GeV]; Trigger Efficiency",
                                              "legendCoords": (0.45, 0.25, 0.8, 0.45),
                                              "stampCoords": (0.67, 0.7),}
                                            ],
                                histos=eff_histos["divide_pfHThigher_by_pfHTlower"],
                               )
			
