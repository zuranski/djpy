import sys,os,pickle,math,ROOT as r
from multiprocessing import Pool
import random

def rnd(num,sig_figs):
	if num != 0:
		return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
	else:
		return 0

def limit(f):
	data=pickle.load(open(effDir+f))
	print data
	eff=data[dictionary[option][1]]
	factor=eval(f[:-4].split('_')[4])
	b,o=bkg[0],obs[0]
	if factor>0.3: b,o=bkg[1],obs[1]
	res={}
	keys = ['exp','1ms','2ms','1ps','2ps','obs']
	for key in keys: res[key]=None
	#eff=dict['eff']
	#if dict.has_key('bkg') : b=dict['bkg']
	#if dict.has_key('obs') : o=dict['obs']
	print b,o,f

	if eff[0]>0:
		os.mkdir(f)
		os.chdir(f)

		limit = r.LimitResult()
		#r.roostats_cl95(lumi[0],lumi[1],rnd(eff[0],3),rnd(eff[1],2),rnd(b[0],3),rnd(b[1],2),int(o[0]),False,1,'cls','',random.randint(0,1e7),limit)

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


option=sys.argv[2]
dictionary={'e':('eff',1),'ea':('effacc',2)}

effDir=sys.argv[1]+'/efficiencies/'
limDir=sys.argv[1]+'/limits'+option+'/'

files=[f for f in os.listdir(effDir) if '.pkl' in f and '.swp' not in f]
print files

# roostats
r.gROOT.LoadMacro('roostats_cl95.C+')

# input out of nowhere
lumi=(18600,0.044*18600)
bkg=[(1.60,0.58),(1.14,0.54)]
obs=[(2,0.),(1,0)]

p=Pool(1)
p.map(limit,files)
