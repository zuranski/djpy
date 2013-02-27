import supy,samples,calculables,steps,ROOT as r

class jetmerging(supy.analysis) :

	MH = [1000,1000,1000,400,400,200]
	MX = [350,150,50,150,50,50]
	ctau = [35,10,4,40,8,20]
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
		### pile-up reweighting
		+[supy.calculables.other.Target("pileupTrueNumInteractionsBX0",thisSample=config['baseSample'],
                                    target=("data/pileup/HT300_Double_R12BCD_true.root","pileup"),
                                    groups=[('H',[])]).onlySim()] 
		### filters

		### acceptance filters
		#+[supy.steps.filters.value('genHT',min=200)]
		+self.dijetSteps0()

		+[steps.event.effDenom(indices=self.AccCuts[-1]['name']+'Indices')]	
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
			sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles, weights = ['pileupTrueNumInteractionsBX0Target']))
			#sig_samples+=(supy.samples.specify(names = self.sig_names[i], markerStyle=20, color=i+1,  nEventsMax=nEvents, nFilesMax=nFiles))

		return sig_samples

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
		#self.totalEfficiencies(org,dir='final')
		self.merging(org)

	def merging(self,org):
		merging = None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'merging' in plotName: merging = step[plotName]

		for histo,sample in zip(merging,org.samples):
			for i in range(1,histo.GetNbinsX()+1):
				print i-1,histo.GetBinContent(i)/histo.Integral(), sample['name']

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

