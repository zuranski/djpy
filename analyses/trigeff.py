
import supy,samples,calculables,steps,ROOT as r
from calculables.utils import abcdCmp

class trigeff(supy.analysis) :
    
	qcd_bins = [str(q) for q in [80,120,170,300,470,600,800]]
	qcd_names = ["qcd_%s_%s" %(low,high) for low,high in zip(qcd_bins[:-1],qcd_bins[1:])]

	ToCalculate = ['jetPromptness']

	IniCuts=[
        {'name':'jet'},
        {'name':'jetPt','min':80},
        {'name':'jetPromptness','max':0.35},
    ]
	Cuts=[
        {'name':'jetTrigPrompt','val':True},
    ]
	
	def dijetSteps1(self):
		mysteps = []
		for cut in self.IniCuts:
			mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=2))
			mysteps.append(steps.plots.trigvars(indices=cut['name']+'Indices',njets=1))
		#for cut in self.Cuts: 
		#	mysteps.append(supy.steps.filters.multiplicity(cut['name']+'Indices',min=1))
		#	mysteps.append(steps.plots.trigvars(indices=cut['name']+'Indices',njets=1))
		return ([supy.steps.filters.label('dijet multiplicity filters')]+mysteps)

	def calcsIndices(self):
		calcs = []
		cuts = self.IniCuts+self.Cuts
		for cutPrev,cutNext in zip(cuts[:-1],cuts[1:]):
			calcs.append(calculables.Indices.Indices(indices=cutPrev['name']+'Indices',cut=cutNext))
		return calcs

	def calcsVars(self):
		calcs = []
		for calc in self.ToCalculate:
			calcs.append(getattr(calculables.Vars,calc)('jetIndices'))
		return calcs

	def listOfSteps(self,config) :
		return ([
			supy.steps.printer.progressPrinter(),

			### filters
			supy.steps.filters.label('data cleanup'),
			supy.steps.filters.value('isPrimaryVertex',min=1),
			supy.steps.filters.value('isPhysDeclared',min=1).onlyData(),
			supy.steps.filters.value('isBeamScraping',max=0),
			supy.steps.filters.value('passBeamHaloFilterTight',min=1),
			supy.steps.filters.value('passHBHENoiseFilter',min=1)]

			### pile-up reweighting
			+[supy.calculables.other.Target("pileupPUInteractionsBX0",thisSample=config['baseSample'],
				target=("data/ABcontrol_observed.root","pileup"),
				groups=[('qcd',[]),('Huds',[]),('Hb',[])]).onlySim()] 

			### trigger
			+[supy.steps.filters.label("hlt trigger"),
			steps.trigger.hltFilterWildcard("HLT_HT250_v")]
			#steps.trigger.hltFilterWildcardUnprescaled("HLT_HT250_DoubleDisplacedJet60")]
			
			#+[supy.steps.filters.value('PfHt',min=250)]

			### plots
			+[steps.event.general()]
			+self.dijetSteps1()
			+[steps.trigger.hltFilterWildcard("HLT_HT250_DoubleDisplacedJet60_v")]
			)

	def listOfCalculables(self,config) :
		return ( supy.calculables.zeroArgs(supy.calculables) +
			supy.calculables.zeroArgs(calculables) 
			+self.calcsIndices()
			+self.calcsVars()
                 )
    
	def listOfSampleDictionaries(self) :
		return [samples.qcd,samples.data,samples.sigmc]

	def listOfSamples(self,config) :
		nFiles = None # or None for all
		nEvents = None # or None for all

		qcd_samples = []
		for i in range(len(self.qcd_names)):
			qcd_samples+=(supy.samples.specify(names = self.qcd_names[i] ,nFilesMax = nFiles, nEventsMax = nEvents, color = i+3, weights=['pileupPUInteractionsBX0Target']))
		return (supy.samples.specify(names = "dataA", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=9.0456)
			#+ supy.samples.specify(names = "dataB", color = r.kBlack, markerStyle = 20, nFilesMax = nFiles, nEventsMax = nEvents, overrideLumi=1.913)
			+ qcd_samples 
		) 

	def conclude(self,pars) :
		#make a pdf file with plots from the histograms created above
		org = self.organizer(pars)
		org.mergeSamples(targetSpec = {"name":"qcd", "color":r.kBlue}, allWithPrefix = "qcd")
		org.mergeSamples(targetSpec = {"name":"data", "color":r.kBlack, "markerStyle":20}, allWithPrefix = "data")
		org.scale(lumiToUseInAbsenceOfData=11)
		plotter = supy.plotter( org,
			#dependence2D=True,
			pdfFileName = self.pdfFileName(org.tag),
			samplesForRatios = ("data","qcd"),
			sampleLabelsForRatios = ("data","qcd"),
			doLog=True,
			blackList = ["lumiHisto","xsHisto","nJobsHisto"],
		)
		plotter.plotAll()
		#self.makeEfficiencyPlots(org,"jet","jetTrigPrompt", plotter, "1")
		#self.makeEfficiencyPlots(org,"jetPt","jetTrigPrompt", plotter, "2")

	def makeEfficiencyPlots(self, org, denomName, numName, plotter, instance):
		plotter.pdfFileName = plotter.pdfFileName+instance
		plotter.doLog = False
		plotter.printCanvas("[")
		text1 = plotter.printTimeStamp()
		text2 = plotter.printNEventsIn()
		plotter.flushPage()

		hists_denom = []
		hists_num = []
		for step in org.steps:
			for plotName in sorted(step.keys()):
				if denomName in plotName: hists_denom.append(step[plotName])
				if numName in plotName: hists_num.append(step[plotName])

		for num_list,denom_list in zip(hists_num,hists_denom):
			print num_list, denom_list
			ratio_tpl = tuple([supy.utils.ratioHistogram(num,denom) for num,denom in zip(num_list,denom_list)])
			for ratio in ratio_tpl:
				ratio.GetYaxis().SetTitle("efficiency")
				ratio.GetXaxis().SetTitle(num.GetXaxis().GetTitle())
			plotter.onePlotFunction(ratio_tpl)
		plotter.printCanvas("]")
		print plotter.pdfFileName, 'has been written'

