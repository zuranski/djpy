import supy,samples,calculables,steps,ROOT as r

class displookHT(supy.analysis) :
    
	IniCuts=[
		{'name':'dijet'},
		{'name':'dijetTrueLxy','min':0},
		{'name':'dijetPromptEnergyFrac1','max':1},
		{'name':'dijetPromptEnergyFrac2','max':1},
		#{'name':'dijetPt1','min':65},
		#{'name':'dijetPt2','min':65},
		# vertex minimal
		{'name':'dijetVtxChi2','min':0,'max':5},
		{'name':'dijetVtxN1','min':1},
		{'name':'dijetVtxN2','min':1},
		# cluster minimal
		{'name':'dijetbestclusterN','min':2},
	]
	Cuts=[
		# clean up cuts	
		{'name':'dijetVtxNRatio','min':0.1},
		{'name':'dijetLxysig','min':8},
		{'name':'dijetVtxmass','min':4},
		{'name':'dijetVtxpt','min':8},
	  	{'name':'dijetNAvgMissHitsAfterVert','max':2},
		{'name':'dijetNoOverlaps','val':True},
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
	        +[steps.other.genParticleMultiplicity(pdgIds=[6001114,6002114,6003114],collection='XpdgId',min=2,max=2)]
			#+[steps.other.genParticleMultiplicity(pdgIds=[13],collection='genqFlavor',min=2,max=2)]

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

		MH = [1000,1000,400,400,200]
		MX = [350,150,150,50,50]
		sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]

		qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
		qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

		qcd_samples = []
		sig_samples = []
		for i in range(len(qcd_names)):
			qcd_samples+=(supy.samples.specify(names = qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
		for i in range(len(sig_names)):
			sig_samples+=(supy.samples.specify(names = sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target']))

		return (
		    supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4.04) +
			supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=0.4437) +
			supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=5.769) +
			supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6.427) +
			
			qcd_samples 
			+[sig_samples[i] for i in [0,2,4]]
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"E2","fillColor":r.kBlue,"fillStyle":3001,"double":True,"markerSize":0}, allWithPrefix = "qcd",scaleFactors=[0.75]*6)
		org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(350) c#tau=35cm","markerSize":0, "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_350",scaleFactors=[1e4])                                 
		org.mergeSamples(targetSpec = {"name":"H^{0}(400)#rightarrow 2X^{0}(150) c#tau=40cm","markerSize":0, "color":r.kGreen,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_400_X_150",scaleFactors=[1e4])                               
		org.mergeSamples(targetSpec = {"name":"H^{0}(200)#rightarrow 2X^{0}(50) c#tau=20cm","markerSize":0, "color":r.kBlack,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_200_X_50",scaleFactors=[1e4])
		#org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=18600)
		plotter=supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			anMode=True,
			samplesForRatios = ("Data","QCD"),
			sampleLabelsForRatios = ("Data","QCD"),
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			#dependence2D=True,
			doCorrTable=True,
			pegMinimum=0.3,
			#pegMinimum=1000,
		)
		plotter.plotAll()

		#org.lumi=None	
		plotter.individualPlots(preliminary=False,plotSpecs = [
											  {"plotName":"Lxysig_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; L_{xy} significance; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
											  {"plotName":"PromptEnergyFrac2_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Charged Prompt Energy Fraction; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.55, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"NPromptTracks2_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Number of Prompt Tracks ; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.55, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"VtxN_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex Track Multiplicity ; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"Vtxmass_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex Invariant Mass [GeV]; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"Vtxpt_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex p_{T} [GeV]; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"bestclusterN_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster Track Multiplicity; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"glxyrmsclr_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster RMS; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"NAvgMissHitsAfterVert_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Missing Hits per track after Vertex; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"Posip2dFrac_h_dijetVtxNRatio",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Fraction of tracks with positive IP; dijets / bin",
                                              "legendCoords": (0.18, 0.77, 0.5, 0.92),
                                              "stampCoords": (0.73, 0.88)
                                              },
                                              {"plotName":"VtxN_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Vertex Track Multiplicity ; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
                                              {"plotName":"bestclusterN_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster Track Multiplicity; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
                                              {"plotName":"glxyrmsclr_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Cluster RMS; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
                                              {"plotName":"Posip2dFrac_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Fraction of tracks with positive IP; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
											  {"plotName":"PromptEnergyFrac2_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Charged Prompt Energy Fraction; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
                                              {"plotName":"NPromptTracks2_h_dijetNoOverlaps",
                                              "stepName":"cutvars",
                                              "stepDesc":"cutvars",
                                              "newTitle":"; Number of Prompt Tracks ; dijets / bin",
                                              "legendCoords": (0.18, 0.68, 0.63, 0.92),
                                              "stampCoords": (0.78, 0.88)
                                              },
                                            ], simulation = False
                               )
