import itertools,supy,samples,calculables,steps,ROOT as r
from utils.ABCDscan import plotABCDscan,plotExpLimit

class finSelection(supy.analysis) :
   
	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	sig_names = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]
 
	ToCalculate = ['dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']
	ToCalculate +=['dijetPt1','dijetPt2']

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
        {'name':'dijetVtxmass','min':4},
        {'name':'dijetVtxpt','min':8},
        {'name':'dijetNAvgMissHitsAfterVert','max':2},
        {'name':'dijetLxysig','min':8},
        {'name':'dijetNoOverlaps','val':True},
        {'name':'dijetTrueLxy','min':0},
    ]

	ABCDCutsLow = [
        {'name':'Prompt1Low','vars':({'name':'dijetNPromptTracks1','max':1},
                                  {'name':'dijetPromptEnergyFrac1','max':0.15})
        },
        {'name':'Prompt2Low','vars':({'name':'dijetNPromptTracks2','max':1},
                                  {'name':'dijetPromptEnergyFrac2','max':0.15})
        },
        {'name':'DiscLow','vars':({'name':'dijetDiscriminant','min':0.9},)}
        ]

	ABCDCutsHigh = [
        {'name':'Prompt1High','vars':({'name':'dijetNPromptTracks1','max':1},
                                  {'name':'dijetPromptEnergyFrac1','max':0.09})
        },
        {'name':'Prompt2High','vars':({'name':'dijetNPromptTracks2','max':1},
                                  {'name':'dijetPromptEnergyFrac2','max':0.09})
        },
        {'name':'DiscHigh','vars':({'name':'dijetDiscriminant','min':0.8},)}
        ]
	ABCDCutsSets=[ABCDCutsLow,ABCDCutsHigh]

	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut is self.Cuts[-1]:
				mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
				mysteps.append(steps.plots.ABCDvars(indices=cut['name']+'Indices',plot2D=True,plot1D=False))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for i in range(len(self.ABCDCutsSets)) :
			mysteps.append(steps.plots.ABCDEFGHplots(indices='ABCDEFGHIndices'+str(i)))
		for cutSet in self.ABCDCutsSets:
			mysteps.append(steps.plots.cutvars(indices=cutSet[-1]['name']+'Indices'))
			mysteps.append(steps.plots.observables(indices=cutSet[-1]['name']+'Indices'))
			mysteps.append(steps.other.collector(indices=cutSet[-1]['name']+'Indices',
            vars=['dijetDiscriminant',
				  'dijetNPromptTracks1',
                  'dijetNPromptTracks2',
                  'dijetPromptEnergyFrac1',
				  'dijetPromptEnergyFrac2',
				  'dijetMass',
				  'dijetVtxN1',
				  'dijetVtxN2',
				  'dijetPt1',
				  'dijetPt2',
				  'dijetLxy',
                  'run',
                  'lumiSection',
                  'event']))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts
		cutsLow = self.Cuts[-1:] + self.ABCDCutsSets[0]
		cutsHigh = self.Cuts[-1:] + self.ABCDCutsSets[1]
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cutPrev,cutNext in zip(cutsLow[:-1],cutsLow[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cutPrev,cutNext in zip(cutsHigh[:-1],cutsHigh[1:]):
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
				target=("data/pileup/HT300_Double_R12BCD_true.root","pileup"),
				groups=[('qcd',[]),('H',[])]).onlySim()] 

			+[steps.event.effDenom().onlySim()]

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

		return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=4430*0.9) 
			+ supy.samples.specify(names = "dataC1", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=495.03*0.9) 
			+ supy.samples.specify(names = "dataC2", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=6401.3*0.9) 
			+ supy.samples.specify(names = "dataD", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=7274*0.9)
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		#org.mergeSamples(targetSpec = {"name":"QCD", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"Data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		#org.mergeSamples(targetSpec = {"name":"H#rightarrow X #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			pageNumbers=False,
			doLog=True,
			dependence2D=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		#plotABCDscan(self,org,plotter,8,blind=False)
		#plotExpLimit(self,8,org)
