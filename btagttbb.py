import ROOT
from tabulate import tabulate
jetpt_b= ROOT.TH1D("jetpt_b", "jets above 400GeV that are true b", 31, 25, 800 )
eventhist_b=ROOT.TH1D("eventhist_b", "leading jet per event above 400GeV that are true b", 31, 25, 800 )
jetpt_c= ROOT.TH1D("jetpt_c", "jets above 250GeV that are true c", 31, 25, 800 )
eventhist_c=ROOT.TH1D("eventhist_c", "leading jet per event above 250GeV that are true c", 31, 25, 800 )
jetpt_light= ROOT.TH1D("jetpt_light", "jets above 300GeV that are true light", 31, 25, 800 )
eventhist_light=ROOT.TH1D("eventhist_light", "leading jet per event above 300GeV that are true light", 31, 25, 800 )
jetpt_total=ROOT.TH1D("jetpt_total", "all jets outside the calibration", 31, 25, 800 )
eventpt_total=ROOT.TH1D("eventpt_total", "all events outside the calibration", 31, 25, 800 )
jetpt=ROOT.TH1D("jetpt", "all jets", 31, 25, 800 )
hs = ROOT.TList()
runs=['a','d','e']
runslumi=[36207.66,44307.4,58450.1]
for i in range(0,len(runs)):
    inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/ttH_PP8_mc16'+str(runs[i])+'.root')
    tree = inFile.Get("nominal_Loose")

    if tree.boostedRecoHiggsPt > 450000:
        for ievt in range(0,tree.GetEntries()):	
            tree.GetEntry(ievt)
            weight=tree.weight_normalise * runslumi[i] * tree.weight_mc * tree.weight_pileup * tree.weight_leptonSF * tree.weight_jvt * tree.weight_bTagSF_DL1r_Continuous
            if tree.passedOfflineBoostedSelection == 0:
                continue
            passjetsel_b=False
            passjetsel_c=False
            passjetsel_light=False
            bjets=[]
            cjets=[]
            lightjets=[]

            for j in range(0,tree.jet_pt.size()) :
                ptjet = tree.jet_pt[j]/1000
                jetpt.Fill(ptjet,weight)
                if tree.jet_truthflav[j]==5:
                    bjets.append(tree.jet_pt[j])
                    jetpt_b.Fill(ptjet,weight)
                    #jetpt_total.Fill(ptjet,weight)
                    passjetsel_b=True
                elif tree.jet_truthflav[j]==4:
                    cjets.append(tree.jet_pt[j])
                    jetpt_c.Fill(ptjet,weight)
                    #jetpt_total.Fill(ptjet,weight)
                    passjetsel_c=True
                elif tree.jet_truthflav[j]== 1 or 16:
                    lightjets.append(tree.jet_pt[j])
                    jetpt_light.Fill(ptjet,weight)
                    #jetpt_total.Fill(ptjet,weight)
                    passjetsel_light=True
                    
            if passjetsel_b==True and tree.boostedRecoHiggsPt > 450000:
                eventhist_b.Fill(bjets[0]/1000,weight)
                eventpt_total.Fill(bjets[0]/1000,weight)
                
                
            if passjetsel_c==True and tree.boostedRecoHiggsPt > 450000:
                eventhist_c.Fill(cjets[0]/1000,weight)
                eventpt_total.Fill(cjets[0]/1000,weight)
                
            if passjetsel_light==True and tree.boostedRecoHiggsPt > 450000:
                eventhist_light.Fill(lightjets[0]/1000,weight)
                eventpt_total.Fill(lightjets[0]/1000,weight)

                
    
                           
                           


