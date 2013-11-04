import supy,samples,calculables,steps,ROOT as r

class kshorts(supy.analysis) :
    
	Cuts=[
		{'name':'ks'},
		{'name':'ksNoOverlaps','val':True},
		{'name':'kscolin','min':0},
		{'name':'ksCtau','max':12},
		#{'name':'ksEta','min':-1.1,'max':1.1},
		{'name':'ksChi2','max':7.}, #chi2<3 for trk pt>3
		{'name':'ksTrk1Pt','min':1},
		{'name':'ksTrk2Pt','min':1},
		{'name':'ksMass','min':0.48,'max':0.515},
		#{'name':'ksMass','min':0.4,'max':0.6},
		# vertex minimal
	]
	# obtained scale for trk pt >1 is 1.495
	CutsScale=[
        {'name':'ksLxy','max':2},
	]

	def ksSteps(self):
		mysteps = []
		for cut in self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(steps.plots.kshort(indices=cut['name']+'Indices',ks=True))
		return ([supy.steps.filters.label('kshort multiplicity filters')]+mysteps)

	def ksStepsScale(self):
		mysteps = []
		for cut in self.CutsScale:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(steps.plots.kshort(indices=cut['name']+'Indices',ks=True))
		return ([supy.steps.filters.label('kshort Scale multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts=self.Cuts + self.CutsScale
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext)
			)
		return calcs

	def calcsVars(self):
		calcs = []
		calcs.append(calculables.Overlaps.ksNoOverlaps('ksIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),]

			### pile-up reweighting
			#+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
			#	target=(supy.whereami()+"/../data/pileup/HT300_R12BCD_true.root","pileup"),
			#	groups=[('qcd',[]),('H',[])]).onlySim()] 

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

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT300_v"),
			supy.steps.filters.value('pfHT',min=250),
			]

			### nPV re-weighting
			+[supy.calculables.other.Ratio("nPV",binning=(25,4.5,29.5),thisSample=config['baseSample'],
				target=("data",[]),
				groups=[('qcd',[])])] 

			### plots
			+[steps.event.general(),steps.plots.general(njets=1,indices='jetIndices')]
			+self.ksSteps()

			+[supy.calculables.other.Ratio("ksPt",binning=(20,0,40),thisSample=config['baseSample'],
                target=("data",[]),
                groups=[('qcd',[])],
                #indices='ksMassIndices')]
                indices=self.Cuts[-1]['name']+'Indices')]
			+[supy.calculables.other.Ratio("ksEta",binning=(20,-2.5,2.5),thisSample=config['baseSample'],
                target=("data",[]),
                groups=[('qcd',[])],
                #indices='ksMassIndices')]
                indices=self.Cuts[-1]['name']+'Indices')]
			
			+[steps.event.efftrk('ksMassIndices')]
			#+[supy.steps.filters.value('nPV',max=8)]
			+self.ksStepsScale()

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

		qcd_bins = [str(q) for q in [80,120,170,300,470,	600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		for i in range(len(qcd_names)):
			#qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['nPVRatio']))

		return (#qcd_samples
            supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.04) +
			supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.444) 
			+ supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=5.769) 
			+ supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6.427)
			+ qcd_samples 
			#+ sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation","markerSize":0, "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd",scaleFactors=[1.00/1.495]*6)
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11000)
		plotter=supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			#dependence2D=True,
			doCorrTable=True,
			#pegMinimum=1,
			anMode=True,
		)
		plotter.plotAll()
		org.lumi=None
		
		plotter.individualPlots(preliminary=True, plotSpecs = [{"plotName":"Mass_h_kscolin",
                                              "stepName":"kshort",
                                              "stepDesc":"kshort",
                                              "newTitle":"; K_{s}^{0} mass [GeV]; K_{s}^{0} / bin",
                                              "legendCoords": (0.6, 0.6, 0.95, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksCtau",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} c#tau [cm]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksLxy",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} Transverse Decay Length [cm]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksLxyz",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} Decay Length [cm]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"kstrkip2d",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} track IP_{xy} [cm]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"kstrkip3d",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} track IP_{xyz} [cm]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksP",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} momentum [GeV]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksLxysig",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} L_{xy} significance (L_{xy}>2cm); K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksChi2",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} vertex #chi^{2}/dof (L_{xy}>2cm); K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"ksTrkPt",
                                              "stepName":"efftrk",
                                              "stepDesc":"efftrk",
                                              "newTitle":"; K_{s}^{0} track p_{T} [GeV]; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"Lxysig_h_ksLxy",
                                              "stepName":"kshort",
                                              "stepDesc":"kshort",
                                              "newTitle":"; K_{s}^{0} L_{xy} significance (L_{xy}<2cm) ; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
											 {"plotName":"Chi2_h_ksLxy",
                                              "stepName":"kshort",
                                              "stepDesc":"kshort",
                                              "newTitle":"; K_{s}^{0} vertex #chi^{2}/dof (L_{xy}<2cm) ; K_{s}^{0} / bin",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
                                            ],
                               )
		
		self.makeEfficiencyPlots(org,'den','num',plotter)

	def makeEfficiencyPlots(self, org, denomName, numName, plotter):
		names_denom=['Pt_h_jet','nPV']
		names_num=['numksJetPt','numnPV']
		hists_denom = []
		hists_num = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if plotName in names_denom: hists_denom.append(step[plotName])
				if plotName in names_num: hists_num.append(step[plotName])

		hists_num.reverse()
		print hists_num
		print hists_denom

		eff_histos = {}
		for num_list,denom_list in zip(hists_num,hists_denom):
			name=num_list[0].GetName()
			ratio_tpl = tuple([r.TGraphAsymmErrors(num,denom,"cl=0.683 cp") for num,denom in zip(num_list,denom_list)])
			for ratio,num in zip(ratio_tpl,num_list):
				ratio.GetXaxis().SetLimits(num.GetXaxis().GetXmin(),num.GetXaxis().GetXmax())
			eff_histos[ratio_tpl[0].GetName()]=ratio_tpl
			print ratio_tpl[0].GetName()

		
		plotter.individualPlots(plotSpecs = [{"plotName":"effJetPt",
											  "histos":eff_histos["divide_numksJetPt_by_Pt_h_jet"],
                                              "newTitle":"; jet p_{T} [GeV] ; <K_{s}> ",
                                              "legendCoords": (0.65, 0.55, 0.8, 0.75),
                                              "stampCoords": (0.7, 0.9),},
                                             {"plotName":"effnPV",
                                              "histos":eff_histos["divide_numnPV_by_nPV"],
                                              "newTitle":"; pileup vertices ; <K_{s}^{0}>",
                                              "legendCoords": (0.55, 0.6, 0.9, 0.8),
                                              "stampCoords": (0.67, 0.88),},
                                            ],
                               )
		
