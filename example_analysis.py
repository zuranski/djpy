import supy, ROOT as r
from steps import jetHistogramer 

class example_analysis(supy.analysis) :
    
    def listOfSteps(self,config) :
        return [
            supy.steps.printer.progressPrinter(),
	    supy.steps.filters.value('trigHT',min=0.5),
	    supy.steps.filters.value('ht',min=250),
	    #supy.steps.filters.value('npfjets',min=2),
            supy.steps.histos.value('ht',100,-1,1e3),
            supy.steps.histos.value('pfht',100,-1,1e3),
            supy.steps.histos.value('njets',18,-2,15),
            supy.steps.histos.value('npfjets',17,-1,15),
            supy.steps.histos.value('nPV',52,-1,50),
            supy.steps.histos.value('nTrks',100,-1,2500),
	    jetHistogramer(),
            ]
    
    def listOfCalculables(self,config) :
        return ( supy.calculables.zeroArgs(supy.calculables) +
                 [supy.calculables.other.fixedValue('Two',2) ]
                 )
    
    def listOfSampleDictionaries(self) :
        exampleDict = supy.samples.SampleHolder()
	nEvts = 5e4
	ntupleDir = '/home/zuranski/DisplacedJets/Analysis/ntuples/'
	exampleDict.add('data_r177782','["/home/zuranski/DisplacedJets/Analysis/ntuples/ntupled.root"]',lumi=0.009)
	exampleDict.add('qcd_120_170','["/home/zuranski/DisplacedJets/Analysis/ntuples/ntupleq120.root"]', xs=11.5e4)
	exampleDict.add('qcd_170_300','["/home/zuranski/DisplacedJets/Analysis/ntuples/ntupleq170.root"]', xs=2.43e4)
	exampleDict.add('qcd_300_470','["/home/zuranski/DisplacedJets/Analysis/ntuples/ntupleq300.root"]', xs=11.7e2)
        return [exampleDict]
    
    def listOfSamples(self,config) :
        return (supy.samples.specify(names = "data_r177782", color = r.kBlack, markerStyle = 20) +
                supy.samples.specify(names = "qcd_120_170", color = r.kBlue, markerStyle = 20) +
		supy.samples.specify(names = "qcd_170_300", color = r.kBlue, markerStyle = 20) +
		supy.samples.specify(names = "qcd_300_470", color = r.kBlue, markerStyle = 20) )
    
    def conclude(self,pars) :
        #make a pdf file with plots from the histograms created above
        org = self.organizer(pars)
	org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
        org.scale()
        supy.plotter( org,
                      pdfFileName = self.pdfFileName(org.tag),
                      samplesForRatios = ("data_r177782","qcd"),
                      sampleLabelsForRatios = ("data","qcd"),
		      pegMinimum=0.1,
		      doLog=True,
                      ).plotAll()
