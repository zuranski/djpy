from supy.samples import SampleHolder
from supy.sites import pnfs

sigmc = SampleHolder()

loc = 'DJTuple44x_DEV/'
sigmc.add('H_400_X_150','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_150_Ctau_400/") ,xs=500) #/pb
sigmc.add('H_1000_X_20','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_20_Ctau_15/") ,xs=500) #/pb
