import supy,samples,calculables,steps,ROOT as r

class efficiency(supy.analysis) :

	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names_u = ['Huds_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]
	sig_names_b = ['Hb_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]

	ToCalculate = ['dijetVtxNRatio','dijetPromptness1','dijetPromptness2']
    
	IniCuts=[
        {'name':'dijet'},
        #{'name':'dijetTrueLxy','min':0},
        # vertex minimal
        {'name':'dijetVtxChi2','min':0,'max':4},
        {'name':'dijetVtxN1','min':1},
        {'name':'dijetVtxN2','min':1},
        {'name':'dijetNoOverlaps','val':True},
        # cluster minimal
        {'name':'dijetbestclusterN','min':2},
    ]
	Cuts=[
        # clean up cuts 
        {'name':'dijetNAvgMissHitsAfterVert','max':1.99},
        {'name':'dijetVtxmass','min':5},
        {'name':'dijetVtxpt','min':10},
        {'name':'dijetVtxNRatio','min':0.1},
        {'name':'dijetLxysig','min':8},
    ]
	ABCDCuts= [
		{'name':'dijetPromptness1','max':0.35,'more':'max0.35'},
		{'name':'dijetPromptness2','max':0.35,'more':'max0.35'},
		{'name':'dijetDiscriminant','min':0.7,'more':'min0.7'},
		]
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		#mysteps.append(supy.steps.filters.multiplicity('dijetNoOverlapsIndices',min=1))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for cut in self.ABCDCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		#mysteps.append(supy.steps.filters.multiplicity(self.ABCDCuts[-1]['name']+'Indices',max=1))
		mysteps.append(steps.other.collector(['dijetMass','dijetLxy'],indices=self.ABCDCuts[-1]['name']+'Indices'))
		mysteps.append(steps.plots.observables(indices=self.ABCDCuts[-1]['name']+'Indices'))
		mysteps.append(steps.plots.cutvars(indices=self.ABCDCuts[-1]['name']+'Indices'))
		mysteps.append(steps.plots.ABCDvars(indices=self.ABCDCuts[-1]['name']+'Indices'))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts + self.ABCDCuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		calcs.append(calculables.Indices.ABCDIndices(indices=self.Cuts[-1]['name']+'Indices',cuts=self.ABCDCuts))
		#calcs.append(calculables.Overlaps.dijetNoOverlapsIndices(indices=self.Cuts[-1]['name']+'Indices'))
		return calcs

	def discs(self):
		discSamplesRight=[name+'.pileupPUInteractionsBX0Target' for name in (self.sig_names_u + self.sig_names_b)]
		discSamplesLeft=['dataA','dataB']
		return([supy.calculables.other.Discriminant(fixes=("dijet",""),
													right = {"pre":"H","tag":"","samples":discSamplesRight},
													left = {"pre":"data","tag":"","samples":discSamplesLeft},
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
			calcs.append(getattr(calculables.Vars,calc)('dijetIndices'))
		calcs.append(calculables.Overlaps.dijetNoOverlaps('dijetVtxN2Indices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		### filters
		+[supy.steps.filters.label('data cleanup'),
		supy.steps.filters.value('isPrimaryVertex',min=1),
		supy.steps.filters.value('isPhysDeclared',min=1).onlyData(),
		supy.steps.filters.value('isBeamScraping',max=0),
		supy.steps.filters.value('passBeamHaloFilterTight',min=1),
		supy.steps.filters.value('passHBHENoiseFilter',min=1)]

		### pile-up reweighting
		+[supy.calculables.other.Target("pileupPUInteractionsBX0",thisSample=config['baseSample'],
                                    target=("data/ABcontrol_observed.root","pileup"),
                                    groups=[('qcd',[]),('Huds',[]),('Hb',[])]).onlySim()] 

		### trigger
		+[supy.steps.filters.label("hlt trigger"),
		steps.trigger.hltFilterWildcard("HLT_HT250_v"),
		steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_v")]
		#steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_PromptTrack_v")]

		#steps.effplots.histos('candsDouble'),
		#steps.effplots.histos("doubleVeryLoose"),
		+self.dijetSteps1()
		+self.discs()
		+self.dijetSteps2()
		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
		+self.calcsVars()
		+self.calcsIndices()
		)

	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]
    
	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all
		sig_samples_u = []
		sig_samples_b = []

		qcd_samples = []
		for i in range(len(self.sig_names_u)):
			sig_samples_u+=(supy.samples.specify(names = self.sig_names_u[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles))
			sig_samples_b+=(supy.samples.specify(names = self.sig_names_b[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles))

		return sig_samples_u #+ sig_samples_b

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.scale(lumiToUseInAbsenceOfData=30)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()

		#self.makeEfficiencyPlots(org,"candsDouble","doubleVeryLoose", plotter)

	def makeEfficiencyPlots(self, org, denomName, numName, plotter):
		plotter.doLog = False
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		text2 = plotter.printNEventsIn()
		plotter.flushPage()

		hists_denom = []
		hists_num = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if denomName in plotName: hists_denom.append(step[plotName])
				if numName in plotName: hists_num.append(step[plotName])

		for num_list,denom_list in zip(hists_num,hists_denom):
			ratio_tpl = tuple([supy.utils.ratioHistogram(num,denom) for num,denom in zip(num_list,denom_list)])
			for ratio in ratio_tpl:
				ratio.GetYaxis().SetTitle("efficiency")
			plotter.onePlotFunction(ratio_tpl)
		plotter.printCanvas("]")
		print plotter.pdfFileName, 'has been written'
