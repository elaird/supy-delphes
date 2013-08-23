import utils
import ROOT as r
from supy import wrappedChain


class GenWeight(wrappedChain.calculable):
    def update(self, _):
        self.value = self.source["Event"][0].Weight


class HT(wrappedChain.calculable):
    def update(self, _):
        self.value = self.source["ScalarHT"][0].HT


class Particles(wrappedChain.calculable):
    @property
    def name(self):
        return "%sParticles" % self.label

    def __init__(self, pids=[], label=""):
        self.pids = pids
        self.label = label
        if self.pids:
            self.moreName = "pdgId in %s" % str(list(self.pids))

    def update(self, _):
        self.value = []
        for particle in self.source["Particle"]:
            if particle.PID in self.pids:
                self.value.append(particle)


class bTaggedJets(wrappedChain.calculable):
    def update(self, _):
        print "add mask"
        self.value = []
        for jet in self.source["Jet"]:
            if jet.BTag:
                self.value.append(jet)


class JetMatchedTo(wrappedChain.calculable):
    @property
    def name(self):
        return "JetMatchedTo_%s" % self.sourceKey

    def __init__(self, sourceKey="", minPt=None):
        self.sourceKey = sourceKey
        self.minPt = minPt

    def update(self, _):
        self.value = {}
        #print
        #print self.source["Event"][0].Number
        for particle in self.source[self.sourceKey]:
            if self.minPt and particle.PT < self.minPt:
                continue
            dR = []
            #print "particle eta=%6.3f, phi=%6.3f, pt=%6.1f" % (particle.Eta, particle.Phi, particle.PT)
            for jet in self.source["Jet"]:
                #print "jet      eta=%6.3f, phi=%6.3f, pt=%6.1f, DR=%6.3f" % (jet.Eta, jet.Phi, jet.PT, utils.deltaR(particle, jet))
                dR.append((utils.deltaR(particle, jet), jet))
            self.value[particle] = min(dR)[1] if dR else None
            #print min(dR)[0], self.value[particle].PT
        #print
