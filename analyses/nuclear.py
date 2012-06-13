import supy,samples,calculables,steps,ROOT as r

class nuclear(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHT',min=0.5),
	    supy.steps.filters.value('PfHt',min=250),
	    supy.calculables.other.Ratio("nPV",binning = (50,-0.5,49.5),thisSample=config['baseSample'],target=('data',[]), groups=[('qcd',[])]),
	    steps.counts.counts('countsSingle'),
            steps.counts.counts('countsDouble'),
	    steps.plotjets.general("nuclSingle"),
	    steps.plotjets.tracks("nuclSingle"),
	    steps.plotjets.vertices("nuclSingle"),
	    steps.plotjets.tracks("nuclDouble"),
	    steps.plotjets.general("nuclDouble"),
	    steps.plotjets.vertices("nuclDouble"),
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
		 supy.calculables.zeroArgs(calculables) 
                 )
    
    def listOfSampleDictionaries(self) :
        return [samples.qcd,samples.data,samples.sigmc]
    
    def listOfSamples(self,config) :
	nFiles = 2 # or None for all
	qcd_bins = [str(q) for q in [80,120,170,300,470,600]]
        return (supy.samples.specify(names = "data", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, overrideLumi=0.5725) +
		supy.samples.specify(names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])], nFilesMax = nFiles, weights = 'nPVRatio') + 
		supy.samples.specify(names = "H_400_X_150", nFilesMax = nFiles, color = r.kRed))
    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
	org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
        org.scale()
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      samplesForRatios = ("data","qcd"),
                      sampleLabelsForRatios = ("data","qcd"),
		      doLog=True,
		      blackList = ["lumiHisto","xsHisto","nJobsHisto"],
                      ).plotAll()
