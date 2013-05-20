import supy,samples,calculables,steps,ROOT as r

class displook(supy.analysis) :
    
	ToCalculate=['dijetVtxNRatio']
	ToCalculate += ['dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']

	IniCuts=[
		{'name':'dijet'},
		{'name':'dijetTrueLxy','min':0},
		# vertex minimal
		{'name':'dijetVtxChi2','min':0,'max':5},
		{'name':'dijetVtxN1','min':1},
		{'name':'dijetVtxN2','min':1},
		# cluster minimal
		{'name':'dijetbestclusterN','min':2},
	]
	Cuts=[
		# clean up cuts	
		{'name':'dijetVtxmass','min':4},
		{'name':'dijetVtxpt','min':8},
		#{'name':'dijetVtxNRatio','min':0.1},
		{'name':'dijetLxysig','min':8},
		{'name':'dijetNoOverlaps','val':True},
	  	#{'name':'dijetNAvgMissHitsAfterVert','max':2},
		#{'name':'dijetTrueLxy','min':0},
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
			supy.steps.printer.progressPrinter(),]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
				target=(supy.whereami()+"/../data/pileup/HT300_Single_R12BCD_true.root","pileup"),
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
			steps.trigger.hltFilterWildcard("HLT_HT300_SingleDisplacedPFJet60_v"),
			steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v",veto=True).onlyData(),
			supy.steps.filters.value('caloHT',min=325),]

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
		sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		sig_samples = []
		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
		for i in range(len(sig_names)):
			sig_samples+=(supy.samples.specify(names = sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target']))

		return (qcd_samples
			+supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=44.3) +
			supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.95) +
			supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=63.44) +
			supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=71.05) 
			#+ qcd_samples 
			#+ sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"E2","fillColor":r.kBlue,"fillStyle":3001,"double":True,"markerSize":0}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=11000)
		plotter=supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("Data","QCD"),
			sampleLabelsForRatios = ("Data","QCD"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			dependence2D=True,
			doCorrTable=True,
			pegMinimum=1,
			anMode=True,
		)
		plotter.plotAll()

		plotter.individualPlots(plotSpecs = [
											  {"plotName":"Lxysig_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; L_{xy} significance; di-jets / bin",
                                              "legendCoords": (0.35, 0.15, 0.9, 0.35),
                                              "stampCoords": (0.7, 0.88)
                                              },
											  {"plotName":"PromptEnergyFrac2_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Charged Prompt Energy Fraction; di-jets / bin",
                                              "legendCoords": (0.35, 0.15, 0.9, 0.35),
                                              "stampCoords": (0.5, 0.7)
                                              },
                                              {"plotName":"NPromptTracks2_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Number of Prompt Tracks ; di-jets / bin",
                                              "legendCoords": (0.45, 0.15, 0.9, 0.35),
                                              "stampCoords": (0.7, 0.7)
                                              },
                                              {"plotName":"VtxN_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex Multiplicity ; di-jets / bin",
                                              "legendCoords": (0.55, 0.35, 0.9, 0.55),
                                              "stampCoords": (0.7, 0.8)
                                              },
                                              {"plotName":"Vtxmass_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex Invariant Mass [GeV/c^{2}]; di-jets / bin",
                                              "legendCoords": (0.45, 0.15, 0.9, 0.35),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"Vtxpt_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex p_{T} [GeV/c]; di-jets / bin",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"bestclusterN_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster Multiplicity; di-jets / bin",
                                              "legendCoords": (0.55, 0.45, 0.9, 0.65),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"glxyrmsclr_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster RMS; di-jets / bin",
                                              "legendCoords": (0.55, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.9)
                                              },
                                              {"plotName":"NAvgMissHitsAfterVert_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Missing Hits per track after Vertex; di-jets / bin",
                                              "legendCoords": (0.45, 0.15, 0.9, 0.35),
                                              "stampCoords": (0.7, 0.7)
                                              },
                                              {"plotName":"Posip2dFrac_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Tracks with positive IP fraction; di-jets / bin",
                                              "legendCoords": (0.2, 0.15, 0.4, 0.35),
                                              "stampCoords": (0.7, 0.5)
                                              },
                                            ]
                               )
