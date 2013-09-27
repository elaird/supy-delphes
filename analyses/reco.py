import math
import supy
import calculables
import steps
from units import fb, mb, mtau
import ROOT as r

class reco(supy.analysis):
    def parameters(self):
        return {"jec": self.vary({#"c0_pu0": ("c0", "b_v3"),
                                  #"c4_pu140": ("c41", "b_v2_10"),
                                  "c4_pu140": ("c4", "one"),
                                  }),
                }

    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                supy.steps.histos.value("HT", 50, 0.0, 2500.0),
                supy.steps.histos.multiplicity("Jets"),
                supy.steps.filters.multiplicity("Jets", min=4),
                supy.steps.histos.multiplicity("bTagged_Jets_mask1"),
                supy.steps.filters.multiplicity("bTagged_Jets_mask1", min=2, max=2),
                supy.steps.histos.multiplicity("tauTagged_Jets"),
                supy.steps.filters.multiplicity("tauTagged_Jets", min=2, max=2),
                supy.steps.histos.value("HT", 50, 0.0, 2500.0),

                supy.steps.histos.multiplicity("tauTagged_bTagged_Jets_mask1"),
                supy.steps.filters.multiplicity("tauTagged_bTagged_Jets_mask1", max=0),

                #supy.steps.histos.mass("bTagged_Jets_mask1_SumP4",              50, 0.0, 250.0),
                #supy.steps.histos.mass("JetsFixedMass_bTagged_SumP4",           50, 0.0, 250.0),
                supy.steps.histos.mass("JetsFixedMass_bTagged_Corrected_SumP4", 50, 0.0, 250.0),
                supy.steps.filters.mass("JetsFixedMass_bTagged_Corrected_SumP4", min=100.0, max=140.0),
                supy.steps.histos.mass("JetsFixedMass_bTagged_Corrected_SumP4", 50, 0.0, 250.0),
                
                #supy.steps.histos.mass("tauTagged_Jets_SumP4",                    50, 0.0, 250.0),
                #supy.steps.histos.mass("JetsFixedMass_tauTagged_SumP4",           50, 0.0, 250.0),
                supy.steps.histos.mass("JetsFixedMass_tauTagged_Corrected_SumP4", 25, 0.0, 250.0),
                supy.steps.filters.mass("JetsFixedMass_tauTagged_Corrected_SumP4", min=75.0, max=125.0),
                supy.steps.histos.mass("JetsFixedMass_tauTagged_Corrected_SumP4", 50, 0.0, 250.0),

                supy.steps.histos.mass("bbtt_LvSumP4", 32, 0.0, 800.0),
                supy.steps.filters.mass("bbtt_LvSumP4", min=350.0),
                
                supy.steps.histos.pt("JetsFixedMass_bTagged_Corrected_SumP4", 12, 0.0, 300.0),
                supy.steps.filters.pt("JetsFixedMass_bTagged_Corrected_SumP4", min=100.0),
                
                supy.steps.histos.pt("JetsFixedMass_tauTagged_Corrected_SumP4", 12, 0.0, 300.0),
                supy.steps.filters.pt("JetsFixedMass_tauTagged_Corrected_SumP4", min=100.0),

                supy.steps.histos.multiplicity("bParticles"),
                supy.steps.histos.multiplicity("tauParticles"),
                supy.steps.histos.value("HT", 50, 0.0, 2500.0),
                supy.steps.histos.value("DeltaR_bTagged_Jets_mask1", 30, 0.0, 3.0),
                supy.steps.histos.value("DeltaR_tauTagged_Jets", 30, 0.0, 3.0),
                #steps.displayer(),
                #supy.steps.filters.value("DeltaR_tauTagged_Jets", min=0.7),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.jecFactor(*pars["jec"]),
                              calculables.Filtered(pids=[-5, 5], label="b", key="Particle", status=[3]),
                              calculables.Filtered(pids=[-15, 15], label="tau", key="Particle", status=[3]),
                              calculables.Filtered(label="", ptMin=20.0, absEtaMax=2.4, key="Jet"),
                              calculables.bTagged("Jets", mask=0x1),
                              calculables.tauTagged("Jets"),
                              calculables.tauTagged("bTagged_Jets_mask1"),
                              calculables.Duplicates(key1="bTagged_Jets_mask1", key2="tauTagged_Jets", minDR=0.2),
                              calculables.DeltaR("bTagged_Jets_mask1"),
                              calculables.DeltaR("tauTagged_Jets"),

                              # mbb
                              calculables.SumP4("bTagged_Jets_mask1"),
                              calculables.JetsFixedMass("bTagged_Jets_mask1", m=mb, label="bTagged"),
                              calculables.SumP4("JetsFixedMass_bTagged"),
                              calculables.JetsFixedMass("bTagged_Jets_mask1", m=mb, correctPt=True, label="bTagged"),
                              calculables.SumP4("JetsFixedMass_bTagged_Corrected"),

                              # mtt
                              calculables.SumP4("tauTagged_Jets"),
                              calculables.JetsFixedMass("tauTagged_Jets", m=mtau, label="tauTagged"),
                              calculables.SumP4("JetsFixedMass_tauTagged"),
                              calculables.JetsFixedMass("tauTagged_Jets", m=mtau, correctPt=True, label="tauTagged"),
                              calculables.SumP4("JetsFixedMass_tauTagged_Corrected"),

                              # mbbtt
                              calculables.LvSumP4(label="bbtt", keys=["JetsFixedMass_bTagged_Corrected_SumP4",
                                                                      "JetsFixedMass_tauTagged_Corrected_SumP4"]),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import skims
        return [skims]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        c = pars["tag"]
        el = 1e5/fb
        return (##specify(names="hh_bbtt_%s_10_skim" % c) +
                specify(names="hh_bbtt_%s_20_skim" % c) +
                
                specify(names="tt_%s_0_6_skim" % c,   weights=w, effectiveLumi=el) +
                specify(names="tt_%s_6_11_skim" % c,  weights=w, effectiveLumi=el) +
                specify(names="tt_%s_11_17_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="tt_%s_17_25_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="tt_%s_25_1k_skim" % c, weights=w, effectiveLumi=el) +

                specify(names="BB_%s_0_3_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BB_%s_3_7_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BB_%s_7_13_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BB_%s_13_21_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BB_%s_21_1k_skim" % c, weights=w, effectiveLumi=el) +

                specify(names="BBB_%s_0_6_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BBB_%s_6_13_skim" % c, weights=w, effectiveLumi=el) +
                specify(names="BBB_%s_13_1k_skim" % c, weights=w, effectiveLumi=el) +

                #specify(names="tt_0_6",   weights=w) + #, nEventsMax=n) +
                #specify(names="tt_6_11",  weights=w) + #, nEventsMax=n) +
                #specify(names="tt_11_17", weights=w) + #, effectiveLumi=40/fb) +
                #specify(names="tt_17_25", weights=w) + #, nEventsMax=n) + #effectiveLumi=20/fb) +
                #specify(names="tt_25_1k", weights=w) + #, nEventsMax=n) + #effectiveLumi=200/fb) +
                #specify(names="hh_bbtt_c4_10", effectiveLumi=el) +
                #specify(names="hh_bbtt_c4_20", effectiveLumi=el) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        supy.utils.printSkimResults(org)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        #org.mergeSamples(targetSpec=gopts("tt_0_6",   r.kBlue),    sources=["tt_0_6.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_6_11",  r.kGreen),   sources=["tt_6_11.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_11_17", r.kCyan),    sources=["tt_11_17.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_17_25", r.kMagenta), sources=["tt_17_25.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("tt_25_1k", r.kOrange),  sources=["tt_25_1k.GenWeight"])

        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_10", r.kRed), sources=["hh_bbtt_c4_10"])
        #org.mergeSamples(targetSpec=gopts("hh_bbtt", r.kRed), sources=["hh_bbtt_c4_20"])

        keep = False
        c = pars["tag"]
        org.mergeSamples(targetSpec=gopts("tt_0_6",   r.kBlue),    sources=["tt_%s_0_6_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt_6_11",  r.kGreen),   sources=["tt_%s_6_11_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt_11_17", r.kCyan),    sources=["tt_%s_11_17_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt_17_25", r.kMagenta), sources=["tt_%s_17_25_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt_25_1k", r.kOrange),  sources=["tt_%s_25_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt", r.kBlack), allWithPrefix="tt_", keepSources=keep)

        org.mergeSamples(targetSpec=gopts("BB_0_3",   r.kBlue),    sources=["BB_%s_0_3_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB_3_7",  r.kGreen),    sources=["BB_%s_3_7_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB_7_13", r.kCyan),     sources=["BB_%s_7_13_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB_13_21", r.kMagenta), sources=["BB_%s_13_21_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB_21_1k", r.kOrange),  sources=["BB_%s_21_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB", r.kBlue), allWithPrefix="BB_", keepSources=keep)

        org.mergeSamples(targetSpec=gopts("BBB_0_6",  r.kBlue),    sources=["BBB_%s_0_6_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BBB_6_13", r.kGreen),   sources=["BBB_%s_6_13_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BBB_13_1k", r.kCyan),   sources=["BBB_%s_13_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BBB", r.kCyan), allWithPrefix="BBB_", keepSources=keep)
        
        org.mergeSamples(targetSpec=gopts("hh_bb#tau#tau", r.kRed), sources=["hh_bbtt_%s_20_skim" % c])
        
        org.scale(3.e3/fb)
        #org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     doLog=True,
                     pegMinimum=0.1,
                     #optStat=1100,
                     optStat=1111,
                     #fitFunc=self.profFit,
                     showStatBox=False,
                     latexYieldTable=False,
                     samplesForRatios=("hh_bb#tau#tau", "tt"),
                     sampleLabelsForRatios=("hh", "tt"),
                     foms=[{"value": lambda x, y: x/y,
                            "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y)**2),
                            "label": lambda x, y:"%s/%s" % (x, y),
                            },
                     #      #{"value": lambda x,y: x/(y**0.5),
                     #      # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y/2.)**2),
                     #      # "label": lambda x,y: "%s/sqrt(%s)" % (x, y),
                     #      # },
                           ],
                     ).plotAll()
