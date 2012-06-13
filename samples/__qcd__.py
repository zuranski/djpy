from supy.samples import SampleHolder
from supy.sites import pnfs

qcd = SampleHolder()

loc = 'DJTuple44x_DEV/'
qcd.add('qcd_80_120','%s/%s/%s")'%(pnfs,loc,"QCD_Pt_80to120") ,xs=7.843e5) #/pb
qcd.add('qcd_120_170','%s/%s/%s")'%(pnfs,loc,"QCD_Pt_120to170") ,xs=11.5e4) #/pb
qcd.add('qcd_170_300','%s/%s/%s")'%(pnfs,loc,"QCD_Pt_170to300") ,xs=2.43e4) #/pb
qcd.add('qcd_300_470','%s/%s/%s")'%(pnfs,loc,"QCD_Pt_300to470") ,xs=11.7e2) #/pb
qcd.add('qcd_470_600','%s/%s/%s")'%(pnfs,loc,"QCD_Pt_470to600") ,xs=70.2) #/pb
