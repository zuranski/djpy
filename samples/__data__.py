from supy.samples import SampleHolder
from supy.sites import pnfs
from supy.utils.io import fileListFromDisk

data = SampleHolder()

# FNAL
'''
loc = 'DJTuple44x_PROD/'
data.add('dataB','%s/%s/%s")'%(pnfs,loc,"DataRun2011B") ,lumi=0.5725) #/pb
data.add('dataA','%s/%s/%s")'%(pnfs,loc,"DataRun2011A") ,lumi=0.5725) #/pb
'''

#PU
loc='/tigress-hsm/zuranski/work/cms/data/DJTuple53x_DEV/'
data.add('dataB','%s'%(fileListFromDisk(loc+"/DataRun2012B")),lumi=0.5725) #/pb
data.add('dataC1','%s'%(fileListFromDisk(loc+"/DataRun2012C1")),lumi=0.5725) #/pb
data.add('dataC2','%s'%(fileListFromDisk(loc+"/DataRun2012C2")),lumi=0.5725) #/pb
data.add('dataD','%s'%(fileListFromDisk(loc+"/DataRun2012D")),lumi=0.5725) #/pb
