import os,sys,pickle
from utils.other import stringValue

dir=sys.argv[1]+'/efficiencies'

map={'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
     'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,
	 'SQ_1500_CHI_494':18.1,'SQ_1000_CHI_148':5.85,'SQ_350_CHI_148':18.8,'SQ_120_CHI_48':15.5
    }

files=sorted(os.listdir(dir),key=lambda file: (eval(file[:-4].split('_')[1]),
					       eval(file[:-4].split('_')[3]),
					       eval(file[:-4].split('_')[4]))
            )

print "\\begin{table}[!h] \n\centering \n\\begin{tabular}{llll} \n\hline"
#print "$H^{0}$ [GeV] & $X$ [GeV] & c$\\tau$ [cm] & Acceptance [\%] & $\epsilon$ [\%] & $\epsilon_{InAcceptance}$ [\%] \\\\"
print "$H^{0}$ [GeV] & $X$ [GeV] & c$\\tau$ [cm] & $\epsilon$ [\%]\\\\"
H,X=0,0

for file in files:
	strings=file[:-4].split('_')
	if H!=strings[1] or X!=strings[3]: print '\hline'
	H,X,factor=strings[1],strings[3],strings[4]
	if factor not in ['0.1','1.0','10.0'] : continue
	main_ctau=map['_'.join(strings[:4])]
	ctau=main_ctau*eval(factor)
	if int(ctau)==ctau: ctau=int(ctau)
	data = pickle.load(open(dir+'/'+file))
	#string = " & ".join(stringValue(100*a[0],100*a[1],1) for a in data)
	string = stringValue(100*data[0][0],100*data[0][1],1)
	print "%s & %s & %s & %s \\\\"%(H,X,ctau,string)

print "\hline"
print "\end{tabular} \n\end{table}" 
