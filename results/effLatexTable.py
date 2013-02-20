import os,sys,pickle,math

def rnd(num,sig_figs):
    if num != 0:
        return round(num, -int(math.floor(math.log10(abs(num))) - (sig_figs - 1)))
    else:
        return 0

dir=sys.argv[1]+'/efficiencies'

map={'H_1000_X_350':35,'H_1000_X_150':10,'H_1000_X_50':4,
     'H_400_X_150':40,'H_400_X_50':8,'H_200_X_50':20,
    }

files=sorted(os.listdir(dir),key=lambda file: (eval(file[:-4].split('_')[1]),
					       eval(file[:-4].split('_')[3]),
					       eval(file[:-4].split('_')[4]))
            )

print "\\begin{table}[!h] \n\centering \n\\begin{tabular}{llll} \n\hline"
print "$H^{0}$ [GeV] & $X$ [GeV] & c$\\tau$ [cm] & $\epsilon$ [\%] \\\\"
H,X=0,0

for i,file in enumerate(files):
	strings=file[:-4].split('_')
	if H!=strings[1] or X!=strings[3]: print '\hline'
	H,X,factor=strings[1],strings[3],strings[4]
	main_ctau=map['_'.join(strings[:4])]
	ctau=rnd(main_ctau*eval(factor),3)
	if int(ctau)==ctau: ctau=int(ctau)
	dict = pickle.load(open(dir+'/'+file))
	print "%s & %s & %s & %s$\pm%s$ \\\\"%(H,X,ctau,rnd(100*dict['eff'][0],2),rnd(100*dict['eff'][1],2))#,dict['idx']

print "\hline"
print "\end{tabular} \n\end{table}" 
