#! /usr/bin/env python

#import argparse
import glob
import os
import sys

import ROOT

#
mainFolder = "/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/"

#Booking histograms
#h_l1pt = ROOT.TH1D("l1pt", "l1 transverse momentum", 20, 10, 400 ) # 1st lepton pT   			# What histograms are we interested in?
#h_l2pt = ROOT.TH1D("l2pt", "l2 transverse momentum", 20, 10, 400 )
# 2nd lepton pT
tthevents= ROOT.TH1D("tthevents", "tth events after 400GeV", 20, 300, 800 ) 
tthevents2= ROOT.TH1D("tthevents2", "tth events after 400GeV", 20, 300, 800 ) 

#Defining the selection
nevt = 0                        # number of total events considered
nevt_sel = 0			# number of total selected events
nselectedjets= 0                # number of selected jets
isMC = False
selected_jet = ROOT.TLorentzVector()     #defining the TLorentzVector to get the jet mass later 
#print("The input directory is "+inputDir)
inFile = ROOT.TFile.Open('/Users/zefranrozario/Desktop/ttHbb_legacy/boosted/ttH_PP8_mc16a.root')
tree = inFile.Get("nominal_Loose")
tree.Show(1)
#
print ("INFO: TotalEvents: "+str(tree.GetEntries()))
ptjet, etajet, phijet = 0,0,0
#
for ievt in range(0,tree.GetEntries()):	
    nevt += 1
    tree.GetEntry(ievt)
    #
    weight=tree.weight_normalise * 36207.66
    passjetsel=False
    DNNHiggs=False
    #
    if tree.passedOfflineBoostedSelection == 0:
        continue
    for j in range(0,tree.rcjet_pt.size()):
        if tree.rcjet_pt[j] > 300000 and abs(tree.rcjet_eta[j])<2:
            ptjet, etajet, phijet,Ejet = tree.rcjet_pt[j]/1000,tree.rcjet_eta[j],tree.rcjet_phi[j],tree.rcjet_e[j]/1000 #Adding the jet transverse energy to the list
            selected_jet.SetPtEtaPhiE(ptjet,etajet,phijet,Ejet) #Creating the TLorentzVector by giving it the jet pT, eta, phi and ET
            #            print('the pt of jet '+str(ievt)+','+str(j)+','+str(j)+' was '+str(ptjet))
            if selected_jet.M() < 50:          # 50 GeV cut on the jet mass 
                continue
            #            print(selected_jet.M())
            passjetsel=True
            nselectedjets+=1
    #
    if nselectedjets<1: #rejecting the event if they fail the jet requirements 
        continue
    #
    for j in range(0,tree.rcjet_pHiggs_DNN.size()):
        if  tree.rcjet_pHiggs_DNN[j] >=0.6:
            DNNHiggs=True
    #
    if DNNHiggs==False:
        continue
    nevt_sel+=1 
    #
    # Example of how to access the TLorentz vector info
    if selected_jet.M() < 100 or selected_jet.M() > 140:
        continue
    tthevents.Fill(ptjet,weight)

#print(nevt)
#print(ptjet)
print(nevt_sel)
#print(nevt)
#print(nevt_sel/nevt)
#print(nselectedjets)
#            
outHistFile = ROOT.TFile.Open("try.root" ,"RECREATE")
tthevents.Write()
outHistFile.Close()
#tthevents.Draw()
#tthevents2.Draw()
#print(tthevents2.Integral())
print(tthevents.Integral())
