import supy,samples,calculables,steps,ROOT as r

class ptbias(supy.analysis) :

	MH = [1000,1000,1000,1000,400,400,400,200,200,120,120]
	MX = [350,150,50,20,150,50,20,50,20,50,20]
	ctau = [35,10,4,1.5,40,8,4,20,7,50,13]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]

	AccCuts=[
		{'name':'gendijet'},
		#{'name':'genjetLxy1','max':50},
		#{'name':'genjetEta1','max':2},
		#{'name':'genjetPt1','min':40},
		#{'name':'gendijetDR','min':1.},
	]
	Cuts=[
		{'name':'jet'},
		{'name':'jetgenjetLxy','min':0,'max':50},
		{'name':'jetPt','min':40},
		#{'name':'jetgenjetPt','min':40},
	]
 
	def dijetSteps0(self):
		mysteps = []
		for cut in self.AccCuts[1:]:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
		return([supy.steps.filters.label('Acceptance Cuts')]+mysteps)

	def jetSteps(self):
		mysteps = []
		for cut in self.Cuts[-1:]:
			mysteps.append(steps.plots.genjets(njets=1,indices=cut['name']+'Indices',plot2D=True))
		return ([supy.steps.filters.label('Jet Cuts')] +mysteps)
	
	def calcsIndices(self):
		calcs = []
		for cutPrev,cutNext in zip(self.AccCuts[:-1],self.AccCuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cutPrev,cutNext in zip(self.Cuts[:-1],self.Cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs


	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		### pile-up reweighting
		#+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
        #                            target=("data/pileup/HT300_Double_R12BCD_true.root","pileup"),
        #                            groups=[('H',[])]).onlySim()] 
		### filters

		### acceptance filters
		#+[supy.steps.filters.value('genHT',min=200)]
		+self.dijetSteps0()

		#+[steps.event.effDenom(indices=self.AccCuts[-1]['name']+'Indices')]	
		#+[supy.steps.filters.value('caloHT',min=325)]
	
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
		
		#+[steps.other.genParticleMultiplicity(6003114,min=2)]
		### trigger
		+[supy.steps.filters.label("hlt trigger"),
		#steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v"),
		#supy.steps.filters.value('caloHT',min=325),
		#steps.genjets.general(),
		]
		+[
		  supy.steps.filters.multiplicity('genjetEta1',min=2,max=2),
		  supy.steps.filters.multiplicity('genjetEta2',min=2,max=2),
	    ]
		+self.jetSteps()

		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
		+self.calcsIndices()
		+[
		  calculables.Vars.jetgenjetPtDiff('jetgenjetLxyIndices'),
		  calculables.Vars.jetgenjetPhiDiff('jetgenjetLxyIndices'),
		  calculables.Vars.jetgenjetEtaDiff('jetgenjetLxyIndices'),
		 ]
		)

	def listOfSampleDictionaries(self) :
		return [samples.sigmc]
    
	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all
		sig_samples = []

		for i in range(len(self.sig_names)):
			#sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles, weights = ['pileupTrueNumInteractionsBX0Target']))
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles))

		merged_samples=[sig_samples[i] for i in [2,3,6,8,10]]
		nonmerged_samples=[sig_samples[i] for i in [0,1,4,5,7,9]]

		#return merged_samples
		return nonmerged_samples

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		#org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow X(350) #rightarrow q#bar{q}, q=uds", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "Huds_1000_X_350")
		#org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow X(150) #rightarrow q#bar{q}, q=uds", "color":r.kRed,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "Huds_1000_X_150")
		#org.mergeSamples(targetSpec = {"name":"H(400)#rightarrow X(50) #rightarrow q#bar{q}, q=uds", "color":r.kBlack,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "Huds_400_X_50")
		org.scale(lumiToUseInAbsenceOfData=18600)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			#anMode=True,
			showStatBox=True,
			pegMinimum=0.5,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()
		plotter.doLog=False
		
		'''
		plotter.individualPlots(plotSpecs = [{"plotName":"Mass_h_dijetDiscriminant",
                                              "stepName":"observables",
                                              "stepDesc":"observables",
                                              "newTitle":";Mass [GeV/c^{2}];di-jets / bin",
                                              "legendCoords": (0.45, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.88)
                                              },
											  {"plotName":"Lxy_h_dijetDiscriminant",
                                              "stepName":"observables",
                                              "stepDesc":"observables",
                                              "newTitle":";L_{xy} [cm];di-jets / bin",
                                              "legendCoords": (0.45, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                            ]
                               )
		'''
		self.profiles(org,plotter)

	def profiles(self,org,plotter):

		plotter.pdfFileName = plotter.pdfFileName.replace(self.name+'.pdf','Profiles_'+self.name+'.pdf')
		plotter.pageNumbers=False
		plotter.canvas.Clear()
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		plotter.flushPage()

		profiles = [] 
		XorY = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'genjetPtDiff' not in plotName: continue
				if issubclass(type(step[plotName][0]),r.TH2) : 
					isX = 0 if plotName.find('genjetPtDiff') == 0 else 1
					XorY.append(isX)
					profiles.append(step[plotName])

		def removeLowStats(histos):
			for histo in histos:
				for i in range(1,histo.GetNbinsX()+1):
					if histo.GetBinEntries(i)<20: 
						histo.SetBinContent(i,0)		
						histo.SetBinError(i,0)		


		for profile,isX in zip(profiles,XorY):
			plotter.canvas.Divide(3,2)
			histosX = [h.ProfileX('',1,-1,'s').Clone() for h in profile]
			histosY = [h.ProfileY('',1,-1,'').Clone() for h in profile]
			removeLowStats(histosX)
			removeLowStats(histosY)
			histos = histosX if isX else histosY
			for i,sample in enumerate(org.samples):
				name='M_{H}='+sample['name'].split('_')[1]+' M_{X}='+sample['name'].split('_')[3]
				plotter.canvas.cd(i+1)
				r.gPad.SetLeftMargin(0.15)
				r.gPad.SetRightMargin(0.05)
				histos[i].SetStats(False)
				histos[i].SetName(name)
				histos[i].SetTitle(name)
				histos[i].GetYaxis().SetTitle('(Jet pt - genJet pt) / genJet pt')
				histos[i].GetYaxis().SetTitleOffset(2.)
				histos[i].Draw()

			plotter.printCanvas()
			plotter.canvas.Clear()
		plotter.printCanvas("]")
