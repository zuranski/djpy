import os,sys,pickle,math
from utils.other import rnd,weightedAvg

dir1=sys.argv[1]+'/efficiencies'
dir2=sys.argv[2]+'/efficiencies'

option=sys.argv[3]
dict={'e':('\epsilon',1),'a':('Acceptance',0),'ea':('\epsilon_{InAcceptance}',2)}

files1=sorted(os.listdir(dir1),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

files2=sorted(os.listdir(dir2),key=lambda file: (eval(file[:-4].split('_')[1]),
                           eval(file[:-4].split('_')[3]),
                           eval(file[:-4].split('_')[4]))
            )

x,w=[],[]
H,X=0,0

for file1,file2 in zip(files1,files2):
	data1,data2=pickle.load(open(dir1+'/'+file1)),pickle.load(open(dir2+'/'+file2))
	strings=file1[:-4].split('_')
	if ((H!=strings[1] or X!=strings[3]) and H!=0):
		avg,err=weightedAvg(x,w)
		print round(avg,5),round(err,5)
		x,w=[],[]	
	H,X,factor = strings[1],strings[3],eval(strings[4])
	if factor != 0.1 and factor!=1 and factor!=10 : continue
	e1,e2 = data1[dict[option][1]],data2[dict[option][1]]
	if e1[0]==e2[0]==0 : continue
	diff = 100* 2*(e1[0]-e2[0])/(e1[0]+e2[0])
	n1=pow(e1[0]/e1[1],2)
	n2=pow(e2[0]/e2[1],2)
	if n1-n2==0: continue
	diffe = diff*1./math.sqrt(abs(n1-n2))
	#diffe=1
	#diffe = 100* 4/pow(e1[0]+e2[0],2)*math.sqrt(pow(e2[0]*e1[1],2)+pow(e1[0]*e2[1],2))
	x.append(diff)
	w.append(diffe)
	e1=tuple([str(rnd(a,2)) for a in e1])
	e2=tuple([str(rnd(a,2)) for a in e2])
	print file1,e1,e2,rnd(diff,2),rnd(diffe,2)

avg,err = weightedAvg(x,w)
print round(avg,5),round(err,5)
