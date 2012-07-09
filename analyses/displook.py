import supy,samples,calculables,steps,ROOT as r

class displook(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHT',min=0.5),
	    supy.steps.filters.value('PfHt',min=250),
	    supy.calculables.other.Ratio("nPV",binning = (50,-0.5,49.5),thisSample=config['baseSample'],target=('data',[]), groups=[('qcd',[])]),
	    steps.counts.counts('countsSingle'),
	    steps.counts.counts('countsDouble'),
	    steps.pfjetplots.general("singleLoose"),
	    steps.pfjetplots.tracks("singleLoose"),
	    steps.trackplots.disptracks("singleLoose"),
	    steps.vertexplots.vertices("singleLoose"),
	    steps.pfjetplots.general("doubleLoose"),
	    steps.pfjetplots.double("doubleLoose"),
	    steps.pfjetplots.tracks("doubleLoose"),
	    steps.trackplots.disptracks("doubleLoose"),
	    steps.vertexplots.vertices("doubleLoose"),
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
		 supy.calculables.zeroArgs(calculables)
                 )
    
    def listOfSampleDictionaries(self) :
        return [samples.qcd,samples.data,samples.sigmc]
    
    def listOfSamples(self,config) :
	nFiles = 1 # or None for all
	qcd_bins = [str(q) for q in [80,120,170,300,470,600]]
	qcd_samples = []
	for i in range(len(qcd_bins)-1):
		name = "qcd_%s_%s" %(qcd_bins[i],qcd_bins[i+1])
		qcd_samples+=(supy.samples.specify(names = name ,nFilesMax = nFiles, color = i+3, weights='nPVRatio'))

        return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, overrideLumi=9.0456) +
		qcd_samples +
		supy.samples.specify(names = "H_400_X_150", nFilesMax = nFiles, color = r.kRed)+
		supy.samples.specify(names = "H_1000_X_20", nFilesMax = nFiles, color = r.kGreen)
		)
    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
	org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
        org.scale()
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      samplesForRatios = ("dataA","qcd"),
                      sampleLabelsForRatios = ("data","qcd"),
		      doLog=True,
		      blackList = ["lumiHisto","xsHisto","nJobsHisto"],
                      ).plotAll()
