from supy.samples import SampleHolder
from supy.sites import pnfs
from supy.utils.io import fileListFromDisk

sigmc = SampleHolder()

#FNAL
'''
loc = 'DJTuple44x_PROD/'
# u-d-s quark samples
sigmc.add('H_1000_X_350','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_350_Ctau_350/") ,xs=500) #/pb
sigmc.add('H_1000_X_150','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_150_Ctau_100/") ,xs=500) #/pb
sigmc.add('H_1000_X_50','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_50_Ctau_40/") ,xs=500) #/pb
sigmc.add('H_400_X_150','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_150_Ctau_400/") ,xs=500) #/pb
sigmc.add('H_400_X_50','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_50_Ctau_80/") ,xs=500) #/pb
sigmc.add('H_200_X_50','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_50_Ctau_200/") ,xs=500) #/pb

# b quark samples
sigmc.add('H_1000_X_350b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_350_Ctau_350b/") ,xs=500) #/pb
sigmc.add('H_1000_X_150b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_150_Ctau_100b/") ,xs=500) #/pb
sigmc.add('H_1000_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_1000_MX_50_Ctau_40b/") ,xs=500) #/pb
sigmc.add('H_400_X_150b','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_150_Ctau_400b/") ,xs=500) #/pb
sigmc.add('H_400_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_400_MX_50_Ctau_80b/") ,xs=500) #/pb
sigmc.add('H_200_X_50b','%s/%s/%s")'%(pnfs,loc,"MH_200_MX_50_Ctau_200b/") ,xs=500) #/pb
'''

# PU
loc='/tigress-hsm/zuranski/work/cms/data/DJTuple44x_DEV/'
# u-d-s quark samples
sigmc.add('Huds_1000_X_350','%s'%(fileListFromDisk(loc+"MH_1000_MX_350_Ctau_350/")) ,xs=500) #/pb
sigmc.add('Huds_1000_X_150','%s'%(fileListFromDisk(loc+"MH_1000_MX_150_Ctau_100/")) ,xs=500) #/pb
sigmc.add('Huds_1000_X_50','%s'%(fileListFromDisk(loc+"MH_1000_MX_50_Ctau_40/")) ,xs=500) #/pb
sigmc.add('Huds_400_X_150','%s'%(fileListFromDisk(loc+"MH_400_MX_150_Ctau_400/")) ,xs=500) #/pb
sigmc.add('Huds_400_X_50','%s'%(fileListFromDisk(loc+"MH_400_MX_50_Ctau_80/")) ,xs=500) #/pb
sigmc.add('Huds_200_X_50','%s'%(fileListFromDisk(loc+"MH_200_MX_50_Ctau_200/")) ,xs=500) #/pb

# b quark samples
sigmc.add('Hb_1000_X_350','%s'%(fileListFromDisk(loc+"MH_1000_MX_350_Ctau_350b/")) ,xs=500) #/pb
sigmc.add('Hb_1000_X_150','%s'%(fileListFromDisk(loc+"MH_1000_MX_150_Ctau_100b/")) ,xs=500) #/pb
sigmc.add('Hb_1000_X_50','%s'%(fileListFromDisk(loc+"MH_1000_MX_50_Ctau_40b/")) ,xs=500) #/pb
sigmc.add('Hb_400_X_150','%s'%(fileListFromDisk(loc+"MH_400_MX_150_Ctau_400b/")) ,xs=500) #/pb
sigmc.add('Hb_400_X_50','%s'%(fileListFromDisk(loc+"MH_400_MX_50_Ctau_80b/")) ,xs=500) #/pb
sigmc.add('Hb_200_X_50','%s'%(fileListFromDisk(loc+"MH_200_MX_50_Ctau_200b/")) ,xs=500) #/pb
