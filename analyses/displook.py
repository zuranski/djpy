import supy,samples,calculables,steps,ROOT as r

class displook(supy.analysis) :
    
	ToCalculate=['dijetVtxNRatio','dijetPromptness','dijetPromptness1','dijetPromptness2']

	IniCuts=[
		{'name':'dijet'},
		# vertex minimal
		{'name':'dijetVtxChi2','min':0,'max':4},
		{'name':'dijetVtxN1','min':1},
		{'name':'dijetVtxN2','min':1},
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
		{'name':'dijetNoOverlaps','val':True},
	]

	def dijetSteps(self):
		mysteps = []
		cutsToPlot1D = self.IniCuts[-1:]+self.Cuts
		cutsToPlot2D = cutsToPlot1D[-1:]
		for cut in (self.IniCuts+self.Cuts):
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut in cutsToPlot1D: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			if cut in cutsToPlot2D: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices',plot2D=True,plot1D=False))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts=self.IniCuts+self.Cuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext)
			)
		return calcs

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
			steps.trigger.hltFilterWildcard("HLT_HT250_v")]

			### plots
			+[steps.event.general()]
			+self.dijetSteps()
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

		MH = [1000,1000,1000,400,400,200]
		MX = [350,150,50,150,50,50]
		sig_names_u = ["Huds_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
		sig_names_b = ["Hb_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		sig_samples_u = []
		sig_samples_b = []
		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupPUInteractionsBX0Target']))
		for i in range(len(sig_names_u)):
			sig_samples_u+=(supy.samples.specify(names = sig_names_u[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupPUInteractionsBX0Target']))
		for i in range(len(sig_names_b)):
			sig_samples_b+=(supy.samples.specify(names = sig_names_b[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupPUInteractionsBX0Target']))

		return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456)
			+ supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1.913)
			+ qcd_samples 
			+ sig_samples_u
			+ sig_samples_b
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"Huds", "color":r.kRed}, allWithPrefix = "Huds")
		org.mergeSamples(targetSpec = {"name":"Hb", "color":r.kGreen}, allWithPrefix = "Hb")
		org.scale()
		supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("data","qcd"),
			sampleLabelsForRatios = ("data","qcd"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			dependence2D=True,
			doCorrTable=True,
		).plotAll()
