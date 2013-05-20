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
    def __init__(self,pdgIds=[],collection='',min=None,max=None):
        for item in ['pdgIds','collection','min','max']: setattr(self,item,eval(item))
        pdgIds_str=",".join(str(a) for a in pdgIds)
        self.moreName="%d <= %s"%(min,pdgIds_str) + (" <= %d" % max if max!=None else "")

    def select (self,e):
        if e['realData'] or len(e['XpdgId']) == 0: return True
        nObjects = 0
        X = [a for a in e[self.collection]]
        for pdgId in self.pdgIds: nObjects+=X.count(pdgId)
        if nObjects >= self.min and nObjects <= self.max: 
             return True
        return False
