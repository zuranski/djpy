import os,sys,pickle

effDict = pickle.load(open('../data/eff.pkl','r'))

print "\\begin{table}[!h] \n\centering \n\\begin{tabular}{llll} \n\hline"
print "$H^{0}$ [GeV] & $X$ [GeV] & c$\\tau$ [cm] & $\epsilon$ [\%] \\\\"
print "\hline"

for i,dict in enumerate(effDict):
	print "%s & %s & %s & %s$\pm%s$ \\\\"%(dict['H'],dict['X'],dict['ctau'],round(100*dict['eff'],1),round(100*dict['effErr'],1))
	if i!=(len(effDict)-1):
		if (effDict[i+1]['X']!=dict['X'] or effDict[i+1]['H']!=dict['H']): print "\hline"

print "\hline"
print "\end{tabular} \n\end{table}" 
