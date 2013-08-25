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
            dr = utils.deltaR(particle, jet)
            if self.maxDR and (self.maxDR < dr):
                continue
            self.book.fill(dr, "DeltaR", 50, 0.0, 5.0, title=";#DeltaR"+self.title)
            self.book.fill(jet.PT/particle.PT, "ptRatio", 50, 0.0, 2.0,  title=";jet pT / particle pT"+self.title)


class efficiencyHistogrammer(analysisStep):
    def __init__(self, sourceKey="", particleVar="", jetFlag="", mask=0,
                 maxDR=None, minPt=None, maxAbsEta=None, binsMinMax=None):
        for item in ["sourceKey", "particleVar", "jetFlag", "mask",
                     "maxDR", "minPt", "maxAbsEta", "binsMinMax"]:
            setattr(self, item, eval(item))

        stem = "_".join([sourceKey, self.particleVar, self.jetFlag, hex(self.mask)])
        self.tagTitle = ("tag_"+stem, ";particle %s (%s);matches / bin" % (self.particleVar, self.sourceKey))
        self.probeTitle = ("probe_"+stem, self.tagTitle[1].replace(")", " with %s)" % self.jetFlag))
        self.effTitle = ("efficiency_"+stem, ";particle %s (%s);%s&%s  efficiency" % (self.particleVar,
                                                                                      self.sourceKey,
                                                                                      self.jetFlag,
                                                                                      hex(self.mask)))

        self.moreName = "%s&%s eff. by %s (%s)" % (self.jetFlag, hex(self.mask), self.particleVar, self.sourceKey)
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


    def uponAcceptance(self, eventVars):
        for particle, jet in eventVars[self.sourceKey].iteritems():
            if self.maxDR and self.maxDR < utils.deltaR(particle, jet):
                continue
            if self.minPt and particle.PT < self.minPt:
                continue
            if self.maxAbsEta and self.maxAbsEta < abs(particle.Eta):
                continue
            x = getattr(particle, self.particleVar)
            self.book.fill(x, self.tagTitle[0], *self.binsMinMax, title=self.tagTitle[1])
            if getattr(jet, self.jetFlag) & self.mask:
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


class iterHistogrammer(analysisStep):
    def __init__(self, var="", attr="", labelIndex=False, maxIndex=None, nBins=None, xMin=None, xMax=None):
        for item in ["var", "attr", "labelIndex", "maxIndex"]:
            setattr(self, item, eval(item))
        self.bins = (nBins, xMin, xMax)

    def uponAcceptance(self, eventVars):
        for i, object in enumerate(eventVars[self.var]):
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
