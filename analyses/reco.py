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
                "keepSources": False,
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
                #supy.steps.histos.mass("Jets_bTagged_FixedMass_SumP4",          50, 0.0, 250.0),
                supy.steps.histos.mass("Jets_bTagged_FixedMass_Corrected_SumP4", 50, 0.0, 250.0),
                supy.steps.filters.mass("Jets_bTagged_FixedMass_Corrected_SumP4", min=100.0, max=140.0),
                supy.steps.histos.mass("Jets_bTagged_FixedMass_Corrected_SumP4", 50, 0.0, 250.0),
                
                #supy.steps.histos.mass("tauTagged_Jets_SumP4",                    50, 0.0, 250.0),
                #supy.steps.histos.mass("Jets_tauTagged_FixedMass_SumP4",          50, 0.0, 250.0),
                supy.steps.histos.mass("Jets_tauTagged_FixedMass_Corrected_SumP4", 25, 0.0, 250.0),
                supy.steps.filters.mass("Jets_tauTagged_FixedMass_Corrected_SumP4", min=75.0, max=125.0),
                supy.steps.histos.mass("Jets_tauTagged_FixedMass_Corrected_SumP4", 50, 0.0, 250.0),

                supy.steps.histos.mass("bbtt_SumP4", 32, 0.0, 800.0),
                supy.steps.filters.mass("bbtt_SumP4", min=350.0),
                
                supy.steps.histos.pt("Jets_bTagged_FixedMass_Corrected_SumP4", 12, 0.0, 300.0),
                supy.steps.filters.pt("Jets_bTagged_FixedMass_Corrected_SumP4", min=100.0),
                
                supy.steps.histos.pt("Jets_tauTagged_FixedMass_Corrected_SumP4", 12, 0.0, 300.0),
                supy.steps.filters.pt("Jets_tauTagged_FixedMass_Corrected_SumP4", min=100.0),

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
                              calculables.Jets("bTagged_Jets_mask1", mFixed=mb, label="bTagged"),
                              calculables.Jets("bTagged_Jets_mask1", mFixed=mb, label="bTagged", correctPt=True),
                              calculables.LvSumP4("Jets_bTagged_FixedMass"),
                              calculables.LvSumP4("Jets_bTagged_FixedMass_Corrected"),

                              # mtt
                              calculables.SumP4("tauTagged_Jets"),
                              calculables.Jets("tauTagged_Jets", mFixed=mtau, label="tauTagged"),
                              calculables.SumP4("Jets_tauTagged"),
                              calculables.Jets("tauTagged_Jets", mFixed=mtau, correctPt=True, label="tauTagged"),
                              calculables.SumP4("Jets_tauTagged_FixedMass_Corrected"),

                              # mbbtt
                              calculables.LvMultiSumP4(label="bbtt", keys=["Jets_bTagged_FixedMass_Corrected_SumP4",
                                                                           "Jets_tauTagged_FixedMass_Corrected_SumP4"]),
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

        out = []
        #out += specify(names="hh_bbtt_%s_10_skim" % c)
        out += specify(names="hh_bbtt_%s_20_skim" % c)
        return out

        names = ["tt_%s_0_6_skim" % c,
                 "tt_%s_6_11_skim" % c,
                 "tt_%s_11_17_skim" % c,
                 "tt_%s_17_25_skim" % c,
                 "tt_%s_25_1k_skim" % c,
                 ]

        if c=="c4_pu140":
            names += ["B_skim",
                      "Bj_0_3_skim",
                      "Bj_3_6_skim",
                      "Bj_6_11_skim",
                      "Bj_11_18_skim",
                      "Bj_18_27_skim",
                      "Bj_27_37_skim",
                      "Bj_37_1k_skim",
                      "tB_0_5_skim",
                      "tB_5_9_skim",
                      "tB_9_15_skim",
                      "tB_15_22_skim",
                      "tB_22_1k_skim",
                      "ttB_0_9_skim",
                      "ttB_9_16_skim",
                      "ttB_16_25_skim",
                      "ttB_25_1k_skim",
                      "H_0_3_skim",
                      "H_3_8_skim",
                      "H_8_15_skim",
                      "H_15_1k_skim",
                      "Bjj_0_7_skim",
                      "Bjj_7_14_skim",
                      "Bjj_14_23_skim",
                      "Bjj_23_34_skim",
                      "LL_0_1_skim",
                      "LL_1_2_skim",
                      "LL_2_5_skim",
                      "LL_5_9_skim",
                      "LL_9_14_skim",
                      "LL_14_1k_skim",
                      "LLB_0_4_skim",
                      "LLB_4_9_skim",
                      "LLB_9_1k_skim",
                      "tj_0_5_skim",
                      "tj_5_10_skim",
                      "tj_10_16_skim",
                      "tj_16_24_skim",
                      "tj_24_1k_skim",
                      ]

        names += ["BB_%s_0_3_skim" % c,
                  "BB_%s_3_7_skim" % c,
                  "BB_%s_7_13_skim" % c,
                  "BB_%s_13_21_skim" % c,
                  "BB_%s_21_1k_skim" % c,
                  "BBB_%s_0_6_skim" % c,
                  "BBB_%s_6_13_skim" % c,
                  "BBB_%s_13_1k_skim" % c,
                  ]

        for name in names:
            out += specify(names=name, weights=w, effectiveLumi=el)

        return out


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        supy.utils.printSkimResults(org)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        c = pars["tag"]
        org.mergeSamples(targetSpec=gopts("hh_bb#tau#tau", r.kRed), sources=["hh_bbtt_%s_20_skim" % c])

        keep = pars["keepSources"]

        if keep:
            org.mergeSamples(targetSpec=gopts("tt_0_6",   r.kBlue),    sources=["tt_%s_0_6_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("tt_6_11",  r.kGreen),   sources=["tt_%s_6_11_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("tt_11_17", r.kCyan),    sources=["tt_%s_11_17_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("tt_17_25", r.kMagenta), sources=["tt_%s_17_25_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("tt_25_1k", r.kOrange),  sources=["tt_%s_25_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("tt", r.kBlue), allWithPrefix="tt_", keepSources=keep)

        bj = ["B_skim", "Bj_0_3_skim","Bj_3_6_skim", "Bj_6_11_skim", "Bj_11_18_skim",
               "Bj_18_27_skim", "Bj_27_37_skim", "Bj_37_1k_skim"]
        org.mergeSamples(targetSpec=gopts("Bj", r.kGreen), sources=[x+".GenWeight" for x in bj], keepSources=keep)

        tb = ["tB_0_5_skim", "tB_5_9_skim", "tB_9_15_skim", "tB_15_22_skim", "tB_22_1k_skim"]
        org.mergeSamples(targetSpec=gopts("tB", r.kCyan), sources=[x+".GenWeight" for x in tb], keepSources=keep)

        ttb = ["ttB_0_9_skim", "ttB_9_16_skim", "ttB_16_25_skim", "ttB_25_1k_skim"]
        org.mergeSamples(targetSpec=gopts("ttB", r.kBlue-8), sources=[x+".GenWeight" for x in ttb], keepSources=keep)

        h = ["H_0_3_skim", "H_3_8_skim", "H_8_15_skim", "H_15_1k_skim"]
        org.mergeSamples(targetSpec=gopts("H", r.kOrange-3), sources=[x+".GenWeight" for x in h], keepSources=keep)

        if keep:
            org.mergeSamples(targetSpec=gopts("BB_0_3",   r.kBlue),    sources=["BB_%s_0_3_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BB_3_7",  r.kGreen),    sources=["BB_%s_3_7_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BB_7_13", r.kCyan),     sources=["BB_%s_7_13_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BB_13_21", r.kMagenta), sources=["BB_%s_13_21_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BB_21_1k", r.kOrange),  sources=["BB_%s_21_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BB", r.kBlack), allWithPrefix="BB_", keepSources=keep)

        if keep:
            org.mergeSamples(targetSpec=gopts("BBB_0_6",  r.kBlue),    sources=["BBB_%s_0_6_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BBB_6_13", r.kGreen),   sources=["BBB_%s_6_13_skim.GenWeight" % c])
            org.mergeSamples(targetSpec=gopts("BBB_13_1k", r.kCyan),   sources=["BBB_%s_13_1k_skim.GenWeight" % c])
        org.mergeSamples(targetSpec=gopts("BBB", r.kBlack), allWithPrefix="BBB_", keepSources=keep)

        bjj = ["Bjj_0_7_skim", "Bjj_7_14_skim", "Bjj_14_23_skim", "Bjj_23_34_skim"]
        org.mergeSamples(targetSpec=gopts("Bjj", r.kYellow), sources=[x+".GenWeight" for x in bjj], keepSources=keep)

        ll = ["LL_0_1_skim", "LL_1_2_skim", "LL_2_5_skim", "LL_5_9_skim", "LL_9_14_skim", "LL_14_1k_skim"]
        org.mergeSamples(targetSpec=gopts("LL", r.kBlack), sources=[x+".GenWeight" for x in ll], keepSources=keep)

        llb = ["LLB_0_4_skim", "LLB_4_9_skim", "LLB_9_1k_skim"]
        org.mergeSamples(targetSpec=gopts("LLB", r.kBlack), sources=[x+".GenWeight" for x in llb], keepSources=keep)

        tj = ["tj_0_5_skim", "tj_5_10_skim", "tj_10_16_skim", "tj_16_24_skim", "tj_24_1k_skim"]
        org.mergeSamples(targetSpec=gopts("tj", r.kPink), sources=[x+".GenWeight" for x in tj], keepSources=keep)

        others = ["BB", "BBB", "Bjj", "LL", "LLB", "tj"]
        org.mergeSamples(targetSpec=gopts("others", r.kMagenta), sources=others, keepSources=False)

        sm = ["tt", "Bj", "tB", "ttB", "H", "others"]
        org.mergeSamples(targetSpec=gopts("SM", r.kBlack), sources=sm, keepSources=True)

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
                     samplesForRatios=("hh_bb#tau#tau", "SM"),
                     sampleLabelsForRatios=("hh", "SM"),
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
