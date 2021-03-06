#! /usr/bin/python

"""
Usage: 
  MBIplotter.py ROOTFILE HISTO [-r rebin] [-c cut] [-q quant] [-e energy]

Plot the Material Budget from a specified histogram in a rootfile.

Arguments:
  ROOTFILE  Rootfile containing the data
  HISTO     Name of the histogram including the directory inside the rootfile

Options:
  -h --help
  -r rebin  Perform rebinning in XY with a factor of <rebin> [default: 1]
  -q quant  Specify the quantiles, give the inner percentage [default: 90.]
  -c cut    Specify the minimum number of entries for each distribution [default: 100]
  -e energy Calculate the material budget using the given <energy>
"""

from docopt import docopt

import numpy as np
import matplotlib.pyplot as plt

from ROOT import *

import math
import sys
import getopt
import csv

from array import array

def highfunc(energy, eps):
        return 0.0136/energy*math.sqrt(eps)*(1.+0.038*math.log(eps))

def getEps(trueAngle, energy, minE, maxE, precision=0.0005):
    currentEps = (maxE+minE)/2.
    currentHighland = highfunc(energy, currentEps)
    currentPrecision = maxE-currentEps
    
    if currentPrecision < precision:
        return currentEps
    
    if trueAngle > currentHighland:
        return getEps(trueAngle, energy, currentEps, maxE, precision)
    else:
        return getEps(trueAngle, energy, minE, currentEps, precision)


if __name__ == '__main__':
    args = docopt(__doc__)

    rootfilename = args['ROOTFILE']
    whichHisto = args['HISTO']

    rebin = int(args['-r'])
    quantilesPercentage = float(args['-q'])
    eventCut = int(args['-c'])
    if args['-e']:
        useEps = True
        energy = float(args['-e'])
    else:
        useEps = False

    labelsize = 0.05
    titlesize = 0.05

    quantilesFrac = float(quantilesPercentage)/100.

    quantilesIn = array('d', [quantilesFrac,1.-quantilesFrac/2.])
    quantilesOut = array('d', [0.0,0.0])

    
    rootfile = TFile(rootfilename)
    
    hist3D = rootfile.Get(whichHisto)

    if rebin>1:
        hist3D.Rebin3D(rebin,rebin,1)

    nx = hist3D.GetNbinsX()
    ny = hist3D.GetNbinsY()

    startx = hist3D.GetXaxis().GetBinLowEdge(1)
    endx = hist3D.GetXaxis().GetBinLowEdge(nx)+hist3D.GetXaxis().GetBinWidth(nx)
    starty = hist3D.GetYaxis().GetBinLowEdge(1)
    endy = hist3D.GetYaxis().GetBinLowEdge(ny)+hist3D.GetYaxis().GetBinWidth(ny)

    hist = TH2D("hist","MBI",nx,startx,endx,ny,starty,endy)

    for ix in range(1,nx+1):
        if not ix%10:
            print "Bin " + str(ix) + " of " + str(nx)
        for iy in range(1,ny+1):
            xq = array('d', [0.05,0.95])
            yq = array('d', [0.0,0.0])
            
            proj2 = hist3D.ProjectionZ("_pz2",ix,ix,iy,iy)
            
            nentries = proj2.GetEntries()
            if nentries<eventCut:
                #print "Not enough entries in the histogram"
                continue
            
            proj2.GetQuantiles(2,yq,xq)
            
            nbins2 = proj2.GetNbinsX()
            MAD=0.
            totalEntries=0
            for madi in range(0,nbins2):
                binCenter = proj2.GetBinCenter(madi)
                if binCenter>yq[0] and binCenter<yq[1]:
                    binContent = proj2.GetBinContent(madi)
                    MAD += binContent*abs(binCenter)
                    totalEntries += binContent
                    
            if totalEntries>0:
                MAD /= totalEntries
                
            MAD *= 1.2532

            if useEps:
                eps = getEps(MAD/1000.,energy,0.,5.)
                hist.SetBinContent(ix,iy,eps)
            else:
                hist.SetBinContent(ix,iy,pow(MAD,2))

    
    c1 = TCanvas("c1","c1",1200,600)
    
    gStyle.SetOptStat(0)
    hist.GetZaxis().SetNdivisions(5,0,5)
    
    hist.GetXaxis().SetTitle("x [mm]")
    hist.GetYaxis().SetTitle("y [mm]")
    if useEps:
        hist.GetZaxis().SetTitle("#varepsilon(k_{x,y})")
    else:
        hist.GetZaxis().SetTitle("MAD90(k_{x,y})^{2} [mrad^{2}]")
    
    hist.SetTitleSize(titlesize,"xyz")
    hist.SetLabelSize(titlesize,"xyz")
    
    c1.SetRightMargin(0.165)
    c1.SetBottomMargin(0.11)
    #c1.SetLeftMargin(0.135)
    hist.GetZaxis().SetTitleOffset(1.16)
    hist.GetYaxis().SetTitleOffset(0.95)
    hist.GetXaxis().SetTitleOffset(0.95)
    
    hist.SetTitle("")
    
    hist.Draw("colz")    
    
    c1.Update()

    blah = raw_input("Press Enter to close.")