outHistFile = ROOT.TFile.Open("jetpttureb_ttbb.root" ,"RECREATE")
jetpt_b.Write()
eventhist_b.Write()
jetpt_c.Write()
eventhist_c.Write()
jetpt_light.Write()
eventhist_light.Write()
#jetpt_total.Write()
jetpt.Write()
eventpt_total.Write()
outHistFile.Close()
print('just empty space')
fracjet_b=jetpt_b.Integral(jetpt_b.FindFixBin( 400.0 ), jetpt_b.GetNbinsX()+1)
fracevent_b=eventhist_b.Integral(eventhist_b.FindFixBin( 400.0 ), eventhist_b.GetNbinsX()+1)
fracjet_c=jetpt_c.Integral(jetpt_c.FindFixBin( 250.0 ), jetpt_c.GetNbinsX()+1)
fracevent_c=eventhist_c.Integral(eventhist_c.FindFixBin( 250.0 ), eventhist_c.GetNbinsX()+1)
fracjet_light=jetpt_light.Integral(jetpt_light.FindFixBin( 300.0 ), jetpt_light.GetNbinsX()+1)
fracevent_light=eventhist_light.Integral(eventhist_light.FindFixBin( 300.0 ), eventhist_light.GetNbinsX()+1)
hs.Add(jetpt_light)
hs.Add(jetpt_b)
hs.Add(jetpt_c)
#list=[fracjet_b,fracjet_c,fracjet_light]
jetpt_total.Merge(hs)

#print(totalJEToutside.Integral())

print('The Fraction of b jets above 400GeV: '+str(fracjet_b/jetpt_b.Integral(1,jetpt_b.GetNbinsX()+1)))
print('The Fraction of b events above 400GeV: '+str(fracevent_b/eventhist_b.Integral(1,eventhist_b.GetNbinsX()+1)))
print('The Fraction of c jets above 250GeV: '+str(fracjet_c/jetpt_c.Integral(1,jetpt_c.GetNbinsX()+1)))
print('The Fraction of c events above 250GeV: '+str(fracevent_c/eventhist_c.Integral(1,eventhist_c.GetNbinsX()+1)))
print('The Fraction of light jets above 300GeV: '+str(fracjet_light/jetpt_light.Integral(1,jetpt_light.GetNbinsX()+1)))
print('The Fraction of light events above 300GeV: '+str(fracevent_light/eventhist_light.Integral(1,eventhist_light.GetNbinsX()+1)))
print('Total number of jets: '+str(jetpt.GetEntries()))
#print('Total number of jets outside calibration: '+str(jetpt_total.GetEntries()))
#print('The total number of jets outside the calibration: '+str(jetpt_total.Integral()))
print('The fraction of jets outside the calibration: ')#+str(jetpt_total.Integral(1,jetpt_total.GetNbinsX()+1)/jetpt.Integral(1,jetpt.GetNbinsX()+1)))



print((jetpt_b.GetBinContent(jetpt_b.FindFixBin( 400.0 ), jetpt_b.GetNbinsX()+1)+jetpt_c.GetBinContent(jetpt_c.FindFixBin( 250.0 ), jetpt_c.GetNbinsX()+1)+jetpt_light.GetBinContent(jetpt_light.FindFixBin( 300.0 ), jetpt_light.GetNbinsX()+1))/jetpt.GetBinContent(1,jetpt.GetNbinsX()+1))
print((eventhist_b.GetBinContent(eventhist_b.FindFixBin( 400.0 ), eventhist_b.GetNbinsX()+1)+eventhist_c.GetBinContent(eventhist_c.FindFixBin( 250.0 ), eventhist_c.GetNbinsX()+1)+eventhist_light.GetBinContent(eventhist_light.FindFixBin( 300.0 ), eventhist_light.GetNbinsX()+1))/eventpt_total.GetBinContent(1,eventpt_total.GetNbinsX()+1))




data = [[1, 'Liquid', 24, 12],
[2, 'Virtus.pro', 19, 14],
[3, 'PSG.LGD', 15, 19],
[4,'Team Secret', 10, 20]]
print (tabulate(data, headers=["Pos", "Team", "Win", "Lose"]))
