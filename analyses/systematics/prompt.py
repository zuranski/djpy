import supy,samples,calculables,steps,ROOT as r

class prompt(supy.analysis) :
   
	# scale for QCD 65.8
 
	ToCalculateAny=['dijetPt1','dijetPt2','dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']
	ToCalculateVtx=['dijetVtxNRatio']

	IniCuts=[
		{'name':'dijet'},
		#{'name':'dijetPt1','min':65},
		#{'name':'dijetPt2','min':65},
		# vertex minimal
		{'name':'dijetVtxChi2','min':0,'max':5},
		{'name':'dijetVtxN1','min':1},
		{'name':'dijetVtxN2','min':1},
		# cluster minimal
		#{'name':'dijetbestclusterN','min':2},
	]
	Cuts=[
		# clean up cuts	
		{'name':'dijetVtxNRatio','min':0.1},
		#{'name':'dijetLxysig','min':8},
		{'name':'dijetVtxmass','min':4},
		{'name':'dijetVtxpt','min':8},
	  	{'name':'dijetNAvgMissHitsAfterVert','max':2},
		{'name':'dijetVtxN','min':5},
		{'name':'dijetLxysig','max':3},
	  	#{'name':'dijetNAvgMissHitsAfterVert','max':2},
		#{'name':'dijetNoOverlaps','val':True},
		#{'name':'dijetTrueLxy','min':0},
	]

	def dijetSteps(self):
		mysteps = []
		cutsToPlot1D = self.IniCuts[-1:]+self.Cuts
		cutsToPlot2D = cutsToPlot1D[-1:]
		for cut in (self.IniCuts+self.Cuts):
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut in cutsToPlot1D: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			#if cut in cutsToPlot2D: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices',plot2D=True,plot1D=False))
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
		for calc in self.ToCalculateVtx:
			calcs.append(getattr(calculables.Vars,calc)('dijetVtxChi2Indices'))
		for calc in self.ToCalculateAny:
			calcs.append(getattr(calculables.Vars,calc)('dijetIndices'))
		calcs.append(calculables.Overlaps.dijetNoOverlaps('dijetLxysigIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
				target=(supy.whereami()+"/../data/pileup/HT300_R12BCD_true.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

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
			#supy.steps.filters.value('caloHT',min=325),
			]

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

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		sig_samples = []
		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))

		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.3) +
			supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.495) +
			supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6.34) +
			supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=7.11) +
			qcd_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Simulation", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=18600)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			samplesForRatios = ("Data","Simulation"),
			sampleLabelsForRatios = ("Data","Sim"),
			#anMode=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			dependence2D=True,
			doCorrTable=True,
			pegMinimum=5,
			anMode=True
		)
		plotter.plotAll()
		org.lumi=None
		plotter.individualPlots(plotSpecs = [{"plotName":"NAvgMissHitsAfterVert_h_dijetVtxpt",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":";Missing Hits per track after Vertex;di-jets / bin",
                                              "legendCoords": (0.55, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                            ]
                               )
