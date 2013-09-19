import bisect
from displayer import displayer
import utils
import ROOT as r
from supy import analysisStep


class matchPtHistogrammer(analysisStep):
    def __init__(self, sourceKey="", etas=[], correctPtAxis=False, correctRatio=False, plot2D=False, particleLabel="particle"):
        for item in ["sourceKey", "etas", "correctPtAxis", "correctRatio", "plot2D", "particleLabel"]:
            setattr(self, item, eval(item))
        self.title = " (%s);matches / bin" % self.sourceKey

    def bbl(self, eta=None):
        bin = bisect.bisect_left(self.etas, abs(eta))
        label = ""
        if bin != 0:
            label += "%3.1f < " % self.etas[bin-1]
        label += "|%s#eta|" % ("jet ")
        if bin != len(self.etas):
            label += " #leq %3.1f" % self.etas[bin]
        return bin, label

    def plots(self, jetPt=None, particlePt=None, ratio=None, bin=None, binLabel=""):
        ppt = "%s pT" % self.particleLabel
        jpt = "%sjet pT" % ("c." if self.correctPtAxis else "uc.")
        ratiot = "%sjet pT / %s" % ("c." if self.correctRatio else "uc.", ppt)

        self.book.fill(ratio,
                       "ptRatio1",
                       50, 0.0, 2.0,
                       title=";%s%s" % (ratiot, self.title))

        self.book.fill(ratio,
                       "ptRatio2",
                       75, 0.0, 2.5,
                       title=";%s%s" % (ratiot, self.title))

        self.book.fill((particlePt, jetPt),
                       "ptPt",
                       (20, 20), (0.0, 0.0), (200.0, 200.0),
                       title=";%s;%s%s" % (ppt, jpt, self.title))


        title = ";%s  (%s);%s%s" % (jpt, binLabel, ratiot, self.title)
        name = "rjPt_%d" % bin
        if self.plot2D:
            self.book.fill((jetPt, ratio),
                           name,
                           (20, 20), (0.0, 0.0), (200.0, 2.0),
                           title=title)

        self.book.fill((jetPt, ratio),
                       "%s_prof" % name,
                       20, 0.0, 200.0,
                       title=title)


        #title = ";%s  (%s);%s%s" % (ppt, binLabel, ratiot, self.title)
        #name = "rpPt_%d" % bin
        #self.book.fill((particlePt, ratio),
        #               name,
        #               (20, 20), (0.0, 0.0), (200.0, 2.0),
        #               title=title)
        #self.book.fill((particlePt, ratio),
        #               "%s_prof" % name,
        #               20, 0.0, 200.0,
        #               title=title)


    def uponAcceptance(self, eventVars):
        for particle, jet in eventVars[self.sourceKey].iteritems():
            jetPt = jet.PT
            ratio = jet.PT / particle.PT
            if self.correctPtAxis or  self.correctRatio:
                factor = eventVars["jecFactor"](jetPt, jet.Eta)
            if self.correctPtAxis:
                jetPt *= factor
            if self.correctRatio:
                ratio *= factor

            bin, binLabel = self.bbl(jet.Eta)
            self.plots(jetPt=jetPt,
                       particlePt=particle.PT,
                       ratio=ratio,
                       bin=bin,
                       binLabel=binLabel,
                       )


class massHistogrammer(analysisStep):
    def __init__(self, pts=[]):
        for item in ["pts"]:
            setattr(self, item, eval(item))

    def bbl(self, pt=None):
        bin = bisect.bisect_left(self.pts, pt)
        label = ""
        if bin != 0:
            label += "%3.1f < " % self.pts[bin-1]
        label += "min. b-quark p_{T}"
        if bin != len(self.pts):
            label += " #leq %3.1f" % self.pts[bin]
        return bin, label

    def uponAcceptance(self, eventVars):
        pt = eventVars["bParticles_minPt"]
        m = eventVars["JetsFixedMass_bMatched_Corrected_SumP4"].mass()
        bin, binLabel = self.bbl(pt)
        self.book.fill(m, "mass_pt%d" % bin, 60, 0.0, 300.0, title=";m_{bb} (GeV),       %s;events / bin" % binLabel)


class matchDRHistogrammer(analysisStep):
    def __init__(self, key=""):
        self.key = key

    def uponAcceptance(self, eventVars):
        for particle, jet in eventVars[self.key].iteritems():
            self.book.fill(utils.deltaR(particle, jet), "DeltaR",
                           50, 0.0, 5.0,
                           title=";#DeltaR (%s);matches / bin" % self.key)


class efficiencyHistogrammer(analysisStep):
    def __init__(self, sourceKey="", particleVar="",
                 maxDR=None, minPt=None, maxAbsEta=None, binsMinMax=None):
        for item in ["sourceKey", "particleVar",
                     "maxDR", "minPt", "maxAbsEta", "binsMinMax"]:
            setattr(self, item, eval(item))

        stem = "_".join([sourceKey, self.particleVar])
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


class tauEfficiencyHistogrammer(efficiencyHistogrammer):
    def passFunc(self, particle, jet):
        return jet.TauTag


class matchEfficiencyHistogrammer(efficiencyHistogrammer):
    def passFunc(self, particle, jet):
        return utils.deltaR(particle, jet) < 0.5


class iterHistogrammer(analysisStep):
    def __init__(self, var="", attr="", func=False,
                 labelIndex=False, maxIndex=None, nBins=None, xMin=None, xMax=None):
        for item in ["var", "attr", "func", "labelIndex", "maxIndex"]:
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
                key += " (%s %d)" % (self.var, iObject)
                yTitle = "Events"
            value = getattr(object, self.attr)
            if self.func:
                value = value()
            self.book.fill(value, key, *self.bins, title=";%s;%s / bin" % (key, yTitle))


class modEntry(analysisStep):
    def __init__(self, base=None, value=None):
        for item in ["base", "value"]:
            a = eval(item)
            assert a is not None, a
            setattr(self, item, a)
        self.moreName = "entry % " + "%d == %d" % (self.base, self.value)

    def select(self, eventVars):
        return (eventVars["entry"] % self.base) == self.value
