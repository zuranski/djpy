import supy,samples,calculables,steps,ROOT as r

class jetmerging(supy.analysis) :

	MH = [1000,1000,1000,1000,400,400,400,200,200,120,120]
	MX = [350,150,50,20,150,50,20,50,20,50,20]
	ctau = [35,10,4,1.5,40,8,4,20,7,50,13]
	sig_names = ['H_'+str(a)+'_X_'+str(b) for a,b in zip(MH,MX)]

	AccCuts=[
		{'name':'gendijet'},
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

		+[steps.other.genParticleMultiplicity(pdgIds=[6001114,6002114,6003114],collection='XpdgId',min=2,max=2)]	
	
		+[
		steps.event.general(),
		steps.event.genevent(),
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

		toPlot=[sig_samples[i] for i in [1,2,5]] 
		#toPlot=[sig_samples[i] for i in [7,8]] 

		#return sig_samples
		return toPlot

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)

		# analysis samples
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(350)(X^{0}#rightarrow q#bar{q})", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_350")                                 
		#org.mergeSamples(targetSpec = {"name":"H^{0}(400)#rightarrow 2X^{0}(150)(X^{0}#rightarrow q#bar{q})", "color":r.kGreen,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_400_X_150")                               
		#org.mergeSamples(targetSpec = {"name":"H^{0}(200)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kBlack,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_200_X_50")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(150)(X^{0}#rightarrow q#bar{q})", "color":r.kBlue,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_150")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(400)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kMagenta,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_400_X_50")                               
		

		# gen plots samples
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(150)(X^{0}#rightarrow q#bar{q})", "color":r.kBlue,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_150")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(400)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_400_X_50")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(200)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kBlack,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_200_X_50")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(120)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kGreen,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_120_X_50")

		# dR samples
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(350)(X^{0}#rightarrow q#bar{q})", "color":r.kBlack,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_350")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(150)(X^{0}#rightarrow q#bar{q})", "color":r.kBlue,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_150")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kRed,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_50")
		#org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(20)(X^{0}#rightarrow q#bar{q})", "color":r.kGreen,"lineWidth":3,"goptions":"hist","lineStyle":2}, allWithPrefix = "H_1000_X_20")

		# effDijetSamples [1,2,5]
		org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(150)(X^{0}#rightarrow q#bar{q})", "color":r.kBlue,"lineWidth":3,"goptions":"","lineStyle":2}, allWithPrefix = "H_1000_X_150")
		org.mergeSamples(targetSpec = {"name":"H^{0}(1000)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kGreen,"lineWidth":3,"goptions":"","lineStyle":2}, allWithPrefix = "H_1000_X_50")
		org.mergeSamples(targetSpec = {"name":"H^{0}(400)#rightarrow 2X^{0}(50)(X^{0}#rightarrow q#bar{q})", "color":r.kRed,"lineWidth":3,"goptions":"","lineStyle":2}, allWithPrefix = "H_400_X_50")
		
		org.scale(lumiToUseInAbsenceOfData=18600)
		plotter = supy.plotter( org,
			pdfFileName = self.pdfFileName(org.tag),
			doLog=False,
			anMode=True,
			showStatBox=True,
			pegMinimum=0.5,
			pageNumbers=False,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
			)
		plotter.plotAll()
		org.lumi=None

		'''	
		plotter.individualPlots(simulation=True, plotSpecs = [
                                              {"plotName":"caloHT",
                                              "stepName":"general",
                                              "stepDesc":"general",
                                              "newTitle":"; H_{T} [GeV]; events / bin",
                                              "legendCoords": (0.5, 0.65, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"HPt",
                                              "stepName":"genevent",
                                              "stepDesc":"genevent",
                                              "newTitle":"; H^{0} p_{T} [GeV]; events / bin",
                                              "legendCoords": (0.5, 0.65, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"betagamma",
                                              "stepName":"genevent",
                                              "stepDesc":"genevent",
                                              "newTitle":"; H^{0} #beta#gamma; events / bin",
                                              "legendCoords": (0.5, 0.65, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"XPt",
                                              "stepName":"genevent",
                                              "stepDesc":"genevent",
                                              "newTitle":"; X^{0} p_{T} [GeV]; X^{0} / bin",
                                              "legendCoords": (0.5, 0.65, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"XEta",
                                              "stepName":"genevent",
                                              "stepDesc":"genevent",
                                              "newTitle":"; X^{0} #eta ; X^{0} / bin",
                                              "legendCoords": (0.35, 0.15, 0.75, 0.45),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              {"plotName":"XDR",
                                              "stepName":"genevent",
                                              "stepDesc":"genevent",
                                              "newTitle":"; q#bar{q} #Delta R; X^{0} / bin",
                                              "legendCoords": (0.5, 0.65, 0.9, 0.85),
                                              "stampCoords": (0.7, 0.88)
                                              },
                                              #{"plotName":"dPhi",
                                              #"stepName":"general",
                                              #"stepDesc":"general",
                                              #"newTitle":"; #Delta #phi (dijet, X^{0}); X^{0} / bin",
                                              #"legendCoords": (0.2, 0.68, 0.5, 0.88),
                                              #"stampCoords": (0.72, 0.88)
                                              #},
                                              #{"plotName":"dPhiReduced",
                                              #"stepName":"general",
                                              #"stepDesc":"general",
                                              #"newTitle":"; #Delta #phi (dijet, X^{0}) / #Delta #phi (q#bar{q}); X^{0} / bin",
                                              #"legendCoords": (0.2, 0.68, 0.5, 0.88),
                                              #"stampCoords": (0.72, 0.88)
                                              #},
                                            ]
                               )
		'''
		self.merging(org,plotter)

	def merging(self,org,plotter):
		#plotter.doLog=False
		num,denom=None,None
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if 'ndR' == plotName: profile = step[plotName]
				if 'dRnum' == plotName: num = step[plotName]
				if 'dRdenom' == plotName: denom = step[plotName]

		print num,denom

		for i,sample in enumerate(org.samples):
			n,d=num[i],denom[i]
			print sample['name']
			for iX in range(1,d.GetNbinsX()+1):
				print n.GetBinContent(iX),d.GetBinContent(iX)
				if d.GetBinContent(iX)>0 and d.GetBinError(iX)/d.GetBinContent(iX)>0.1:
					print d.GetBinContent(iX)
					n.SetBinContent(iX,0)
					d.SetBinContent(iX,0)

		#eff=tuple([r.TGraphAsymmErrors(n,d,"cl=0.683 n") for n,d in zip(num,denom)])
		eff=tuple([n.Divide(d) for n,d in zip(num,denom)])
		eff=num
		plotter.individualPlots(simulation=True, plotSpecs = [
                                              {"plotName":"effDijet",
                                              "histos":eff,
                                              "newTitle":"; q#bar{q} #Delta R;dijet efficiency",
                                              "legendCoords": (0.2, 0.58, 0.55, 0.78),
                                              "stampCoords": (0.4, 0.88)
                                              },
                                              {"plotName":"dRdenom",
                                              "histos":denom,
                                              "newTitle":"; q#bar{q} #Delta R; X^{0} / bin",
                                              "legendCoords": (0.2, 0.58, 0.55, 0.78),
                                              "stampCoords": (0.4, 0.88)
                                              }
											],
								)
