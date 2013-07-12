import math

def stringValue(val,err,sig_figs):
    if val!=0:
        place = -int(math.floor(math.log10(abs(err))) - (sig_figs-1))
        val,err=round(val,place),round(err,place)
    return "$"+str(val)+" \pm "+ str(err)+"$"

def roundSig(num,sig_figs):
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0

def weightedAvg(x,w):
    err2 = 1./sum([1/pow(wi,2) for wi in w])
    avg = sum(xi/pow(wi,2) for xi,wi in zip(x,w))*err2
    return avg,math.sqrt(err2)
