import math,os,sys,pickle,ROOT as r
from multiprocessing import Pool

def rnd(num,sig_figs):
	if num != 0:
		return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
	else:
		return 0

def limitScan(scan):
        name = scan[0]+'_'+str(scan[1])
        l_h=r.TH1F(name,'Expected Limit',len(scan[2]),-0.5,len(scan[2])-0.5)
        limits=[None for i in range(len(scan[2]))]
	points=[]
	os.mkdir('tmp')
	os.chdir('tmp')
        for i, (bkg,eff) in enumerate(zip(data['bkg'],scan[2])):
                if eff[0] < 1e-6 : continue
		points.append({'eff':eff,'bkg':bkg,'i':i})
	
	p=Pool(14)
	p.map(singleLimit,points)

	for file in os.listdir('.'):
		if '.pkl' not in file: continue
		limit=pickle.load(open(file))
		i=eval(file.split('.pkl')[0])
		limits[i]=limit
		l_h.SetBinContent(i+1,limit)
	# clean up
	os.system('rm *.pkl ws.root')
	os.chdir('../')
	os.rmdir('tmp')

	# draw plot
        c=r.TCanvas()
        l_h.Draw('hist')
        c.SaveAs('data/'+name+'.eps')

        # pick best point
        done_limits = [l for l in limits if l is not None]
        if len(done_limits)==0:return
        idx=limits.index(min(done_limits))
        print idx
        vars={}
        vars['eff']=scan[2][idx]
        vars['bkg']=data['bkg'][idx]
        vars['obs']=data['obs'][idx]
	vars['idx']=idx
        
        pickle.dump(vars,open('optimized/efficiencies/'+name+'.pkl','w'))
        print name, 'Done'
	

def singleLimit(point):
	eff=point['eff']
	bkg=point['bkg']
	print lumi,lumie,eff,bkg
	#lim = r.GetExpectedLimit(lumi,lumie,eff[0],eff[1],bkg[0],bkg[1],1,'cls')
	lim = r.GetClsLimit(lumi,lumie,rnd(eff[0],3),rnd(eff[1],2),rnd(bkg[0],3),rnd(bkg[1],2),int(bkg[0]))
	pickle.dump(lim.GetExpectedLimit(),open(str(point['i'])+'.pkl','w'))

r.gROOT.ProcessLine('.L roostats_cl95.C+')
data=pickle.load(open(sys.argv[1]))

lumi=16740
lumie=0.044*lumi

samples = [key for key in data.keys() if 'H' in key]
scans=[]
for sample in samples:
        for key in data[sample].keys():
                scans.append((sample,key,data[sample][key]))

print len(scans)

for limscan in scans: 
	if 'H_1000_X_50' in limscan[0]:continue
	limitScan(limscan)

