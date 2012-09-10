import supy,samples,calculables,steps,ROOT as r

class discriminants(supy.analysis) :
    
	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names_u = ["Huds_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	sig_names_b = ["Hb_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate=['dijetVtxptRatio','dijetVtxNTotRatio']

	IniCuts=[
		{'name':'dijet'},
		{'name':'dijetVtxChi2','min':0,'max':4},
		{'name':'dijetVtxN1','min':1},
		{'name':'dijetVtxN2','min':1},
		{'name':'dijetVtxmass','min':5},
		{'name':'dijetPosip2dFrac','min':0.5},
		{'name':'dijetglxyrmsclr','max':1.,'min':0},
	]
	Cuts=[
		{'name':'dijetDiscriminantVtx','min':0.998},
		{'name':'dijetDiscriminantPromptness','min':0.999},
		{'name':'dijetLxysig','min':8},
	]

	def dijetSteps1(self):
		mysteps = []
		cuts = self.IniCuts
		for cut in cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut == cuts[-1]:
				mysteps.append(steps.plots.general(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.promptness(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.vertices(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.clusters(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.discriminants(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		cuts = self.Cuts
		for cut in cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(steps.plots.general(indices=cut['name']+'Indices'))
			mysteps.append(steps.plots.promptness(indices=cut['name']+'Indices'))
			mysteps.append(steps.plots.vertices(indices=cut['name']+'Indices'))
			mysteps.append(steps.plots.clusters(indices=cut['name']+'Indices'))
			mysteps.append(steps.plots.discriminants(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet discriminant filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			indicesPrev=cutPrev['name']+'Indices'
			indicesNext=cutNext['name']+'Indices'	
			calcs.append(getattr(calculables.Indices,cutNext['name']+'Indices')(
				indices=cutPrev['name']+'Indices',
				min=cutNext['min'] if 'min' in cutNext else None,
				max=cutNext['max'] if 'max' in cutNext else None,
				val=cutNext['val'] if 'val' in cutNext else None,
				)
			)
		return calcs

	def discs(self):
		discSamplesRight=[name+'.pileupPUInteractionsBX0Target' for name in (self.sig_names_u + self.sig_names_b)]
		discSamplesLeft=['dataA','dataB']
		return([supy.calculables.other.Discriminant(fixes=("dijet","Promptness"),
												    right = {"pre":"H","tag":"","samples":discSamplesRight},
                                                    left = {"pre":"data","tag":"","samples":discSamplesLeft},
                                                    dists = {"dijetPromptEnergyFrac":(10,0,0.2),
                                                             "dijetNPromptTracks": (12,-0.5,11.5),
															},
													indices=self.IniCuts[-1]['name']+'Indices',
													bins = 50),
			    supy.calculables.other.Discriminant(fixes=("dijet","Vtx"),
													right = {"pre":"H","tag":"","samples":discSamplesRight},
													left = {"pre":"data","tag":"","samples":discSamplesLeft},
													dists = {"dijetVtxN":(7,1.5,8.5),
															 "dijetNAvgMissHitsAfterVert": (6,0,6),
															 "dijetglxyrmsclr": (10,0,1),
															 "dijetbestclusterN": (7,1.5,8.5),
															 "dijetPosip2dFrac": (5,0.5,1),
															 "dijetVtxpt": (12,0.,50),
															 "dijetVtxmass": (20,5.,50),
															},
													indices=self.IniCuts[-1]['name']+'Indices',
													bins = 50),
			   ])

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)(self.IniCuts[-1]['name']+'Indices'))
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
		sig_samples_u = []
		sig_samples_b = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupPUInteractionsBX0Target']))
		for i in range(len(self.sig_names_u)):
			sig_samples_u+=(supy.samples.specify(names = self.sig_names_u[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupPUInteractionsBX0Target']))
		for i in range(len(self.sig_names_b)):
			sig_samples_b+=(supy.samples.specify(names = self.sig_names_b[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupPUInteractionsBX0Target']))

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
		).plotAll()
