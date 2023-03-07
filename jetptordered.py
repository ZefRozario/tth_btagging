import ROOT
import sys

inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/ttH_PP8_mc16a.root')
tree = inFile.Get("nominal_Loose")


runs=['a','d','e']
runslumi=[36207.66,44307.4,58450.1]
for i in range(0,len(runs)):
    inFile = ROOT.TFile.Open('/nfs/atlas/ttH/ttHbb_Legacy/boosted/ttH_PP8_mc16'+str(runs[i])+'.root')
    tree = inFile.Get("nominal_Loose")


    for ievt in range(0,tree.GetEntries()):	
        tree.GetEntry(ievt)
        weight=tree.weight_normalise * runslumi[i] * tree.weight_mc * tree.weight_pileup * tree.weight_leptonSF * tree.weight_jvt * tree.weight_bTagSF_DL1r_Continuous
        passjetsel=False
        DNNHiggs=False
        if tree.passedOfflineBoostedSelection == 0 :
            pass
        for j in range(0,tree.jet_pt.size()):
            if j>0:
                #print(j)
                continue
            if abs(tree.jet_pt[j]) - abs(tree.jet_pt[j-1]) <0:
                print('yikes, event '+str(ievt)+' is not pt ordered')
                print(sorted(tree.jet_pt,reverse=True))
                sys.exit()
                
                
                break


print('we all good, all jets in the events are pt ordered.')
