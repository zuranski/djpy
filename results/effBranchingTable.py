import os,sys,pickle
from utils.other import stringValue

dir1=sys.argv[1]+'/efficiencies'
dir2=sys.argv[2]+'/efficiencies'
dir3=sys.argv[3]+'/efficiencies'

# optione a, e, ea
option=sys.argv[4]
dict={'e':('\epsilon',1),'a':('Acceptance',0),'ea':('\epsilon_{InAcceptance}',2)}

map={'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
     'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,
    }

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

print "\\begin{table}[!h] \n\centering \n\\begin{tabular}{llll} \n\hline"
print "$H^{0}$ [GeV] & $X$ [GeV] & c$\\tau$ [cm] & $"+dict[option][0]+"$ [\%] \\\\"
H,X=0,0

for file1,file2,file3 in zip(files1,files2,files3):
	strings=file1[:-4].split('_')
	if H!=strings[1] or X!=strings[3]: print '\hline'
	H,X,factor=strings[1],strings[3],strings[4]
	if factor not in ['0.1','1.0','10.0'] : continue
	main_ctau=map['_'.join(strings[:4])]
	ctau=main_ctau*eval(factor)
	if int(ctau)==ctau: ctau=int(ctau)
	data1 = pickle.load(open(dir1+'/'+file1))[dict[option][1]]
	data2 = pickle.load(open(dir2+'/'+file2))[dict[option][1]]
	data3 = pickle.load(open(dir3+'/'+file3))[dict[option][1]]
	data=[data1,data2,data3]
	string = " & ".join(stringValue(100*a[0],100*a[1],1) for a in data)
	print "%s & %s & %s & %s \\\\"%(H,X,ctau,string)

print "\hline"
print "\end{tabular} \n\end{table}" 
