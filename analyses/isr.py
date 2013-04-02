import supy,samples,calculables,steps,ROOT as r

class isr(supy.analysis) :

	MH = [1000,1000,400,400,200]
	MX = [350,150,150,50,50]
	ctau = [35,10,40,8,20]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate = ['dijetVtxNRatio','dijetPt1','dijetPt2','dijetPt1Up','dijetPt1Down','dijetPt2Up','dijetPt2Down']
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
		#{'name':'dijetTrueLxy','min':0},
        {'name':'dijetPt1','min':40},
        {'name':'dijetPt2','min':40},
		#{'name':'dijetTrueLxy','min':0},
        # vertex minimal
        #{'name':'dijetVtxChi2','min':0,'max':5},
        #{'name':'dijetVtxN1','min':1},
        #{'name':'dijetVtxN2','min':1},
        # cluster minimal
        #{'name':'dijetbestclusterN','min':2},
    ]
	
	def dijetSteps0(self):
		mysteps = []
		for cut in self.AccCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		return([supy.steps.filters.label('Acceptance Cuts')]+mysteps)
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
			if cut == self.IniCuts[-1]: mysteps.append(steps.plots.cutvars(indices=cut['name']+'Indices'))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		for cutPrev,cutNext in zip(self.AccCuts[:-1],self.AccCuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)('dijetIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		### pile-up reweighting
		+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
                                    target=("data/pileup/HT300_Double_R12BCD_true.root","pileup"),
                                    groups=[('H',[])]).onlySim()] 
		+[supy.calculables.other.Target("HPt",thisSample=config['baseSample'],
                                    target=("data/H200.root","hpt"),
                                    ).onlySim()] 
		### filters

		### acceptance filters
		#+[supy.steps.filters.value('mygenHT',min=180)]
		+self.dijetSteps0()

		+[steps.event.effDenom(indices=self.AccCuts[-1]['name']+'Indices',pdfweights=None)]	
	
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
		#steps.trigger.hltFilterWildcard("HLT_HT300_v"),
		supy.steps.filters.value('caloHT',min=325),
		]

		+self.dijetSteps1()
		+[steps.event.general()]
		+[steps.event.effNum(indices=self.IniCuts[-1]['name']+'Indices',pdfweights=None)]	
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
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target','HPtTarget']))
			#sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles, weights=['pileupTrueNumInteractionsBX0Target']))

		return sig_samples

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.scale(lumiToUseInAbsenceOfData=16740)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=True,
			#anMode=True,
			showStatBox=True,
			pegMinimum=0.5,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()
		plotter.anMode=True
		
		self.totalEfficiencies(org,dir='isr200')

	def totalEfficiencies(self,org,dir=None) :
		num,denom=None,None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'effNum' in plotName : num=step[plotName]
				if 'effDenom' in plotName : denom=step[plotName]

		efficiency = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(num,denom)])
		expos = [-0.67,-0.33,0.,0.33,0.67]
		fs = [pow(10,a) for a in expos]
		allfs = [0.1*a for a in fs] 
		allfs += fs 
		allfs += [10*a for a in fs]
		allfs = [round(a,5) for a in allfs] 
		N=len(allfs)

		import pickle,math
		for i,sample in enumerate(org.samples):
			name = sample['name'].split('.')[0]
			H,X=name.split('_')[1],name.split('_')[3]
			ctau = self.ctau[self.sig_names.index(name)]
			data={}
			for factor in set(allfs): data[factor] = []
			for j in range(N):
				x,y=r.Double(0),r.Double(0)
				efficiency[i].GetPoint(j,x,y)
				eff = float(y)
				effErr = efficiency[i].GetErrorY(j)
				factor=allfs[j]
				print H,X,factor,eff,effErr
				data[factor].append((eff,effErr))
		
			for factor in sorted(data.keys()):
				#print factor,data[factor]
				eff=data[factor]
				e=sum([a[0] for a in eff])/len(eff)
				ee=sum([a[1] for a in eff])/len(eff)
				eff=(e,ee)
				topickle = {}
				topickle['eff']=eff
				print H,X,factor,eff
				pickle.dump(topickle,open('results/'+dir+'/efficiencies/'+name+'_'+str(factor)+'.pkl','w'))
				
