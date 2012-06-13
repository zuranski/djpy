from supy.samples import SampleHolder
from supy.sites import pnfs

data = SampleHolder()

loc = 'DJTuple44x_DEV/'
data.add('data','%s/%s/%s")'%(pnfs,loc,"DataRun2011B") ,lumi=0.5725) #/pb
