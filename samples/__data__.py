from supy.samples import SampleHolder
from supy.sites import pnfs

data = SampleHolder()

loc = 'DJTuple44x_PROD/'
data.add('dataB','%s/%s/%s")'%(pnfs,loc,"DataRun2011B") ,lumi=0.5725) #/pb
data.add('dataA','%s/%s/%s")'%(pnfs,loc,"DataRun2011A") ,lumi=0.5725) #/pb
