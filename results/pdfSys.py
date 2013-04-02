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
dir3=sys.argv[3]+'/efficiencies'

files1=sorted(os.listdir(dir1),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

files2=sorted(os.listdir(dir2),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )
files3=sorted(os.listdir(dir3),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

x,w=[],[]

for file1,file2,file3 in zip(files1,files2,files3):
	dict1,dict2,dict3=pickle.load(open(dir1+'/'+file1)),pickle.load(open(dir2+'/'+file2)),pickle.load(open(dir3+'/'+file3))
	factor = eval(file1[:-4].split('_')[4])
	if factor != 0.1 and factor!=1 and factor!=10 : continue
	e1,e2,e3 = dict1['eff'],dict2['eff'],dict3['eff']
	if e1[0]==e2[0]==0 : continue
	#x = 0.5*(max(e1[0]+e1[1],e2[0]+e2[1],e3[0]+e3[1])+min(e1[0]-e1[1],e2[0]-e2[1],e3[0]-e3[1]))
	#xe = 0.5*(max(e1[0]+e1[1],e2[0]+e2[1],e3[0]+e3[1])-min(e1[0]-e1[1],e2[0]-e2[1],e3[0]-e3[1]))
	x = 50*(max(e1[0],e2[0],e3[0])+min(e1[0],e2[0],e3[0]))
	xe = 50*(max(e1[0],e2[0],e3[0])-min(e1[0],e2[0],e3[0]))
	diffe=1
	e1=tuple([str(rnd(a,2)) for a in e1])
	e2=tuple([str(rnd(a,2)) for a in e2])
	print file1,e1,e2,rnd(x,2),rnd(xe,2),rnd(100*xe/x,2)

