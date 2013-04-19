import supy,samples,calculables,steps,ROOT as r

class jetmerging(supy.analysis) :

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
 
	def dijetSteps0(self):
		mysteps = []
		for cut in self.AccCuts[1:]:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
		return([supy.steps.filters.label('Acceptance Cuts')]+mysteps)
	
	def calcsIndices(self):
		calcs = []
		for cutPrev,cutNext in zip(self.AccCuts[:-1],self.AccCuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs


	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		+self.dijetSteps0()

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
		
		+[
		steps.genjets.general()
		]

		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
		+self.calcsIndices()
		)

	def listOfSampleDictionaries(self) :
		return [samples.sigmc]
    
	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all
		sig_samples = []

		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles))

		return sig_samples

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
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
		
		self.merging(org)

	def merging(self,org):
		merging = None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'merging' in plotName: merging = step[plotName]

		for histo,sample in zip(merging,org.samples):
			H,X=sample['name'].split('_')[1],sample['name'].split('_')[3]
			list = [histo.GetBinContent(i) for i in range(1,histo.GetNbinsX()+1) ]
			list = [int(round(a/histo.Integral(),2)*100) for a in list ]
			objects = [H,X]+list
			string = " & ".join(str(a) for a in objects) + " \\\\"
			print string

