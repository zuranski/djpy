import itertools,supy,samples,calculables,steps,ROOT as r
from utils.ABCDscan import plotABCDscan,plotExpLimit

class abcdHTDouble(supy.analysis) :
    
	MH = [1000,1000,400,400,200]
	MX = [350,150,150,50,50]
	sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	IniCuts=[
        {'name':'dijet'},
        # vertex minimal
        {'name':'dijetVtxN1','min':1},
        {'name':'dijetVtxN2','min':1},
        # cluster minimal
        {'name':'dijetbestclusterN','min':2},
        {'name':'dijetVtxChi2','min':0,'max':5},
    ]
	Cuts=[
        # clean up cuts 
        {'name':'dijetLxysig','min':8},
        {'name':'dijetVtxmass','min':4},
        {'name':'dijetVtxpt','min':8},
        {'name':'dijetNAvgMissHitsAfterVert','max':2},
        #{'name':'dijetTrueLxy','min':0},
        #{'name':'dijetNoOverlaps','val':True},
        {'name':'dijetBestCand','val':True},
    ]
	ABCDCutsSets = []
	scanPrompt = [(2,0.15),(2,0.13),(2,0.11),(2,0.09),(2,0.07),(2,0.05)]
	scanPrompt += [(1,0.15),(1,0.13),(1,0.11),(1,0.09),(1,0.07),(1,0.05)]
	scanPrompt += [(0,0.15),(0,0.13),(0,0.11),(0,0.09),(0,0.07),(0,0.05)]
	scanVtx = [0.7,0.8,0.9,0.95]

	scan = [(obj[0],obj[0],obj[1]) for obj in itertools.product(scanPrompt,scanVtx)]

	for val in scan :
		ABCDCutsSets.append([
		{'name':'Prompt1','vars':({'name':'dijetNPromptTracks1','max':val[0][0]},
   	                              {'name':'dijetPromptEnergyFrac1','max':val[0][1]})
		},
		{'name':'Prompt2','vars':({'name':'dijetNPromptTracks2','max':val[1][0]},
	                              {'name':'dijetPromptEnergyFrac2','max':val[1][1]})
		},
		{'name':'Disc','vars':({'name':'dijetDiscriminant','min':val[2]},)},
		])	
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			if cut is self.Cuts[-1]:
				#mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.ABCDvars(indices=cut['name']+'Indices',plot2D=True))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for i in range(len(self.ABCDCutsSets)) :
			mysteps.append(steps.plots.ABCDEFGHplots(indices='ABCDEFGHIndices'+str(i)))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts + self.ABCDCutsSets[-1]
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for i in range(len(self.ABCDCutsSets)) :
			calcs.append(calculables.Indices.ABCDEFGHIndices(indices=self.Cuts[-1]['name']+'Indices', cuts=self.ABCDCutsSets[i],suffix=str(i)))
		return calcs

	def discs(self):
		discSamplesRight=[name+'.pileupTrueNumInteractionsBX0Target' for name in self.sig_names]
		discSamplesLeft=[name+'.pileupTrueNumInteractionsBX0Target' for name in self.qcd_names]
		return([supy.calculables.other.Discriminant(fixes=("dijet",""),
													right = {"pre":"H","tag":"","samples":discSamplesRight},
													left = {"pre":"qcd","tag":"","samples":discSamplesLeft},
													dists = {"dijetVtxN":(7,1.5,8.5),
															 "dijetglxyrmsclr": (10,0,1),
															 "dijetbestclusterN": (7,1.5,8.5),
															 "dijetPosip2dFrac": (5,0.5001,1.001),
															},
													indices=self.Cuts[-1]['name']+'Indices',
													bins = 14),
			   ])

	def calcsVars(self):
		calcs = []
		calcs.append(calculables.Overlaps.dijetNoOverlaps('dijetLxysigIndices'))
		#calcs.append(calculables.Overlaps.dijetBestCand('dijetNoOverlapsIndices'))
		calcs.append(calculables.Overlaps.dijetBestCand('dijetLxysigIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
				target=(supy.whereami()+"/../data/pileup/HT300_Double_R12BCD_true.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			### signal filters
			+[steps.other.genParticleMultiplicity(pdgIds=[6002114],collection='XpdgId',min=2,max=2).onlySim()]
			+[steps.efficiency.NE(pdfweights=None).onlySim()]	

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
            steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v"),
			supy.steps.filters.value("caloHT",min=325),
			#steps.event.runModulo(modulo=11,inverted=True).onlyData(),
			]

			### plots
			+[steps.event.general()]
			+self.dijetSteps1()
			+[supy.steps.histos.multiplicity(self.Cuts[-2]['name']+'Indices')]
			+[supy.steps.histos.multiplicity(self.Cuts[-1]['name']+'Indices')]
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
		sig_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target']))
	
		factor=1

		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4430*factor) 
			+ supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=495.03*factor) 
			+ supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6401.3*factor) 
			+ supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=7274*factor)
			#+ qcd_samples
			+sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		#org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			pageNumbers=False,
			doLog=True,
			dependence2D=False,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		plotABCDscan(self,org,plotter,8,blind=False)
		plotExpLimit(self,8,org)
