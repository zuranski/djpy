import supy,samples,calculables,steps,ROOT as r

class efficiency(supy.analysis) :

	MH = [1000,1000,400,400,200]
	MX = [350,150,150,50,50]
	ctau = [35,10,40,8,20]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate = ['dijetVtxNRatio']
	ToCalculate += ['dijetNPromptTracks1','dijetNPromptTracks2','dijetPromptEnergyFrac1','dijetPromptEnergyFrac2']   

	AccCuts=[
		{'name':'gendijet'},
		#{'name':'gendijetLxy','max':50},
		#{'name':'gendijetEta1','max':2},
		#{'name':'gendijetEta2','max':2},
		#{'name':'gendijetPt1','min':40},
		#{'name':'gendijetPt2','min':40},
		#{'name':'gendijetDR','min':1.},
	]
 
	IniCuts=[
        {'name':'dijet'},
        {'name':'dijetPt1','min':40},
        {'name':'dijetPt2','min':40},
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
        {'name':'dijetNAvgMissHitsAfterVert','max':2},
        {'name':'dijetVtxmass','min':4},
        {'name':'dijetVtxpt','min':8},
        {'name':'dijetVtxNRatio','min':0.1},
        {'name':'dijetLxysig','min':8},
        {'name':'dijetNoOverlaps','val':True},
    ]
	
	ABCDCutsLow = [
		{'name':'Prompt1','vars':({'name':'dijetNPromptTracks1','max':1},
   	                              {'name':'dijetPromptEnergyFrac1','max':0.15})
		},
		{'name':'Prompt2','vars':({'name':'dijetNPromptTracks2','max':1},
	                              {'name':'dijetPromptEnergyFrac2','max':0.15})
		},
		{'name':'Disc','vars':({'name':'dijetDiscriminant','min':0.9},)}
		]
	
	ABCDCutsHigh = [
		{'name':'Prompt1','vars':({'name':'dijetNPromptTracks1','max':1},
   	                              {'name':'dijetPromptEnergyFrac1','max':0.09})
		},
		{'name':'Prompt2','vars':({'name':'dijetNPromptTracks2','max':1},
	                              {'name':'dijetPromptEnergyFrac2','max':0.09})
		},
		{'name':'Disc','vars':({'name':'dijetDiscriminant','min':0.8},)}
		]
	ABCDCutsSets=[ABCDCutsLow,ABCDCutsHigh]

	def dijetSteps0(self):
		mysteps = []
		for cut in self.AccCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		return([supy.steps.filters.label('Acceptance Cuts')]+mysteps)
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts+self.Cuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut == self.IniCuts[-1]: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			if cut == self.Cuts[-1]: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			if cut == self.ABCDCutsHigh[-1]: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def dijetSteps2(self):
		mysteps=[]
		for i in range(len(self.ABCDCutsSets)) :
			mysteps.append(steps.plots.ABCDEFGHplots(indices='ABCDEFGHIndices'+str(i)))
			mysteps.append(steps.event.effNum(indices='ABCDEFGHIndices'+str(i)).onlySim())
		for cut in self.ABCDCutsLow:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut == self.ABCDCutsLow[-1]: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
			if cut == self.ABCDCutsLow[-1]: mysteps.append(steps.plots.observables(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet ABCD cuts filters')]+mysteps)


	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts + self.Cuts +self.ABCDCutsLow
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for i in range(len(self.ABCDCutsSets)) :
			calcs.append(calculables.Indices.ABCDEFGHIndices(indices=self.Cuts[-1]['name']+'Indices',
                                                             cuts=self.ABCDCutsSets[i],suffix=str(i)))
		for cutPrev,cutNext in zip(self.AccCuts[:-1],self.AccCuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def discs(self):
		discSamplesRight=[name+'.pileupTrueInteractionsBX0Target' for name in self.sig_names]
		discSamplesLeft=[name+'.pileupTrueInteractionsBX0Target' for name in self.qcd_names]
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
			calcs.append(getattr(calculables.Vars,calc)('dijetIndices'))
		calcs.append(calculables.Overlaps.dijetNoOverlaps('dijetLxysigIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		### pile-up reweighting
		+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
                                    target=("data/pileup/HT300_Double_R12BCD_true.root","pileup"),
                                    groups=[('H',[])]).onlySim()] 
		### filters

		### acceptance filters
		#+[supy.steps.filters.value('mygenHT',min=180)]
		+self.dijetSteps0()

		+[steps.event.effDenom(indices=self.AccCuts[-1]['name']+'Indices')]	
	
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
		steps.trigger.hltFilterWildcard("HLT_HT300_DoubleDisplacedPFJet60_v"),
		supy.steps.filters.value('caloHT',min=325),
		]

		+self.dijetSteps1()
		+self.discs()
		+self.dijetSteps2()
		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
		+self.calcsVars()
		+self.calcsIndices()
		)

	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]
    
	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all
		sig_samples = []

		for i in range(len(self.sig_names)):
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles, weights = ['pileupTrueNumInteractionsBX0Target']))
			#sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles))

		return sig_samples

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		#org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow X(350) #rightarrow q#bar{q}", "color":r.kBlue,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "H_1000_X_350")
		#org.mergeSamples(targetSpec = {"name":"H(1000)#rightarrow X(150) #rightarrow q#bar{q}", "color":r.kRed,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "H_1000_X_150")
		#org.mergeSamples(targetSpec = {"name":"H(400)#rightarrow X(50) #rightarrow q#bar{q}", "color":r.kBlack,"lineWidth":3,"goptions":"hist"}, allWithPrefix = "H_400_X_50")
		org.scale(lumiToUseInAbsenceOfData=16740)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			anMode=True,
			showStatBox=True,
			pegMinimum=0.5,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()
		#plotter.doLog=False
		plotter.anMode=True
		
		
		plotter.individualPlots(plotSpecs = [{"plotName":"Mass_h_Disc",
                                              "stepName":"observables",
                                              "stepDesc":"observables",
                                              "newTitle":";Mass [GeV/c^{2}];di-jets / bin",
                                              "legendCoords": (0.45, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.88)
                                              },
											  {"plotName":"Lxy_h_Disc",
                                              "stepName":"observables",
                                              "stepDesc":"observables",
                                              "newTitle":";L_{xy} [cm];di-jets / bin",
                                              "legendCoords": (0.45, 0.55, 0.9, 0.75),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                            ]
                               )
		
		self.totalEfficiencies(org,dir='final')

	def totalEfficiencies(self,org,dir=None) :
		num0,nump,numm,denom=[],[],[],None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'effNum0' in plotName : num0.append(step[plotName])
				if 'effNumm' in plotName : numm.append(step[plotName])
				if 'effNump' in plotName : nump.append(step[plotName])
				if 'effDenom' in plotName : denom=step[plotName]

		efficiency0low = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(num0[0],denom)])
		efficiencymlow = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(numm[0],denom)])
		efficiencyplow = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(nump[0],denom)])
		efficiency0high = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(num0[1],denom)])
		efficiencymhigh = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(numm[1],denom)])
		efficiencyphigh = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(nump[1],denom)])

		import pickle,math
		for i,sample in enumerate(org.samples):
			name = sample['name'].split('.')[0]
			H,X=name.split('_')[1],name.split('_')[3]
			ctau = self.ctau[self.sig_names.index(name)]
			data={}
			for j in range(3):
				x,y=r.Double(0),r.Double(0)
				efficiency0 = efficiency0high
				efficiencym = efficiencymhigh
				efficiencyp = efficiencyphigh
				if j==0: 
					efficiency0 = efficiency0low
					efficiencym = efficiencymlow
					efficiencyp = efficiencyplow
				efficiency0[i].GetPoint(j,x,y)
				eff = float(y)
				effErr = efficiency0[i].GetErrorY(j)
				if eff > 0. : effErr = eff*math.sqrt(0.15*0.15+pow(effErr/eff,2))
				else : effErr = 0.
				data['eff']=(eff,effErr)
				factor=pow(10,int(x-1))
				pickle.dump(data,open('results/'+dir+'/efficiencies/'+name+'_'+str(factor)+'.pkl','w'))
				
				efficiencym[i].GetPoint(j,x,y)
				eff = float(y)
				effErr = efficiencym[i].GetErrorY(j)
				if eff > 0. : effErr = eff*math.sqrt(0.15*0.15+pow(effErr/eff,2))
				else : effErr = 0.
				data['eff']=(eff,effErr)
				factor=pow(10,int(x-1))*pow(10,-1./3.)
				pickle.dump(data,open('results/'+dir+'/efficiencies/'+name+'_'+str(factor)+'.pkl','w'))

				efficiencyp[i].GetPoint(j,x,y)
				eff = float(y)
				effErr = efficiencyp[i].GetErrorY(j)
				if eff > 0. : effErr = eff*math.sqrt(0.15*0.15+pow(effErr/eff,2))
				else : effErr = 0.
				data['eff']=(eff,effErr)
				factor=pow(10,int(x-1))*pow(10,+1./3.)
				pickle.dump(data,open('results/'+dir+'/efficiencies/'+name+'_'+str(factor)+'.pkl','w'))

