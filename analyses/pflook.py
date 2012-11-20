import supy,samples,calculables,steps,ROOT as r

class pflook(supy.analysis) :

	jetCalcs = []
	dijetCalcs = ['dijetPt1','dijetPt2']

	jetCuts=[
        {'name':'jet'},
        {'name':'jetPt','min':65},
    ]
	dijetCuts=[
        {'name':'dijet'},
        {'name':'dijetPt1','min':65},
        {'name':'dijetPt2','min':65},
    ]

	def calcsIndices(self):
		calcs = []
		cutSets = [self.jetCuts,self.dijetCuts]
		for cutSet in cutSets:
			for cutPrev,cutNext in zip(cutSet[:-1],cutSet[1:]):
				calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def calcsVars(self):
		calcs = []
		calcsSets = [self.jetCalcs,self.dijetCalcs]
		indicesSets = ['jetIndices','dijetIndices']
		for calcsSet,indicesSet in zip(calcsSets,indicesSets):
			for calc in calcsSet:
				calcs.append(getattr(calculables.Vars,calc)(indicesSet))
		return calcs

	def plots(self,n):
		indices=[self.jetCuts[-1]['name'],self.dijetCuts[-1]['name']][n-1] + 'Indices'
		return [
                steps.plots.general(indices=indices,njets=n),
				steps.plots.fractions(indices=indices,njets=n),
				steps.plots.promptness(indices=indices,njets=n),
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
			+[supy.calculables.other.Target("pileupPUInteractionsBX0",thisSample=config['baseSample'],
				target=("data/HT300_R12BC_observed.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT300_v")]

			+[supy.steps.filters.value('caloHT',min=360)]
			### plots
			+[steps.event.general()]
			+self.plots(1)
			+self.plots(2)
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

		MH = [1000,1000,1000,400,400,200]
		MX = [350,150,50,150,50,50]
		sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		sig_samples = []
		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=["pileupPUInteractionsBX0Target"]))
		for i in range(len(sig_names)):
			sig_samples+=(supy.samples.specify(names = sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=["pileupPUInteractionsBX0Target"] ))

		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.039) +
			supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.4404) +
			supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=5.764) +
			qcd_samples + 
			sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"H", "color":r.kRed}, allWithPrefix = "H")
		org.scale()
		supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("data","qcd"),
			sampleLabelsForRatios = ("data","qcd"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		).plotAll()
