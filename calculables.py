import math
import units
import utils
import ROOT as r
import supy

class GenWeight(supy.wrappedChain.calculable):
    def update(self, _):
        self.value = self.source["Event"][0].Weight


class HT(supy.wrappedChain.calculable):
    def update(self, _):
        self.value = self.source["ScalarHT"][0].HT


class rho(supy.wrappedChain.calculable):
    def update(self, _):
        if "Rho" in self.source:
            self.value = self.source["Rho"][0].HT
        else:
            self.value = None


class window(supy.wrappedChain.calculable):
    @property
    def name(self):
        out = self.var
        if self.min is not None:
            out = str(int(self.min))+".le."+out
        if self.max is not None:
            out += ".le."+str(int(self.max))
        return out

    def __init__(self, var, min=None, max=None):
        for item in ["var", "min", "max"]:
            setattr(self, item, eval(item))

    def update(self, _):
        val = self.source[self.var]
        self.value = self.min <= val and ((self.max is None) or val <= self.max)


class SumP4(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%sSumP4" % self.label

    def __init__(self, label=""):
        self.label = label
        self.value = supy.utils.LorentzV()
        self.vec = supy.utils.LorentzV()

    def update(self, _):
        self.value.SetCoordinates(0.0, 0.0, 0.0, 0.0)

        for particle in self.source[self.label]:
            if hasattr(particle, "PT"):
                self.vec.SetCoordinates(particle.PT, particle.Eta, particle.Phi, particle.Mass)
                self.value += self.vec
            else:
                self.value += particle


class Filtered(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s%ss" % (self.label, self.key)

    def __init__(self, pids=[], status=[], label="", ptMin=None, absEtaMax=None, key="Particle", ptSort=False, pt="PT"):
        for item in ["pids", "status", "label", "ptMin", "absEtaMax", "key", "ptSort", "pt"]:
            setattr(self, item, eval(item))

        self.moreName = ""
        if self.pids:
            self.moreName += "; pdgId in %s" % str(list(self.pids))
        if self.status:
            self.moreName += "; status in %s" % str(list(self.status))
        if self.ptMin:
            self.moreName += "; %g < pT" % self.ptMin
        if self.absEtaMax:
            self.moreName += "; |eta| < %g" % self.absEtaMax

    def update(self, _):
        self.value = []
        for particle in self.source[self.key]:
            if self.pids and (particle.PID not in self.pids):
                continue
            if self.status and (particle.Status not in self.status):
                continue
            if self.ptMin and (getattr(particle, self.pt) < self.ptMin):
                continue
            if self.absEtaMax and (self.absEtaMax < abs(particle.Eta)):
                continue
            self.value.append(particle)
        if self.ptSort:
            self.value.sort(key=lambda x:getattr(x, self.pt), reverse=True)


class bTaggedJets(supy.wrappedChain.calculable):
    def update(self, _):
        print "add mask"
        self.value = []
        for jet in self.source["Jet"]:
            if jet.BTag:
                self.value.append(jet)


class JetMatchedTo(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "JetMatchedTo_%s" % self.sourceKey

    def __init__(self, sourceKey="", minPt=None, maxDR=None):
        for item in ["sourceKey", "minPt", "maxDR"]:
            setattr(self, item, eval(item))

    def update(self, _):
        self.value = {}
        for particle in self.source[self.sourceKey]:
            if self.minPt and particle.PT < self.minPt:
                continue
            dR = []
            for jet in self.source["Jet"]:
                dr = utils.deltaR(particle, jet)
                if self.maxDR and self.maxDR < dr:
                    continue
                dR.append((dr, jet))
            self.value[particle] = min(dR)[1] if dR else None


class nMatches(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "nMatches_%s" % self.key

    def __init__(self, key="", maxDR=None):
        self.key = key
        self.maxDR = maxDR
        if self.maxDR:
            self.moreName = "#DeltaR < %g" % self.maxDR

    def update(self, _):
        self.value = 0
        for particle, jet in self.source[self.key].iteritems():
            if (not jet) or (self.maxDR and (self.maxDR < utils.deltaR(particle, jet))):
                continue
            self.value += 1


class DeltaR(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "DeltaR_%s" % self.key

    def __init__(self, key=""):
        self.key = key

    def update(self, _):
        objs = self.source[self.key]
        assert len(objs) == 2, len(objs)
        assert all(objs), objs
        self.value = utils.deltaR(*objs)


class JetsFixedMass(supy.wrappedChain.calculable):
    def __init__(self, key="", m=None):
        assert m is not None
        self.m = m
        self.key = key
        self.lv = [supy.utils.LorentzV(), supy.utils.LorentzV()]

    def update(self, _):
        self.value = []
        jets = self.source[self.key]
        assert len(jets) == 2, len(jets)
        assert all(jets), jets
        for i in range(2):
            self.lv[i].SetCoordinates(jets[i].PT, jets[i].Eta, jets[i].Phi, self.m)
        self.value = self.lv


class jdj(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "jdj_%s" % self.jets

    def __init__(self, jets=""):
        self.jets = jets

    def update(self, _):
        jets = self.source[self.jets]
        assert (len(jets) == 2) and all(jets), jets
        self.value = math.sqrt(2.0*supy.utils.Dot(*jets))
