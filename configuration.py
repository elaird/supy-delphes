from supy.defaults import *


def mainTree():
    return ("/", "Delphes")


def initializeROOT(r, cppFiles=[]):
    r.gROOT.SetStyle("Plain")
    r.gStyle.SetPalette(1)
    r.TH1.SetDefaultSumw2(True)
    r.gErrorIgnoreLevel = 2000
    r.gROOT.SetBatch(True)
    r.gSystem.Load("libDelphes.so")


def useCachedFileLists():
    return False


def detectorConfig():
    #return "/PhaseI/Configuration0/NoPileUp/"
    #return "/PhaseI/Configuration0/140PileUp/"
    return "/PhaseII/Configuration3/140PileUp/"


def LorentzVectorType():
    return ('PtEtaPhiM4D', 'double')


def experiment():
    return "cms"
