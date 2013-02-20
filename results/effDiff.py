import os,sys,pickle,math

def rnd(num,sig_figs):
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0

def weightedAvg(x,w):
	err2 = 1./sum([1/pow(wi,2) for wi in w])
	avg = sum(xi/pow(wi,2) for xi,wi in zip(x,w))*err2
	return avg,math.sqrt(err2)

dir1=sys.argv[1]+'/efficiencies'
dir2=sys.argv[2]+'/efficiencies'

files1=sorted(os.listdir(dir1),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

files2=sorted(os.listdir(dir2),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

x,w=[],[]

for file1,file2 in zip(files1,files2):
	dict1,dict2=pickle.load(open(dir1+'/'+file1)),pickle.load(open(dir2+'/'+file2))
	e1,e2 = dict1['eff'],dict2['eff']
	if e1[0]==e2[0]==0 : continue
	diff = 100* 2*(e1[0]-e2[0])/(e1[0]+e2[0])
	diffe = 100* 4/pow(e1[0]+e2[0],2)*math.sqrt(pow(e2[0]*e1[1],2)+pow(e1[0]*e2[1],2))
	x.append(diff)
	w.append(diffe)
	e1=tuple([rnd(a,2) for a in e1])
	e2=tuple([rnd(a,2) for a in e2])
	print file1,e1,e2,rnd(diff,2),rnd(diffe,2)

avg,err = weightedAvg(x,w)
print round(avg,5),round(err,5)
