import ROOT



jetpt= ROOT.TH1D("jetpt", "jets above 400GeV that are true b", 31, 25, 800 ) 
eventhist=ROOT.TH1D("eventhist", "leading jet per event above 400GeV that are true b", 31, 25, 800 ) 


runs=['a','d','e']
runslumi=[36207.66,44307.4,58450.1]
for i in range(0,len(runs)):
    inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_leg/boosted/ttH_PP8_mc16'+str(runs[i])+'.root')
    tree = inFile.Get("nominal_Loose")


    for ievt in range(0,tree.GetEntries()):	
        tree.GetEntry(ievt)
        weight=tree.weight_normalise * runslumi[i] * tree.weight_mc * tree.weight_pileup * tree.weight_leptonSF * tree.weight_jvt * tree.weight_bTagSF_DL1r_Continuous
        passjetsel=False
        DNNHiggs=False
        if tree.passedOfflineBoostedSelection == 0 :
            continue
        for j in range(0,tree.rcjet_pt.size()):
            if tree.jet_pt[j] > 25000 and tree.jet_truthflav[j]==5:
                ptjet = tree.jet_pt[j]/1000
                jetpt.Fill(ptjet,weight)
                #print(ptjet)
                eventhist.Fill(tree.jet_pt[0]/1000,weight)
        
                           
                           


outHistFile = ROOT.TFile.Open("jetpttureb.root" ,"RECREATE")
jetpt.Write()
eventhist.Write()
outHistFile.Close()
print(';aklsdfj')
print(jetpt.Integral(16,32))
print(eventhist.Integral(17,31))
                

        