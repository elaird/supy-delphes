from displayer import displayer
import utils
import ROOT as r
from supy import analysisStep


class matchHistogrammer(analysisStep):
    def __init__(self, sourceKey="", maxDR=None):
        self.sourceKey = sourceKey
        self.maxDR = maxDR
        self.title = ";matches / bin"
        if self.maxDR:
            extra = " (%s,  #DeltaR<%3.1f)" % (self.sourceKey, self.maxDR)
        else:
            extra = " (%s)" % self.sourceKey
        self.title = extra + self.title


    def uponAcceptance(self, eventVars):
        for particle, jet in eventVars[self.sourceKey].iteritems():
            dr = utils.deltaR(particle, jet) if jet else 999.9
            if self.maxDR and (self.maxDR < dr):
                continue
            jetPT = jet.PT if jet else 0.0
            self.book.fill(dr, "DeltaR", 50, 0.0, 5.0, title=";#DeltaR"+self.title)
            self.book.fill(jetPT/particle.PT, "ptRatio", 50, 0.0, 2.0,  title=";jet pT / particle pT"+self.title)


class efficiencyHistogrammer(analysisStep):
    def __init__(self, sourceKey="", particleVar="",
                 maxDR=None, minPt=None, maxAbsEta=None, binsMinMax=None):
        for item in ["sourceKey", "particleVar",
                     "maxDR", "minPt", "maxAbsEta", "binsMinMax"]:
            setattr(self, item, eval(item))

        stem = "_".join([sourceKey, self.particleVar])#, self.jetFlag, hex(self.mask)])
        self.tagTitle = ("tag_"+stem, ";particle %s (%s, all);matches / bin" % (self.particleVar, self.sourceKey))
        self.probeTitle = ("probe_"+stem,
                           self.tagTitle[1].replace("all)", "passing %s)" % self.name.replace("EfficiencyHistogrammer", "")))
        self.effTitle = ("efficiency_"+stem,
                         ";particle %s (%s);%s" % (self.particleVar,
                                                   self.sourceKey,
                                                   self.name.replace("Histogrammer", ""),
                                                   ))

        self.moreName = "eff. by %s (%s)" % (self.particleVar, self.sourceKey)
        conds = []
        if self.maxDR:
            conds.append("#DeltaR < %s" % self.maxDR)
        if self.minPt:
            conds.append("%s < pT" % self.minPt)
        if self.maxAbsEta:
            conds.append("|#eta| < %s" % self.maxAbsEta)
        if conds:
            conds = ",  ".join(conds)
            self.moreName.replace(")", ", %s)" % conds)
            self.effTitle = (self.effTitle[0], self.effTitle[1]+" (%s)" % conds)

    def passFunc(self, particle, jet):
        return True

    def uponAcceptance(self, eventVars):
        for particle, jet in eventVars[self.sourceKey].iteritems():
            dr = utils.deltaR(particle, jet) if jet else 999.9
            if self.maxDR and self.maxDR < dr:
                continue
            if self.minPt and particle.PT < self.minPt:
                continue
            if self.maxAbsEta and self.maxAbsEta < abs(particle.Eta):
                continue
            x = getattr(particle, self.particleVar)
            self.book.fill(x, self.tagTitle[0], *self.binsMinMax, title=self.tagTitle[1])
            if jet and self.passFunc(particle, jet):
                self.book.fill(x, self.probeTitle[0], *self.binsMinMax,  title=self.probeTitle[1])


    def mergeFunc(self, products):
        probe = r.gDirectory.Get(self.probeTitle[0])
        tag = r.gDirectory.Get(self.tagTitle[0])
        if not (tag and probe):
            return
        efficiency = probe.Clone(self.effTitle[0])
        efficiency.SetTitle(self.effTitle[1])
        efficiency.Divide(probe, tag, 1, 1, "B")
        for bin in [0, self.binsMinMax[0]+1]:
            efficiency.SetBinContent(bin, 0)
            efficiency.SetBinError(bin, 0)
        efficiency.Write()
        #efficiency.Print("all")
        print "Output updated with efficiency %s." % self.effTitle[0]


class b1EfficiencyHistogrammer(efficiencyHistogrammer):
    def passFunc(self, particle, jet):
        return jet.BTag & 0x1


class b2EfficiencyHistogrammer(efficiencyHistogrammer):
    def passFunc(self, particle, jet):
        return jet.BTag & 0x2


class matchEfficiencyHistogrammer(efficiencyHistogrammer):
    def passFunc(self, particle, jet):
        return utils.deltaR(particle, jet) < 0.5


class iterHistogrammer(analysisStep):
    def __init__(self, var="", attr="", labelIndex=False, maxIndex=None, nBins=None, xMin=None, xMax=None):
        for item in ["var", "attr", "labelIndex", "maxIndex"]:
            setattr(self, item, eval(item))
        self.bins = (nBins, xMin, xMax)

    def uponAcceptance(self, eventVars):
        for iObject in range(utils.size(eventVars, self.var)):
            object = eventVars[self.var][iObject]
            if (self.maxIndex is not None) and self.maxIndex < i:
                continue
            key = self.attr
            yTitle = self.var
            if self.labelIndex:
                key += " (%s %d)" % (self.var, i)
                yTitle = "Events"
            self.book.fill(getattr(object, self.attr), key, *self.bins, title=";%s;%s / bin" % (key, yTitle))


class modEntry(analysisStep):
    def __init__(self, base=None, value=None):
        for item in ["base", "value"]:
            a = eval(item)
            assert a is not None, a
            setattr(self, item, a)
        self.moreName = "entry % " + "%d == %d" % (self.base, self.value)

    def select(self, eventVars):
        return (eventVars["entry"] % self.base) == self.value
