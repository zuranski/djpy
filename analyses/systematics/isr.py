import supy,samples,calculables,steps,ROOT as r

class isr(supy.analysis) :

	MH = [1000,1000,400,400,200]
	MX = [350,150,150,50,50]
	ctau = [35,10,40,8,20]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	AccCuts=[
		{'name':'gendijet'},
		{'name':'gendijetFlavor','max':6,'min':0},
		{'name':'gendijetLxy','max':60},
		{'name':'gendijetEta1','max':2},
		{'name':'gendijetEta2','max':2},
		{'name':'gendijetPt1','min':40},
		{'name':'gendijetPt2','min':40},
		#{'name':'gendijetDR','min':0.5},
	]
 
	IniCuts=[
        {'name':'dijet'},
		{'name':'dijetTrueLxy','min':0},
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
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=0))
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

	def listOfSteps(self,config) :
		return ([
		supy.steps.printer.progressPrinter()]
		### pile-up reweighting
		+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
                                    target=(supy.whereami()+"/../data/pileup/HT300_Double_R12BCD_true.root","pileup"),
                                    groups=[('H',[])]).onlySim()] 
		+[supy.calculables.other.Target("HPt",thisSample=config['baseSample'],
                                    target=(supy.whereami()+"/../data/H400.root","hpt"),
                                    ).onlySim()] 
		### filters
		+[steps.other.genParticleMultiplicity(pdgIds=[6001114,6002114,6003114],collection='XpdgId',min=2,max=2)]

		### acceptance filters
		#+[supy.steps.filters.value('mygenHT',min=180)]
		+self.dijetSteps0()

		+[steps.efficiency.NX(pdfweights=None)]
		+[steps.efficiency.NXAcc(indicesAcc=self.AccCuts[-1]['name']+'Indices',pdfweights=None)]	

	
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
		+[
          steps.efficiency.NXReco(pdfweights=None,
              indicesRecoLow=self.IniCuts[-1]['name']+'Indices',
              indicesRecoHigh=self.IniCuts[-1]['name']+'Indices')
         ]	
		)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
		supy.calculables.zeroArgs(calculables)
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
		
		self.totalEfficiencies(org,dir='isr400')

	def totalEfficiencies(self,org,dir=None,flavor='') :
		recoLow,recoHigh,acceptance,denom=None,None,None,None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'NXLow'+flavor == plotName : recoLow=step[plotName]
				if 'NXHigh'+flavor == plotName : recoHigh=step[plotName]
				if 'NXAcc'+flavor == plotName : acceptance=step[plotName]
				if 'NX'+flavor == plotName : denom=step[plotName]

		acc = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(acceptance,denom)])
		efflow = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(recoLow,denom)])
		effhigh = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(recoHigh,denom)])
		effacclow = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(recoLow,acceptance)])
		effacchigh = tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(recoHigh,acceptance)])
	
		fs = [0.4,0.6,1.,1.4]	
		allfs = [0.1*a for a in fs] 
		allfs += fs 
		allfs += [10*a for a in fs]
		allfs = [round(a,5) for a in allfs] 
		N=len(allfs)

		f=1.
		sysmap={'1000350':0.08,'1000150':0.08,'400150':0.1,'40050':0.08,'20050':0.22}

		import pickle,math
		for i,sample in enumerate(org.samples):
			name = sample['name'].split('.')[0]
			H,X=name.split('_')[1],name.split('_')[3]
			sys=sysmap[H+X]
			ctau = self.ctau[self.sig_names.index(name)]
			for j in range(N):
				x,y=r.Double(0),r.Double(0)
				eff = effhigh
				effacc = effacchigh
				if j<N/3: 
					eff = efflow
					effacc = effacclow
				eff[i].GetPoint(j,x,y)
				e = f*float(y)
				eErr = f*eff[i].GetErrorY(j)
				effacc[i].GetPoint(j,x,y)
				ea = f*float(y)
				eaErr = f*effacc[i].GetErrorY(j)
				acc[i].GetPoint(j,x,y)
				a = float(y)
				aErr = acc[i].GetErrorY(j)
				#if e > 0. : eErr = e*math.sqrt(sys*sys+pow(eErr/e,2))
				#else : eErr = 0.
				#if ea > 0. : eaErr = ea*math.sqrt(sys*sys+pow(eaErr/ea,2))
				#else : eaErr = 0.
				factor=allfs[j]
				print H,X,factor,a,aErr,e,eErr,ea,eaErr
				data=[(a,aErr),(e,eErr),[ea,eaErr]]
				pickle.dump(data,open(supy.whereami()+'/../results/'+dir+'/efficiencies/'+name+'_'+str(factor)+'.pkl','w'))
