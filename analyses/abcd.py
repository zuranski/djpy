import supy,samples,calculables,steps,ROOT as r

class abcd(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHT',min=0.5),
	    supy.steps.filters.value('PfHt',min=250),
	    supy.calculables.other.Ratio("nPV",binning = (50,-0.5,49.5),thisSample=config['baseSample'],target=('data',[]), groups=[('qcd',[])]),
	    steps.counts.counts('countsDouble'),
	    steps.abcdplots.abcd_histo("abcd_vtxNRatio_lxysig",binning1=(50,0,1),binning2=(50,0,100)),
	    steps.abcdplots.abcd_histo("abcd_posip2dFrac_lxysig",binning1=(50,0.,1.),binning2=(50,0,100)),
	    steps.abcdplots.abcd_histo("abcd_PromptEnergyFrac_lxysig",binning1=(50,0.,1.),binning2=(50,0.,50.)),
	    steps.abcdplots.abcd_histo("abcd_PromptEnergyFrac_vtxNRatio",binning1=(50,0.,1.),binning2=(50,0.,1.)),
	    steps.abcdplots.abcd_histo("abcd_PromptEnergyFrac_bestclusterlxy",binning1=(50,0.,1.),binning2=(50,0.,1.5)),
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
		 supy.calculables.zeroArgs(calculables)
                 )
    
    def listOfSampleDictionaries(self) :
        return [samples.qcd,samples.data,samples.sigmc]
    
    def listOfSamples(self,config) :
	nFiles = None # or None for all
	nEvents = None # or None for all
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_samples = []
	for i in range(len(qcd_bins)-1):
		name = "qcd_%s_%s" %(qcd_bins[i],qcd_bins[i+1])
		qcd_samples+=(supy.samples.specify(names = name ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights='nPVRatio'))

        return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456) +
		qcd_samples +
		supy.samples.specify(names = "H_400_X_150", nFilesMax = nFiles, nEventsMax = nEvents, color = r.kRed)+
		supy.samples.specify(names = "H_1000_X_20", nFilesMax = nFiles, nEventsMax = nEvents, color = r.kGreen)
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
