import ROOT as r
import math

def getCounts(histo):
	keys = ['A','B','C','D','E','F','G','H']
	dict = {}
	for i in range(len(keys)):
		dict[keys[i]] = (histo.GetBinContent(i+1),histo.GetBinError(i+1))

	results = []
	results.append(dict['H'])
	combinations = [('F','G','B'),('E','G','C'),('D','G','A'),('B','E','A'),('C','F','A'),('E','F','D')]
	for comb in combinations:
		b,c,a = dict[comb[0]],dict[comb[1]],dict[comb[2]]
		results.append(estimate(b,c,a))
	return results

def estimate(b,c,a):
	if not b[0]>0 or not c[0]>0 or not a[0]>0 : return (0,0)
	est = b[0]*c[0]/float(a[0])
	err = est*math.sqrt(pow(a[1]/float(a[0]),2)+
						pow(b[1]/float(b[0]),2)+
						pow(c[1]/float(c[0]),2))
	return (est,err)

def string(obj): return '('+','.join(str(a) for a in obj)+')' if type(obj)==tuple else str(obj)

def listdiff(a,b): return [i for i,j in zip(a,b) if i!=j]

def plotABCDscan(analysis,org,plotter,n,blind=True):
	plotter.pdfFileName = plotter.pdfFileName.replace(analysis.name+'.pdf','Scans_'+analysis.name+'.pdf')
	plotter.canvas.Clear()
	plotter.printCanvas("[")
	text1 = plotter.printTimeStamp()
	plotter.flushPage()
	r.gPad.SetLogy()
	r.gPad.SetTicky(0)
	if not plotter.anMode : r.gPad.SetRightMargin(0.2)
	# get all the counts
	counts = [[0]*len(analysis.scan) for sample in org.samples]
	for step in org.steps : 
		for plotName in sorted(step.keys()) :
			if 'ABCDEFGHcounts' not in plotName: continue
			i = eval(plotName[:plotName.find('ABCDEFGH')])
			for j in range(len(org.samples)): counts[j][i] = getCounts(step[plotName][j])

	# pick points to scan
	scans=[
               (analysis.scanPrompt[0],analysis.scanPrompt[0],None),
               (analysis.scanPrompt[1],analysis.scanPrompt[1],None),
               (analysis.scanPrompt[2],analysis.scanPrompt[2],None),
               (analysis.scanPrompt[3],analysis.scanPrompt[3],None),
		  ]

	# constant names
	cutNames = ['(NPrompt1,PromptFrac1)','(NPrompt2,PromptFrac2)','DiscVtx']
	histNames = ['observed','FG/B','EG/C','DG/A','BE/A','CF/A','EF/D']

	# plot scans
	for scan in scans:

		title = ' '.join(name+'='+string(value) if value else '' for name,value in zip(cutNames,scan))
		xtitle = cutNames[scan.index(None)]+ ' cut'
		ytitle = 'Number of Events / ' +str(org.lumi)+'pb^{-1}'

		indices = [i for i,cuts in enumerate(analysis.scan) if len(listdiff(cuts,scan))<=1]
		labels = [string(cuts[scan.index(None)]) for i,cuts in enumerate(analysis.scan) if i in indices]
		# first make a plot of signal efficiency
		sigSamples = [sample for sample in org.samples if 'H' in sample['name']]		
 
	 	sigeff = [r.TH1F('sigeff',sample['name'],len(indices),0,1) for sample in sigSamples]
		for j,sample in enumerate(sigSamples):
			i = org.indexOfSampleWithName(sample['name'])
			norm = sample['xs']*org.lumi
			for k,idx in enumerate(indices):
				sigeff[j].SetBinContent(k+1,100*counts[i][idx][0][0]/float(2*norm))
				sigeff[j].SetBinError(k+1,100*counts[i][idx][0][1]/float(norm))
				sigeff[j].GetXaxis().SetBinLabel(k+1,labels[k])

		for j,sample in enumerate(org.samples):
			if 'H' in sample['name'] : continue
			histos = [r.TH1F(name,sample['name']+' '+title,len(indices),0,1) for name in histNames]
			legend = r.TLegend(0.85, 0.60, 0.99, 0.10)
			for i in reversed(range(n)):
				if blind and 'Data' in sample['name'] and i==0: continue
				for k,idx in enumerate(indices):
					histos[i].SetBinContent(k+1,counts[j][idx][i][0])
					histos[i].SetBinError(k+1,counts[j][idx][i][1])
					histos[i].GetXaxis().SetBinLabel(k+1,labels[k])
				histos[i].GetXaxis().SetTitle(xtitle)
				histos[i].GetYaxis().SetTitle(ytitle)
				histos[i].SetStats(False)
				histos[i].SetMarkerStyle(25 if i!=0 else 8)
				histos[i].SetMarkerColor(i+1)
				histos[i].SetFillColor(0)
				histos[i].SetLabelSize(0.06)
				legend.AddEntry(histos[i],histNames[i])
				option='EX0' if i==(n-1) else 'EX0same'
				histos[i].Draw(option)
			histos_tmp=tuple([histos[i] for i in range(n)])
			plotter.setRanges(histos_tmp,*plotter.getExtremes(1,histos_tmp,[False]*n))
			
			pad = r.TPad("pad2","",0,0,1,1)
			pad.SetRightMargin(0.2)
			pad.SetFillStyle(4000)
			pad.SetFrameFillStyle(0)
			pad.SetLogy(0)
			pad.Draw()
			pad.cd()
			for i,sample in enumerate(sigSamples):
				option='histY+' + ('same' if i>0 else '')
				sigeff[i].SetLineWidth(1)
				sigeff[i].SetStats(False)
				sigeff[i].SetLabelSize(0.06)
				sigeff[i].SetLineColor(i+2)
				sigeff[i].SetLineStyle(2)
				sigeff[i].GetYaxis().SetRangeUser(0,45)
				sigeff[i].GetYaxis().SetTitle('efficiency [%]')
				sigeff[i].Draw(option)
				legend.AddEntry(sigeff[i],sample['name'].split('.')[0])

			legend.Draw("same")
			#histos_tmp=tuple([sigeff[i] for i in range(len(sigSamples))])
			#plotter.setRanges(histos_tmp,*plotter.getExtremes(1,histos_tmp,[False]*len(sigSamples)))
			plotter.printCanvas()
			plotter.canvas.Clear()

	plotter.printCanvas("]")
	print plotter.pdfFileName, "has been written."
