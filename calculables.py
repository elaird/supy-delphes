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
        self.value = self.source["Rho"][0].HT


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
            self.vec.SetCoordinates(particle.PT, particle.Eta, particle.Phi, particle.Mass)
            self.value += self.vec


class Filtered(supy.wrappedChain.calculable):
    @property
    def name(self):
        return "%s%ss" % (self.label, self.key)

    def __init__(self, pids=[], label="", ptMin=None, absEtaMax=None, key="Particle", ptSort=False, pt="PT"):
        for item in ["pids", "label", "ptMin", "absEtaMax", "key", "ptSort", "pt"]:
            setattr(self, item, eval(item))

        self.moreName = ""
        if self.pids:
            self.moreName += "; pdgId in %s" % str(list(self.pids))
        if self.ptMin:
            self.moreName += "; %g < pT" % self.ptMin
        if self.absEtaMax:
            self.moreName += "; |eta| < %g" % self.absEtaMax

    def update(self, _):
        self.value = []
        for particle in self.source[self.key]:
            if self.pids and (particle.PID not in self.pids):
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

    def __init__(self, sourceKey="", minPt=None):
        self.sourceKey = sourceKey
        self.minPt = minPt

    def update(self, _):
        self.value = {}
        for particle in self.source[self.sourceKey]:
            if self.minPt and particle.PT < self.minPt:
                continue
            dR = []
            for jet in self.source["Jet"]:
                dR.append((utils.deltaR(particle, jet), jet))
            self.value[particle] = min(dR)[1] if dR else None
