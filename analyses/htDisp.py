import supy,samples,calculables,steps,ROOT as r

class htDisp(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHTdjpt',min=0.5),
	    steps.event.general(),
	    steps.pfjets.general(),
	    steps.pfjets.fractions(),
	    steps.pfjets.tracks(),
	    steps.pfjets.vertices()
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
		 supy.calculables.zeroArgs(calculables) 
                 )
    
    def listOfSampleDictionaries(self) :
        return [samples.qcd,samples.data]
    
    def listOfSamples(self,config) :
	nFiles = None # or None for all
	qcd_bins = [str(q) for q in [80,120,170,300,470,600]]
        return (supy.samples.specify(names = "data", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, overrideLumi=474.626) +
		supy.samples.specify(names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])], nFilesMax = nFiles))
    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
	org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
        org.scale()
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      samplesForRatios = ("data","qcd"),
                      sampleLabelsForRatios = ("data","qcd"),
		      pegMinimum=0.1,
		      doLog=True,
		      blackList = ["lumiHisto","xsHisto","nJobsHisto"],
                      ).plotAll()
