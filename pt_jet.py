import ROOT

jetpt= ROOT.TH1D("jetpt", "tth events after 400GeV", 20, 300, 800 ) 
tthevents2= ROOT.TH1D("tthevents2", "tth events after 400GeV", 20, 300, 800 ) 

#Defining the selection
nevt = 0                        # number of total events considered
nevt_sel = 0			# number of total selected events
nselectedjets= 0                # number of selected jets
isMC = False
selected_jet = ROOT.TLorentzVector() 
inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/ttH_PP8_mc16a.root')
tree = inFile.Get("nominal_Loose")
pt=[]
for ievt in range(0,tree.GetEntries()):	
    nevt += 1
    tree.GetEntry(ievt)
    weight=tree.weight_mc
    passjetsel=False
    DNNHiggs=False
    if tree.passedOfflineBoostedSelection == 0:
        continue
    for j in range(0,tree.rcjet_pt.size()):
        maxpt=tree.rcjet_pt[0]
        #print("akjdsfhadjk"+str(maxpt))
        pt.append(tree.rcjet_pt[j])
        if abs(tree.rcjet_pt[j]) > maxpt:
            maxpt=tree.rcjet_pt[j]
            print(j)
            print(maxpt)
            print(nevt)
            print(tree.rcjet_pt[j])
               
print('jhkjh   '+str(max(pt)))
print(pt.index(max(pt)))
print(len(pt))