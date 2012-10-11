import pickle,ROOT as r
from supy import analysisStep

class collector(analysisStep) :
    def __init__(self, vars, indices='') :
        self.vars = vars
        self.indices = indices
        self.collection = set([])
    def uponAcceptance(self, eventVars) :
        self.collection.add(tuple([tuple([eventVars[var][idx] for var in self.vars]) for idx in eventVars[self.indices]]))
    def varsToPickle(self) :
        return ["collection"]

    def outputSuffix(self) : return ".pkl"

    def mergeFunc(self, products) :
        s = set([]).union(*products["collection"])
        pickle.dump(s,open(self.outputFileName,"w"))
