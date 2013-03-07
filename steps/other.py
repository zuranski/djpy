import pickle,ROOT as r
from supy import analysisStep

class collector(analysisStep) :
    def __init__(self, vars, indices='') :
        self.indices = indices
        self.collection = set([])
        self.iterVars,self.uniqueVars=[],[]
        [self.iterVars.append(var) if 'jet' in var else self.uniqueVars.append(var) for var in vars]
        #for var in vars: 
        #    if 'jet' in var:
        #        self.iterVars.append(var)
        #    else:
        #        self.uniqueVars.append(var)
        
    def uponAcceptance(self, e) :
        iterTuple=tuple([tuple([e[var][idx] for var in self.iterVars]) for idx in e[self.indices]])
        uniqueTuple=tuple([e[var] for var in self.uniqueVars] if len(e[self.indices])>0 else [])
        self.collection.add(iterTuple+uniqueTuple)

        #self.collection.add(tuple([tuple([e[var][idx] for var in self.vars]) for idx in e[self.indices]]+[tuple(e[var] for var in self.uniqueVars)]))
    def varsToPickle(self) :
        return ["collection"]

    def outputSuffix(self) : return self.indices+".pkl"

    def mergeFunc(self, products) :
        s = set([]).union(*products["collection"])
        pickle.dump(s,open(self.outputFileName,"w"))
        print sorted(list(s))

class genParticleMultiplicity(analysisStep):

    def __init__(self,pdgId,min=1):
        for item in ['pdgId','min']: setattr(self,item,eval(item))

    def select (self,e):
        nObjects = 0
        for pdgId in e["XpdgId"]:
            if pdgId == self.pdgId : nObjects += 1
        if nObjects >= self.min: return True
        return False
