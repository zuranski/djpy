import sys,os,pickle,math,ROOT as r
from multiprocessing import Pool

def expected(dict):
	res={}
	keys = ['explim','m1s','m2s','p1s','p2s']
	for key in keys: res[key]=None
	if dict['eff']>0:
		explimit = r.GetExpectedLimit(l,le,dict['eff'],0.2*dict['eff'],b,be,2,"bayesian")
		res['explim'] = explimit.GetExpectedLimit()
		res['m1s'] = explimit.GetOneSigmaLowRange()
		res['m2s'] = explimit.GetTwoSigmaLowRange()
		res['p1s'] = explimit.GetOneSigmaHighRange()
		res['p2s'] = explimit.GetTwoSigmaHighRange()
	pickle.dump(res,open('tmp/'+str(dict['idx'])+'.pkl','w'))

os.system('mkdir tmp')
# input total efficiencies
effDict = pickle.load(open('../data/eff.pkl','r'))
for i,dict in enumerate(effDict): dict['idx']=i

# roostats
r.gROOT.LoadMacro('roostats_cl95.C+')

l=11317
le=0.044*11317
b=2
be=0.5

p = Pool(9)
p.map(expected,effDict)

for dict in effDict:
	expected = pickle.load(open('tmp/'+str(dict['idx'])+'.pkl','r'))
	for key in expected: dict[key]=expected[key]

os.system('rm -r tmp')
pickle.dump(effDict,open('../data/limits.pkl','w'))
