import math
import supy
import calculables
import steps
from units import pb, fb
import ROOT as r

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
                #supy.steps.histos.multiplicity("cParticles"),
                #supy.steps.histos.multiplicity("muParticles"),
                #supy.steps.histos.multiplicity("eParticles"),
                supy.steps.histos.multiplicity("tauParticles"),
                supy.steps.histos.multiplicity("btauParticles"),
                ]


    def btag(self, mask=0, p=""):
        return [#steps.iterHistogrammer(var="Jet", attr="BTag", labelIndex=False, nBins=5, xMin=-0.5, xMax=4.5),
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


    def ggHHPlots(self):
        return [supy.steps.histos.pt("bParticlesSumP4", 50, 0.0, 500.0),
                supy.steps.histos.pt("tauParticlesSumP4", 50, 0.0, 500.0),
                supy.steps.histos.eta("bParticlesSumP4", 20, -8.0, 8.0),
                supy.steps.histos.eta("tauParticlesSumP4", 20, -8.0, 8.0),
                supy.steps.histos.mass("btauParticlesSumP4", 40, 200.0, 1000.0),
                supy.steps.histos.Rapidity("btauParticlesSumP4", 20, -4.0, 4.0),
                ]

    def particleAcceptancePlots(self):
        return [steps.iterHistogrammer(var="bParticles", attr="PT", nBins=50, xMin=0.0, xMax=200.0),
                steps.iterHistogrammer(var="bParticles", attr="Eta", nBins=50, xMin=-5.0, xMax=5.0),
                steps.iterHistogrammer(var="tauParticles", attr="PT", nBins=50, xMin=0.0, xMax=200.0),
                steps.iterHistogrammer(var="tauParticles", attr="Eta", nBins=50, xMin=-5.0, xMax=5.0),
                steps.iterHistogrammer(var="btauParticles", attr="PT", nBins=50, xMin=0.0, xMax=200.0),
                steps.iterHistogrammer(var="btauParticles", attr="Eta", nBins=50, xMin=-5.0, xMax=5.0),
                ]

    def genSelection(self):
        return [supy.steps.filters.multiplicity("bParticles", min=2),
                supy.steps.filters.multiplicity("tauParticles", min=2),

                #steps.modEntry(base=4, value=0),
                steps.modEntry(base=8, value=0),
                supy.steps.filters.multiplicity("tauKineParticles", min=2, max=2),

                supy.steps.histos.mass("tauParticlesSumP4", 60, 0.0, 300.0),
                supy.steps.filters.mass("tauParticlesSumP4", min=100., max=150.),

                supy.steps.filters.multiplicity("bKineParticles", min=2, max=2),
                supy.steps.histos.mass("bParticlesSumP4", 60, 0.0, 300.0),
                supy.steps.filters.mass("bParticlesSumP4", min=112.5, max=137.5),

                supy.steps.histos.mass("btauParticlesSumP4", 40, 200.0, 1000.0),
                supy.steps.filters.mass("btauParticlesSumP4", min=350.0),

                supy.steps.histos.pt("bParticlesSumP4", 50, 0.0, 500.0),
                supy.steps.filters.pt("bParticlesSumP4", min=100.0),

                supy.steps.histos.pt("tauParticlesSumP4", 50, 0.0, 500.0),
                supy.steps.filters.pt("tauParticlesSumP4", min=100.0),

                ]

    def listOfSteps(self, pars):
        return ([supy.steps.printer.progressPrinter()] +
                self.weightPlots() +
                self.genParticlePlots() +
                self.genSelection() +
                []+
                #self.particleAcceptancePlots() +
                self.ggHHPlots() +
                #self.btag(mask=0x1, p="b") +
                #self.btag(mask=0x1, p="c") +
                #self.btag(mask=0x2, p="b") +
                #self.btag(mask=0x2, p="c") +
                #self.btag(mask=bMask, p="uds") +
                #self.btag("g") +
                #self.btag("tau") +
                #supy.steps.histos.multiplicity("bTaggedJets"),
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

                              calculables.Particles(pids=[-15, -5, 5, 15], label="btau"),

                              calculables.Particles(pids=[-5, 5], label="bKine", ptMin=30.0, absEtaMax=2.4),
                              calculables.Particles(pids=[-15, 15], label="tauKine", ptMin=30.0, absEtaMax=2.4),
                              calculables.Particles(pids=[-15, -5, 5, 15], label="btauKine", ptMin=30.0, absEtaMax=2.4),

                              #calculables.JetMatchedTo(sourceKey="udsParticles"),
                              calculables.JetMatchedTo(sourceKey="cParticles"),
                              calculables.JetMatchedTo(sourceKey="bParticles"),
                              #calculables.JetMatchedTo(sourceKey="tauParticles"),
                              #calculables.JetMatchedTo(sourceKey="gParticles"),
                              calculables.bTaggedJets(),
                              calculables.HT(),
                              calculables.SumP4("bParticles"),
                              calculables.SumP4("tauParticles"),
                              calculables.SumP4("btauParticles"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import conf3
        return [conf3]


    def listOfSamples(self, pars):
        from supy.samples import specify
        #w = supy.calculables.other.fixedValue("another", 1.0)
        w = calculables.GenWeight()
        n = 100000
        return (specify(names="tt_0_600", weights=w, color=r.kBlack, nEventsMax=n) +
                specify(names="tt_600_1100", weights=w, color=r.kBlack, nEventsMax=n) +
                specify(names="tt_1100_1700", weights=w, color=r.kBlack, effectiveLumi=20/fb) +
                specify(names="tt_1700_2500", weights=w, color=r.kBlack, effectiveLumi=20/fb) +
                specify(names="tt_2500_100000", weights=w, color=r.kBlack, effectiveLumi=20/fb) +

                #specify(names="BB_0_3",   weights=w, color=r.kBlue, nEventsMax=n) +
                #specify(names="BB_3_7",   weights=w, color=r.kBlue, nEventsMax=n) +
                #specify(names="BB_7_13",  weights=w, color=r.kBlue, effectiveLumi=20/fb) +
                #specify(names="BB_13_21", weights=w, color=r.kBlue, effectiveLumi=20/fb) +
                ##specify(names="BB_21_1k", weights=w, color=r.kBlue, effectiveLumi=2/fb) +

                specify(names="BBB_0_6",   weights=w, color=r.kGreen, nEventsMax=n) +
                specify(names="BBB_6_13",  weights=w, color=r.kGreen, effectiveLumi=200/fb) +
                specify(names="BBB_13_1k", weights=w, color=r.kGreen, effectiveLumi=200/fb) +

                specify(names="hh_bbtt",              color=r.kRed, effectiveLumi=20000/fb) +
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
        #org.scale(toPdf=True)

        supy.plotter(org,
                     doLog=True,
                     showStatBox=False,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],
                     latexYieldTable=True,
                     samplesForRatios=("hh_bb#tau#tau", "tt"),
                     sampleLabelsForRatios=("hh", "tt"),
                     foms=[{"value": lambda x, y: x/y,
                            "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y)**2),
                            "label": lambda x, y:"%s/%s" % (x, y),
                            },
                           #{"value": lambda x,y: x/(y**0.5),
                           # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y/2.)**2),
                           # "label": lambda x,y: "%s/sqrt(%s)" % (x, y),
                           # },
                           #{"value": lambda x, y: x/(((a*y)**2+y)**0.5),
                           # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 +\
                           #                                              (yUnc*(2*a*a*y+1)/(a*a*y*y+y)/2.)**2\
                           #                                              ),
                           # "label": lambda x,y: "%s/r(%s+%s^2/%3.0f)" % (x, y, y, 1/a/a),
                           # },
                           ],
                     ).plotAll()
