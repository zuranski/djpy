import itertools,supy,samples,calculables,steps,ROOT as r
from utils.ABCDscan import plotABCDscan

class abcdHT(supy.analysis) :
    
	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate=['dijetVtxNRatio']
	ToCalculate += ['dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']

	IniCuts=[
        {'name':'dijet'},
        #{'name':'dijetTrueLxy','min':0},
        # vertex minimal
        {'name':'dijetVtxChi2','min':0,'max':5},
        {'name':'dijetVtxN1','min':1},
        {'name':'dijetVtxN2','min':1},
        # cluster minimal
        {'name':'dijetbestclusterN','min':2},
    ]
	Cuts=[
        # clean up cuts 
        {'name':'dijetNAvgMissHitsAfterVert','max':2},
        {'name':'dijetVtxmass','min':4},
        {'name':'dijetVtxpt','min':8},
        {'name':'dijetVtxNRatio','min':0.1},
        {'name':'dijetLxysig','min':8},
        {'name':'dijetNoOverlaps','val':True},
        {'name':'dijetTrueLxy','min':0},
    ]
	ABCDCutsSets = []
	scanPrompt = [(8,0.45),(7,0.4),(6,0.35),(5,0.3),(4,0.25),(3,0.2),(2,0.15)]
	scanVtx = [1e-5,1e-4,1e-3,1e-2,0.1,0.3,0.85]

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
			if cut is self.Cuts[-1]:
				mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
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
			calcs.append(calculables.Indices.ABCDEFGHIndices(indices=self.Cuts[-1]['name']+'Indices',
															 cuts=self.ABCDCutsSets[i],suffix=str(i)))
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
															 #"dijetNAvgMissHitsAfterVert": (6,0.,3.),
															 #"dijetVtxpt": (10,0,50),
															},
													indices=self.Cuts[-1]['name']+'Indices',
													bins = 14),
			   ])

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
				target=("data/pileup/HT300_R12BCD_true.root","pileup"),
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
			supy.steps.filters.value("caloHT",min=325),]

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
		sig_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupTrueNumInteractionsBX0Target']))
		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target']))

		return (qcd_samples
			    + sig_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			#anMode=True,
			showStatBox=False,
			pageNumbers=False,
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		plotABCDscan(self,org,plotter,8)

		plotter.individualPlots(plotSpecs = [{"plotName":"NPromptTracks1_h_dijetTrueLxy",
                                              "stepName":"ABCDvars",
                                              "stepDesc":"ABCDvars",
                                              "newTitle":"; N Prompt Tracks (jet 2) ;di-jets / bin",
                                              "legendCoords": (0.58, 0.7, 0.78, 0.9),
                                              "stamp": False 
                                              },
											 {"plotName":"PromptEnergyFrac1_h_dijetTrueLxy",
                                              "stepName":"ABCDvars",
                                              "stepDesc":"ABCDvars",
                                              "newTitle":"; Prompt Energy Fraction (jet 2) ;di-jets / bin",
                                              "legendCoords": (0.58, 0.7, 0.78, 0.9),
                                              "stamp": False 
                                              },
											  {"plotName":"Discriminant_h_dijetTrueLxy",
                                              "stepName":"ABCDvars",
                                              "stepDesc":"ABCDvars",
                                              "newTitle":"; Vertex/Cluster Discriminant ;di-jets / bin",
                                              "legendCoords": (0.58, 0.7, 0.78, 0.9),
                                              "stamp": False 
                                              },])


