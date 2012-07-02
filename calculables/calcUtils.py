
def DeltaPhi(obj1,obj2):
	dphi = obj1.phi - obj2.phi
	import math
        while (dphi > math.pi ): dphi -= 2*math.pi
        while (dphi <= -math.pi ): dphi += 2*math.pi
	return dphi

def DeltaR(obj1,obj2):

        import math
        deta = obj1.eta - obj2.eta
	dphi = DeltaPhi(obj1,obj2)
        return math.sqrt(deta*deta + dphi*dphi)

def Theta(eta):
	import math
	return 2*math.atan(math.exp(-eta))
