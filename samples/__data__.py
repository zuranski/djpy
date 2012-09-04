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
loc='/tigress-hsm/zuranski/work/cms/data/DJTuple44x_DEV/'
data.add('dataA','%s'%(fileListFromDisk(loc+"/DataRun2011A")),lumi=0.5725) #/pb
data.add('dataB','%s'%(fileListFromDisk(loc+"/DataRun2011B")),lumi=0.5725) #/pb
