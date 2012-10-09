import ROOT as r
from supy import analysisStep

class hltFilter(analysisStep) :

    def __init__(self,hltPathName):
        self.hltPathName = hltPathName

    def select (self,e) :
        return e["triggered"][self.hltPathName]
#####################################
class hltFilterWildcard(analysisStep) :

    def __init__(self,hltPathWildcard):
        self.hltPathWildcard = hltPathWildcard

    def select (self,e):
        for path in e["triggered"]:
            if self.hltPathWildcard in path.first and path.second: return True
        return False
#####################################
class hltFilterWildcardUnprescaled(analysisStep):

    def __init__(self,hltPathWildcard):
        self.hltPathWildcard = hltPathWildcard

    def select (self,e):
        for path,prescale in zip(e["triggered"],e["prescaled"]):
			if self.hltPathWildcard in path.first and path.second and prescale.second==1: return True
        return False
    
