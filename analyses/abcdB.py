import supy,samples,calculables,steps,ROOT as r

class abcdB(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHTdjpt',min=0.5),
	    supy.steps.filters.value('PfHt',min=250),
	    supy.calculables.other.Ratio("nPV",binning = (50,-0.5,49.5),thisSample=config['baseSample'],target=('data',[]), groups=[('qcd',[])]),
	    #steps.counts.histos('countsDouble'),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_glxyrmsvtx",binning1=(50,0.,5.),binning2=(50,0.,2.5)),
	    steps.abcdplots.abcd_counts("abcd_Promptness_glxyrmsvtx"),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_posip2dFrac",binning1=(50,0.,5.),binning2=(50,0.,1.)),
	    steps.abcdplots.abcd_counts("abcd_Promptness_posip2dFrac"),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_vtxpt",binning1=(50,0.,5.),binning2=(100,0.,100.)),
	    #steps.abcdplots.abcd_counts("abcd_Promptness_vtxpt"),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_vtxmass",binning1=(50,0.,5.),binning2=(100,0.,50.)),
	    steps.abcdplots.abcd_counts("abcd_Promptness_vtxmass"),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_vtxN",binning1=(50,0.,5.),binning2=(15,0.5,15.5)),
	    steps.abcdplots.abcd_counts("abcd_Promptness_vtxN"),
	    #steps.abcdplots.abcd_histo("abcd_Promptness_nAvgMissHitsAfterVert",binning1=(50,0.,5.),binning2=(12,0.,6.)),
	    steps.abcdplots.abcd_counts("abcd_Promptness_nAvgMissHitsAfterVert"),
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

        return (supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1828.) +
		qcd_samples +
		supy.samples.specify(names = "H_400_X_150", nFilesMax = nFiles, nEventsMax = nEvents, color = r.kRed)
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
		      blackList = ["lumiHisto","xsHisto","nJobsHisto","allweighted","logMyValue","meweighted","unweighted"],
                      ).plotAll()
