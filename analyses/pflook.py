import supy,samples,calculables,steps,ROOT as r

class pflook(supy.analysis) :

	def plots(self,n):
		return [
                steps.plots.general(njets=n),
				steps.plots.fractions(njets=n),
				steps.plots.promptness(njets=n),
               ]
	
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
			steps.trigger.hltFilterWildcard("HLT_HT250_v")]

			### plots
			+[steps.event.general()]
			+self.plots(1)
		    +self.plots(2)
			  )

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
		)

	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = 1 # or None for all
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

		return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456) +
			supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1.913) +
			qcd_samples + 
			sig_samples_u + 
			sig_samples_b
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
		).plotAll()
