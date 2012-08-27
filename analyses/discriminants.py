import supy,samples,calculables,steps,ROOT as r

class discriminants(supy.analysis) :
 
    MH = [1000,1000,1000,400,400,200]
    MX = [350,150,50,150,50,50]
    sig_names_u = ["H_"+str(a)+"_X_"+str(b) for a,b in zip(MH,MX)]
    sig_names_b = ["H_"+str(a)+"_X_"+str(b)+"b" for a,b in zip(MH,MX)]
 
    qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
    qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]
    def listOfSteps(self,config) :
	discSamplesLeft = [name+".nPVRatio" for name in self.qcd_names]
	discSamplesRight = [name+".nPVRatio" for name in (self.sig_names_u + self.sig_names_b)]
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHT',min=0.5),
	    supy.steps.filters.value('PfHt',min=250),
	    supy.calculables.other.Ratio("nPV",binning = (50,-0.5,49.5),thisSample=config['baseSample'],target=('data',[]), groups=[('qcd',[]),('H',[])]),
	    supy.calculables.other.Discriminant(fixes=("","promptness"),
						right = {"pre":"H","tag":"","samples":discSamplesRight},
						left = {"pre":"qcd","tag":"","samples":discSamplesLeft},
						dists = {"doublePromptEnergyFrac":(10,0,0.2),
							 "doublenPrompt": (12,-0.5,11.5),
							},
						bins = 15),
	    supy.calculables.other.Discriminant(fixes=("","kin"),
						right = {"pre":"H","tag":"","samples":discSamplesRight},
						left = {"pre":"qcd","tag":"","samples":discSamplesLeft},
						dists = {"doublevtxpt": (25,0,100),
							 "doublevtxmass":(25,5,100),
							 "doublevtxptRatio":(25,0,1),
							},
						bins = 15),
	    supy.calculables.other.Discriminant(fixes=("","vtxQual"),
						right = {"pre":"H","tag":"","samples":discSamplesRight},
						left = {"pre":"qcd","tag":"","samples":discSamplesLeft},
						dists = {"doublevtxN":(5,1.5,6.5),
							 "doublenAvgMissHitsAfterVert": (6,0,3),
							 "doubleglxydistclr": (15,0,0.5),
							 "doublebestclusterN": (5,1.5,6.5),
							},
						bins = 15),
	    steps.discplots.general('candsDoubleDisc'),
	    steps.counts.discs('countsDoubleDisc'),
	    steps.pfjetplots.general("doubleDisc"),
	    steps.pfjetplots.double("doubleDisc"),
	    steps.pfjetplots.tracks("doubleDisc"),
	    steps.pfjetplots.discs("doubleDisc"),
	    steps.vertexplots.vertices("doubleDisc"),
	    steps.trackplots.clusters("doubleDisc"),
	    steps.trackplots.disptracks("doubleDisc"),
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
		 supy.calculables.zeroArgs(calculables)
                 )
    
    def listOfSampleDictionaries(self) :
        return [samples.qcd,samples.data,samples.sigmc]
    
    def listOfSamples(self,config) :
	nFiles = None  # or None for all
	nEvents = None # or None for all
	qcd_samples = []
	sig_samples_u = []
	sig_samples_b = []
	for i in range(len(self.qcd_names)):
		qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights="nPVRatio"))
	for i in range(len(self.sig_names_u)):
                sig_samples_u+=(supy.samples.specify(names = self.sig_names_u[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights='nPVRatio'))
	for i in range(len(self.sig_names_b)):
                sig_samples_b+=(supy.samples.specify(names = self.sig_names_b[i], color=i+1, markerStyle=20, nEventsMax=nEvents, nFilesMax=nFiles, weights='nPVRatio'))


        return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456) +
        	supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1.913) +
		qcd_samples + sig_samples_u + sig_samples_b
		)
    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
	org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
	org.mergeSamples(targetSpec = {"name":"data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
	org.mergeSamples(targetSpec = {"name":"H", "color":r.kRed}, allWithPrefix = "H")
        org.scale()
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      samplesForRatios = ("data","qcd"),
                      sampleLabelsForRatios = ("data","qcd"),
		      doLog=True,
		      blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		      dependence2D = True,
                      ).plotAll()
