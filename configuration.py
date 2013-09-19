from supy.defaults import *
import supy


def mainTree():
    return ("/", "Delphes")


def initializeROOT(r, cppFiles=[]):
    r.gROOT.SetStyle("Plain")
    r.gStyle.SetPalette(1)
    r.TH1.SetDefaultSumw2(True)
    r.gErrorIgnoreLevel = 2000
    r.gROOT.SetBatch(True)

    site = supy.sites.site()
    if site == "cern":
        r.gSystem.Load("libDelphes-3.0.10_ECFA_v1.so")
    elif site == "fnal":
        r.gSystem.Load("libDelphes-3.0.9.1.so")
    else:
        r.gSystem.Load("libDelphes.so")


def useCachedFileLists():
    return False


def detectorConfig(site=""):
    if site == "cern":
        #return "/PhaseI/Configuration0/NoPileUp/"
        #return "/PhaseI/Configuration0/140PileUp/"
        #return "/PhaseII/Configuration3/140PileUp/"
        #return "/PhaseII/Configuration4/140PileUp/"
        return "/PhaseII/Configuration4v2/140PileUp/"
    elif site == "fnal":
        return "/140PileUp/"


def LorentzVectorType():
    return ('PtEtaPhiM4D', 'double')


def experiment():
    return "cms"
