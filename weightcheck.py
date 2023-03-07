import ROOT


jetpt= ROOT.TH1D("jetpt", "tth events after 400GeV", 20, 300, 800 ) 
tthevents2= ROOT.TH1D("tthevent2", "truth flav match b after 400GeV", 5, 300, 800 ) 

#Defining the selection
nevt = 0                        # number of total events considered
nevt_sel = 0			# number of total selected events
nselectedjets= 0                # number of selected jets
isMC = False
selected_jet = ROOT.TLorentzVector() 
runs=['a','d','e']
runslumi=[36207.66,44307.4,58450.1]
for i in range(0,len(runs)):
    inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/ttH_PP8_mc16'+str(runs[i])+'.root')
    tree = inFile.Get("nominal_Loose")


    for ievt in range(0,tree.GetEntries()):	
        nevt += 1
        tree.GetEntry(ievt)
        weight=tree.weight_normalise * runslumi[i] * tree.weight_mc * tree.weight_pileup * tree.weight_leptonSF * tree.weight_jvt * tree.weight_bTagSF_DL1r_Continuous
        passjetsel=False
        DNNHiggs=False
        if tree.passedOfflineBoostedSelection == 0 :
            continue
        for j in range(0,tree.rcjet_pt.size()):
            if tree.rcjet_pt[j] > 300000:# and tree.jet_truthflav==4:
                ptjet = tree.rcjet_pt[j]/1000
                #print(ptjet)
                #print(tree.rcjet_pt)
                #print(weight)
                tthevents2.Fill(ptjet,weight)
        jetpt.Fill(tree.rcjet_pt[0]/1000,weight)
        
                


outHistFile = ROOT.TFile.Open("400gevtrueb.root" ,"RECREATE")
tthevents2.Write()
jetpt.Write()
outHistFile.Close()
print(tthevents2.Integral())
print(jetpt.Integral())
print(jetpt.GetBinContent(21))