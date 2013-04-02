import sys,os,pickle,math,ROOT as r
from multiprocessing import Pool
import random

def rnd(num,sig_figs):
	if num != 0:
		return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
	else:
		return 0

def limit(effErr):
	f=str(eff)+'_'+str(effErr)	
	res={}
	keys = ['exp','1ms','2ms','1ps','2ps','obs']
	for key in keys: res[key]=None
	print b,o

	if eff>0:
		os.mkdir(f)
		os.chdir(f)

		limit = r.LimitResult()
		r.roostats_cl95(lumi[0],lumi[1],eff,eff*effErr/100.,rnd(b[0],3),rnd(b[1],2),int(o[0]),False,0,'cls','',random.randint(0,1e7),limit)
		#limit=r.roostats_clm(lumi[0],lumi[1],rnd(eff,3),rnd(effErr*eff/100.,2),rnd(b[0],3),rnd(b[1],2),int(o[0]),False,1,'cls','',random.randint(0,1e7),limit)

		res['obs'] = limit.GetObservedLimit()
		res['exp'] = limit.GetExpectedLimit()
		res['1ms'] = limit.GetOneSigmaLowRange()
		res['2ms'] = limit.GetTwoSigmaLowRange()
		res['1ps'] = limit.GetOneSigmaHighRange()
		res['2ps'] = limit.GetTwoSigmaHighRange()
		os.system('rm ws.root')
		os.chdir('../')
		os.rmdir(f)
		pickle.dump(res,open(limDir+f,'w'))


limDir=sys.argv[1]+'/'

eff=eval(sys.argv[2])
effErrs=[0,10,20,30,40,50,60,70,80,90]
print eff

# roostats
r.gROOT.LoadMacro('roostats_cl95.C+')

# input out of nowhere
lumi=(16740,0.044*16740)
bkg=[(1.45,0.45),(1.08,0.51)]
b=bkg[0]
obs=[(2,0.),(1,0)]
o=obs[0]

p=Pool(15)
p.map(limit,effErrs)
