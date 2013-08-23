import supy, calculables, steps
import ROOT as r
from units import pb, fb

class example(supy.analysis):
    def weightPlots(self):
        return [supy.steps.filters.label("weightPlots"),
                supy.steps.histos.value("one", 1, 0.0, 2.0, xtitle="1.0 (filled with weight 1.0)", w="one"),
                supy.steps.histos.value("one", 1, 0.0, 2.0, xtitle="1.0 (filled with event weight)"),
                supy.steps.histos.value("weight", 100, 0.0, 5.0, xtitle="event weight (filled with weight 1.0)", w="one"),
                supy.steps.histos.value("HT", 100, 0.0, 5000.0, xtitle="Scalar HT"),
                ]


    def genParticlePlots(self):
        return [supy.steps.filters.label("genParticlePlots"),
                supy.steps.histos.multiplicity("Particle", max=40),
                supy.steps.histos.multiplicity("nuParticles"),
                supy.steps.histos.multiplicity("tParticles"),
                supy.steps.histos.multiplicity("hParticles"),
                supy.steps.histos.multiplicity("bParticles"),
                supy.steps.histos.multiplicity("cParticles"),
                #supy.steps.histos.multiplicity("muParticles"),
                #supy.steps.histos.multiplicity("eParticles"),
                supy.steps.histos.multiplicity("tauParticles"),
                ]


    def btag(self, mask=0, p=""):
        return [#supy.steps.histos.multiplicity("bTaggedJets"),
                #steps.jetHistogrammer(var="BTag", nBins=5, xMin=-0.5, xMax=4.5)+
                #supy.steps.histos.multiplicity("JetMatchedTo_%sParticles" % p),
                steps.matchHistogrammer("JetMatchedTo_%sParticles" % p),
                steps.matchHistogrammer("JetMatchedTo_%sParticles" % p, maxDR=0.3),
                steps.efficiencyHistogrammer("JetMatchedTo_%sParticles" % p,
                                             particleVar="PT",
                                             jetFlag="BTag", mask=mask,
                                             maxDR=0.3, minPt=20.0, maxAbsEta=2.4,
                                             binsMinMax=(20, 0.0, 200.0)),
                steps.efficiencyHistogrammer("JetMatchedTo_%sParticles" % p,
                                             particleVar="Eta",
                                             jetFlag="BTag", mask=mask,
                                             maxDR=0.3, minPt=50.0, maxAbsEta=None,
                                             binsMinMax=(20, -5.0, 5.0)),
                ]


    def listOfSteps(self, pars):
        return ([supy.steps.printer.progressPrinter()] +
                self.weightPlots() +
                #self.genParticlePlots() +
                self.btag(mask=0x1, p="b") +
                self.btag(mask=0x1, p="c") +
                self.btag(mask=0x2, p="b") +
                self.btag(mask=0x2, p="c") +
                #self.btag(mask=bMask, p="uds") +
                #self.btag("g") +
                #self.btag("tau") +
                [])


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [supy.calculables.other.fixedValue("one", 1.0),
                              calculables.Particles(pids=[-3, -2, -1, 1, 2, 3], label="uds"),
                              calculables.Particles(pids=[-4, 4], label="c"),
                              calculables.Particles(pids=[-5, 5], label="b"),
                              calculables.Particles(pids=[-6, 6], label="t"),
                              calculables.Particles(pids=[-11, 11], label="e"),
                              calculables.Particles(pids=[-13, 13], label="mu"),
                              calculables.Particles(pids=[-15, 15], label="tau"),
                              calculables.Particles(pids=[-16, -14, -12, 12, 14, 16], label="nu"),
                              calculables.Particles(pids=[21], label="g"),
                              calculables.Particles(pids=[25], label="h"),
                              #calculables.JetMatchedTo(sourceKey="udsParticles"),
                              calculables.JetMatchedTo(sourceKey="cParticles"),
                              calculables.JetMatchedTo(sourceKey="bParticles"),
                              #calculables.JetMatchedTo(sourceKey="tauParticles"),
                              #calculables.JetMatchedTo(sourceKey="gParticles"),
                              calculables.bTaggedJets(),
                              calculables.HT(),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import conf3
        return [conf3]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()
        return (specify(names="tt_0_600", weights=w, color=r.kBlack, effectiveLumi=0.02/fb) +
                specify(names="tt_600_1100", weights=w, color=r.kBlack, effectiveLumi=0.2/fb) +
                specify(names="tt_1100_1700", weights=w, color=r.kBlack, effectiveLumi=1/fb) +
                specify(names="tt_1700_2500", weights=w, color=r.kBlack, effectiveLumi=10/fb) +
                specify(names="tt_2500_100000", weights=w, color=r.kBlack, effectiveLumi=10/fb) +

                specify(names="BB_0_3",   weights=w, color=r.kBlue, effectiveLumi=0.02/fb) +
                specify(names="BB_3_7",   weights=w, color=r.kBlue, effectiveLumi=0.2/fb) +
                specify(names="BB_7_13",  weights=w, color=r.kBlue, effectiveLumi=2/fb) +
                specify(names="BB_13_21", weights=w, color=r.kBlue, effectiveLumi=2/fb) +
                #specify(names="BB_21_1k", weights=w, color=r.kBlue, effectiveLumi=2/fb) +

                specify(names="BBB_0_6",   weights=w, color=r.kGreen, effectiveLumi=20/fb) +
                specify(names="BBB_6_13",  weights=w, color=r.kGreen, effectiveLumi=20/fb) +
                specify(names="BBB_13_1k", weights=w, color=r.kGreen, effectiveLumi=200/fb) +

                specify(names="hh_bbtt",              color=r.kRed, effectiveLumi=200/fb) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        #org.mergeSamples(targetSpec=gopts("tt_0_6",   r.kBlue),    sources=["tt_0_6.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_6_11",  r.kGreen),   sources=["tt_6_11.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_11_17", r.kCyan),    sources=["tt_11_17.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_17_25", r.kMagenta), sources=["tt_17_25.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_25_1k", r.kOrange),  sources=["tt_25_1k.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt", r.kBlack), allWithPrefix="tt_")

        #org.mergeSamples(targetSpec=gopts("BB_0_3",   r.kGreen),   sources=["BB_0_3.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_3_7",   r.kCyan),    sources=["BB_3_7.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_7_13",  r.kMagenta), sources=["BB_7_13.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_13_21", r.kOrange),  sources=["BB_13_21.GenWeight"])
        org.mergeSamples(targetSpec=gopts("BB", r.kBlue), allWithPrefix="BB_")

        #org.mergeSamples(targetSpec=gopts("BBB_0_6",   r.kBlue),    sources=["BBB_0_6.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BBB_6_13",  r.kCyan),    sources=["BBB_6_13.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BBB_13_1k", r.kMagenta), sources=["BBB_13_1k.GenWeight"])
        org.mergeSamples(targetSpec=gopts("BBB", r.kGreen), allWithPrefix="BBB_")

        org.mergeSamples(targetSpec=gopts("hh_bb#tau#tau", r.kRed), sources=["hh_bbtt"])

        #org.mergeSamples(targetSpec=gopts("tt*w", r.kBlue), sources=["tt0_600.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt*1.0", r.kBlack) sources=["tt0_600"])

        org.scale(1.0/fb)
        
        supy.plotter(org,
                     doLog=True,
                     showStatBox=False,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     ).plotAll()
