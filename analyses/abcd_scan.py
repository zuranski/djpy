import supy,samples,calculables,steps,ROOT as r
from calculables.utils import abcdCmp

class abcd_scan(supy.analysis) :
    
	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names_u = ["Huds_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	sig_names_b = ["Hb_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate=['dijetVtxNRatio','dijetPromptness']
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
    ]
	ABCDCuts=[]
	cut1 = [5,4,3,2,1,0.9,0.8,0.7,0.6,0.5]
	cut2 = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
	for c1 in cut1:
		for c2 in cut2:
			ABCDCuts.append([
				{'name':'dijetPromptness','max':c1,'more':'max'+str(c1)},
				{'name':'dijetDiscriminant','min':c2,'more':'min'+str(c2)},
			])

	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut is self.Cuts[-1]:
				mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.ABCDvars(indices=cut['name']+'Indices',plot2D=True))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for cuts in self.ABCDCuts:
			mysteps.append(steps.plots.ABCDplots(indices=cuts[0]['name']+'_'+cuts[1]['name']+'_ABCDIndices_'+cuts[0]['more']+'_'+cuts[1]['more']))

		#for cut in self.ABCDCuts:
		#	mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		#	mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
		#	mysteps.append(steps.plots.ABCDvars(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cuts in self.ABCDCuts:
			calcs.append(calculables.Indices.ABCDIndices(indices=self.Cuts[-1]['name']+'Indices',cuts=cuts))
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
															 #"dijetNAvgMissHitsAfterVert": (4,0.,2.),
															 #"dijetVtxmass": (6,5,40),
															 #"dijetVtxpt": (6,10,40),
															},
													indices=self.Cuts[-1]['name']+'Indices',
													bins = 50),
			   ])

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)('dijetVtxChi2Indices'))
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
			#steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60")]

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
		plotter = supy.plotter( org,
			#dependence2D=True,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("data","qcd"),
			sampleLabelsForRatios = ("data","qcd"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		#self.makeABCDmap(org,plotter)

	def makeABCDmap(self,org,plotter):
		plotter.doLog = False
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		text2 = plotter.printNEventsIn()
		plotter.flushPage()

		histo=tuple([r.TH2D('abcd'+sample['name'],'',len(self.cut1),min(self.cut1),max(self.cut1),len(self.cut2),min(self.cut2),max(self.cut2)) for sample in org.samples])
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'counts' in plotName:
					strings=plotName.split('_')
					if len(strings)>2:
						val1=strings[2][3:]
						val2=strings[3][3:strings[3].find('counts')]
						for i in range(len(step[plotName])):
							histo[i].SetBinContent(histo[i].GetXaxis().FindBin(val1),histo[i].GetYaxis().FindBin(val2),abcdCmp(step[plotName][i]))
		for h in histo:
			h.SetMinimum(-5)
			h.SetMaximum(5)
		plotter.onePlotFunction(histo)
		plotter.printCanvas("]")
		print plotter.pdfFileName, "has been written."
