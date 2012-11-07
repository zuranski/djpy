
import supy,samples,calculables,steps,ROOT as r
from calculables.utils import abcdCmp

class trigeff1Ptrk(supy.analysis) :
    
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate = ['jetPromptness']

	IniCuts=[
        {'name':'jet'},
        {'name':'jetPt','min':60},
    ]
	Cuts=[
        #{'name':'jetPromptness','max':0.35},
        {'name':'jetNPromptTracks','max':1},
        {'name':'jetTrigPrompt','val':True},
    ]
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
			mysteps.append(steps.plots.trigvars(indices=cut['name']+'Indices',njets=1))
		for cut in self.Cuts: 
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(steps.plots.trigvars(indices=cut['name']+'Indices',njets=1))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts+self.Cuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)('jetIndices'))
		return calcs

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
				target=("data/HT250_R11AB_observed.root","pileup"),
				groups=[('qcd',[]),('Huds',[]),('Hb',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT250_v"),
			steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_v",veto=True),
			steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v",veto=True),
			steps.trigger.hltIsPresent("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v"),
			]
			
			+[supy.steps.filters.value('pfHT',min=280)]

			### plots
			+[steps.event.general()]
			+self.dijetSteps1()
			)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
			+self.calcsIndices()
			+self.calcsVars()
			+[calculables.Matching.jetTrigPrompt('hlt2DisplacedHT2501PTrkL3Filter')]
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all

		qcd_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupPUInteractionsBX0Target']))
		return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456)
			+ supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1.913)
			+ qcd_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation", "color":r.kBlue,"markerStyle":21,"markerSize":0.3}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":21,"markerSize":0.3}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			#dependence2D=True,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			doLog=False,
			anMode=True,
			pageNumbers=False,
			pushLeft=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		#self.makeEfficiencyPlots1(org,"jetPt","jetTrigPrompt", plotter)
		#self.makeEfficiencyPlots2(org,"jetPromptness","jetTrigPrompt",plotter)
		self.makeEfficiencyPlots2(org,"jetNPromptTracks","jetTrigPrompt",plotter)

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
		plotter.individualPlots(plotSpecs = [{"plotName":"effNPromptTracks",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; N Prompt Tracks; Trigger Efficiency",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.67, 0.85),}
                                            ],
                                histos=eff_histos["divide_NPromptTracks_h_jetTrigPrompt_by_NPromptTracks_h_jetPt"],
                               )
		plotter.individualPlots(plotSpecs = [{"plotName":"effPromptEnergyFrac",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; Prompt Energy Fraction; Trigger Efficiency",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.67, 0.85),}
                                            ],
                                histos=eff_histos["divide_PromptEnergyFrac_h_jetTrigPrompt_by_PromptEnergyFrac_h_jetPt"],
                               )
		plotter.individualPlots(plotSpecs = [{"plotName":"effPromptness",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; Promptness; Trigger Efficiency",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.67, 0.85),}
                                            ],
                                histos=eff_histos["divide_Promptness_h_jetTrigPrompt_by_Promptness_h_jetPt"],
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
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; jet #eta; Trigger Efficiency",
                                              "legendCoords": (0.35, 0.15, 0.7, 0.35),
                                              "stampCoords": (0.5, 0.65),}
                                            ],
                                #histos=eff_histos["divide_Eta_h_jetTrigPrompt_by_Eta_h_jetPromptness"],
                                histos=eff_histos["divide_Eta_h_jetTrigPrompt_by_Eta_h_jetNPromptTracks"],
                               )
		plotter.individualPlots(plotSpecs = [{"plotName":"effPhi",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; jet #phi; Trigger Efficiency",
                                              "legendCoords": (0.35, 0.15, 0.7, 0.35),
                                              "stampCoords": (0.5, 0.65),}
                                            ],
                                #histos=eff_histos["divide_Phi_h_jetTrigPrompt_by_Phi_h_jetPromptness"],
                                histos=eff_histos["divide_Phi_h_jetTrigPrompt_by_Phi_h_jetNPromptTracks"],
                               )
		plotter.individualPlots(plotSpecs = [{"plotName":"effPt",
                                              "stepName":"",
                                              "stepDesc":"",
                                              "newTitle":"; jet p_{T} [GeV/c]; Trigger Efficiency",
                                              "legendCoords": (0.35, 0.15, 0.7, 0.35),
                                              "stampCoords": (0.5, 0.65),}
                                            ],
                                #histos=eff_histos["divide_Pt_h_jetTrigPrompt_by_Pt_h_jetPromptness"],
                                histos=eff_histos["divide_Pt_h_jetTrigPrompt_by_Pt_h_jetNPromptTracks"],
                               )
