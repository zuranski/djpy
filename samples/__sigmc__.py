from supy.samples import SampleHolder
from supy.sites import pnfs

sigmc = SampleHolder()

loc = 'DJTuple44x_PROD/'

# u-d-s quark samples
sigmc.add('H_1000_X_350','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_350_Ctau_350/") ,xs=500) #/pb
sigmc.add('H_1000_X_150','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_150_Ctau_100/") ,xs=500) #/pb
sigmc.add('H_1000_X_50','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_50_Ctau_40/") ,xs=500) #/pb
sigmc.add('H_1000_X_20','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_20_Ctau_15/") ,xs=500) #/pb
sigmc.add('H_400_X_150','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_150_Ctau_400/") ,xs=500) #/pb
sigmc.add('H_400_X_50','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_50_Ctau_80/") ,xs=500) #/pb
sigmc.add('H_400_X_20','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_20_Ctau_40/") ,xs=500) #/pb
sigmc.add('H_200_X_50','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_50_Ctau_200/") ,xs=500) #/pb
sigmc.add('H_200_X_20','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_20_Ctau_70/") ,xs=500) #/pb
sigmc.add('H_120_X_50','%s/%s/%s")'%(pnfs,loc,"MH_120_MX_50_Ctau_500/") ,xs=500) #/pb
sigmc.add('H_120_X_20','%s/%s/%s")'%(pnfs,loc,"MH_120_MX_20_Ctau_130/") ,xs=500) #/pb

# b quark samples
sigmc.add('H_1000_X_350b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_350_Ctau_350b/") ,xs=500) #/pb
sigmc.add('H_1000_X_150b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_150_Ctau_100b/") ,xs=500) #/pb
sigmc.add('H_1000_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_50_Ctau_40b/") ,xs=500) #/pb
sigmc.add('H_1000_X_20b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_20_Ctau_15b/") ,xs=500) #/pb
sigmc.add('H_400_X_150b','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_150_Ctau_400b/") ,xs=500) #/pb
sigmc.add('H_400_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_50_Ctau_80b/") ,xs=500) #/pb
sigmc.add('H_400_X_20b','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_20_Ctau_40b/") ,xs=500) #/pb
sigmc.add('H_200_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_50_Ctau_200b/") ,xs=500) #/pb
sigmc.add('H_200_X_20b','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_20_Ctau_70b/") ,xs=500) #/pb
sigmc.add('H_120_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_120_MX_50_Ctau_500b/") ,xs=500) #/pb
sigmc.add('H_120_X_20b','%s/%s/%s")'%(pnfs,loc,"MH_120_MX_20_Ctau_130b/") ,xs=500) #/pb
