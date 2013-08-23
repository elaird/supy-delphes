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
        from samples import holder
        return [holder]


    def listOfSamples(self, pars):
        w = calculables.GenWeight()
        return (#supy.samples.specify(names="tt.conf3_0_600", color=r.kBlack, effectiveLumi=0.02/fb) +
                supy.samples.specify(names="tt.conf3_0_600", weights=w, color=r.kBlue, effectiveLumi=0.02/fb) +
                supy.samples.specify(names="tt.conf3_600_1100", weights=w, color=r.kBlue, effectiveLumi=0.2/fb) +
                supy.samples.specify(names="tt.conf3_1100_1700", weights=w, color=r.kBlue, effectiveLumi=1/fb) +
                supy.samples.specify(names="tt.conf3_1700_2500", weights=w, color=r.kBlue, effectiveLumi=10/fb) +
                supy.samples.specify(names="tt.conf3_2500_100000", weights=w, color=r.kBlue, effectiveLumi=10/fb) +
                supy.samples.specify(names="hh_bbtt.conf3", color=r.kRed, effectiveLumi=200/fb) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        org.mergeSamples(targetSpec={"name":"tt_0_6", "color":r.kBlue, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt.conf3_0_600.GenWeight"],
                         )
        org.mergeSamples(targetSpec={"name":"tt_6_11", "color":r.kGreen, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt.conf3_600_1100.GenWeight"],
                         )
        org.mergeSamples(targetSpec={"name":"tt_11_17", "color":r.kCyan, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt.conf3_1100_1700.GenWeight"],
                         )
        org.mergeSamples(targetSpec={"name":"tt_17_25", "color":r.kMagenta, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt.conf3_1700_2500.GenWeight"],
                         )
        org.mergeSamples(targetSpec={"name":"tt_25_1k", "color":r.kOrange, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt.conf3_2500_100000.GenWeight"],
                         )
        org.mergeSamples(targetSpec={"name":"hh_bb#tau#tau", "color":r.kRed, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["hh_bbtt.conf3"],
                         )
        org.mergeSamples(targetSpec={"name":"tt", "color":r.kBlack, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
                         sources=["tt_0_6", "tt_6_11", "tt_11_17", "tt_17_25", "tt_25_1k"], keepSources=True,
                         )

        #org.mergeSamples(targetSpec={"name":"tt*w", "color":r.kBlue, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
        #                 sources=["tt.conf3_0_600.GenWeight"],
        #                 )
        #org.mergeSamples(targetSpec={"name":"tt*1.0", "color":r.kBlack, "markerStyle":1, "lineWidth":2, "goptions":"ehist"},
        #                 sources=["tt.conf3_0_600"],
        #                 )
        org.scale(1.0/fb)
        
        supy.plotter(org,
                     doLog=True,
                     showStatBox=False,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     ).plotAll()
