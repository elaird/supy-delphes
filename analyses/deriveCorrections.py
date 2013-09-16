import math
import supy
import calculables
import steps
from units import fb, mb, mtau
import ROOT as r

class deriveCorrections(supy.analysis):
    def listOfSteps(self, _):
        p = "b"
        return [supy.steps.printer.progressPrinter(),
                ##supy.steps.histos.value("rho", 30, 0.0, 150.0),
                #supy.steps.histos.value("HT", 300, 0.0, 3000.0),
                supy.steps.filters.multiplicity("%sParticles" % p, min=2, max=2),
                supy.steps.histos.mass("%sParticles_SumP4" % p, 50, 0.0, 250.0),
                steps.iterHistogrammer(var="bParticles", attr="PT", func=False, nBins=30, xMin=0.0, xMax=300.0),

                steps.matchDRHistogrammer("JetMatchedTo_%sParticles_noMaxDR" % p),

                supy.steps.histos.multiplicity("JetMatchedTo_%sParticles" % p),
                supy.steps.filters.multiplicity("JetMatchedTo_%sParticles" % p, max=2),
                #supy.steps.histos.value("DeltaR_JetMatchedTo_%sParticles.values" % p, 100, 0.0, 10.0),
                #supy.steps.filters.value("DeltaR_JetMatchedTo_%sParticles.values" % p, min=0.2),

                #supy.steps.histos.mass("JetMatchedTo_%sParticles.values_SumP4" % p,   50, 0.0, 250.0),
                #supy.steps.histos.mass("JetsFixedMass_%sMatched_SumP4" % p,           50, 0.0, 250.0),
                #supy.steps.histos.mass("JetsFixedMass_%sMatched_Corrected_SumP4" % p, 50, 0.0, 250.0),

                #steps.iterHistogrammer(var="JetsFixedMass_%sMatched" % p, attr="pt", func=True,
                #                       labelIndex=False, nBins=20, xMin=0.0, xMax=200.0),

                supy.steps.filters.label("uncorrected"),
                steps.matchDRHistogrammer("JetMatchedTo_%sParticles" % p),
                steps.matchPtHistogrammer("JetMatchedTo_%sParticles" % p,
                                          #etas=[0.6, 1.2, 1.8, 2.4, 3.0, 4.0],
                                          etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                                          correctPtAxis=False,
                                          correctRatio=False,
                                          ),
                #supy.steps.filters.label("corrected"),
                #steps.matchPtHistogrammer("JetMatchedTo_%sParticles" % p,
                #                          #etas=[0.6, 1.2, 1.8, 2.4, 3.0, 4.0],
                #                          etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                #                          correctPtAxis=False,
                #                          correctRatio=True,
                #                          ),
                #supy.steps.filters.label("corrected2"),
                #steps.matchPtHistogrammer("JetMatchedTo_%sParticles" % p,
                #                          #etas=[0.6, 1.2, 1.8, 2.4, 3.0, 4.0],
                #                          etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                #                          correctPtAxis=True,
                #                          correctRatio=True,
                #                          ),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              #calculables.jecFactor("conf0_b_v3"),
                              calculables.Filtered(pids=[23], label="Z", key="Particle", status=[3]),
                              calculables.Filtered(pids=[25], label="h", key="Particle", status=[3]),
                              ]
        listOfCalculables += [# b
                              calculables.Filtered(pids=[-5, 5], label="b", status=[3], key="Particle", ptMin=0.0),
                              calculables.JetMatchedTo(sourceKey="bParticles"),
                              calculables.JetMatchedTo(sourceKey="bParticles", maxDR=0.3),
                              calculables.SumP4("bParticles"),

                              supy.calculables.other.values("JetMatchedTo_bParticles"),
                              calculables.DeltaR("JetMatchedTo_bParticles.values"),
                              # mass 1
                              calculables.SumP4("JetMatchedTo_bParticles.values"),
                              # mass 2
                              calculables.JetsFixedMass("JetMatchedTo_bParticles.values", m=mb, label="bMatched"),
                              calculables.SumP4("JetsFixedMass_bMatched"),
                              calculables.JetsFixedMass("JetMatchedTo_bParticles.values", m=mb, correctPt=True, label="bMatched"),
                              calculables.SumP4("JetsFixedMass_bMatched_Corrected"),
                              ]

        listOfCalculables += [# tau
                              calculables.Filtered(pids=[-15, 15], label="tau", key="Particle", status=[3]),
                              calculables.JetMatchedTo(sourceKey="tauParticles"),
                              calculables.JetMatchedTo(sourceKey="tauParticles", maxDR=0.3),
                              calculables.SumP4("tauParticles"),

                              supy.calculables.other.values("JetMatchedTo_tauParticles"),
                              calculables.DeltaR("JetMatchedTo_tauParticles.values"),
                              # mass 1
                              calculables.SumP4("JetMatchedTo_tauParticles.values"),
                              # mass 2
                              calculables.JetsFixedMass("JetMatchedTo_tauParticles.values",
                                                        m=mtau, label="tauMatched"),
                              calculables.SumP4("JetsFixedMass_tauMatched"),
                              calculables.JetsFixedMass("JetMatchedTo_tauParticles.values",
                                                        m=mtau, correctPt=True, label="tauMatched"),
                              calculables.SumP4("JetsFixedMass_tauMatched_Corrected"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        #n = 10000
        return (#specify(names="H_0_3_c0_pu0",    weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c0_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c3_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c4_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +

                ##specify(names="BB_0_3",   weights=w, color=r.kBlue, nEventsMax=n) +
                ##specify(names="BB_3_7",   weights=w, color=r.kBlue, nEventsMax=n) +
                ##specify(names="BB_7_13",  weights=w, color=r.kBlue, nEventsMax=n) +
                ##specify(names="BB_13_21", weights=w, color=r.kBlue, nEventsMax=n) +
                ###specify(names="BB_21_1k", weights=w, color=r.kBlue, effectiveLumi=2/fb) +

                #specify(names="QCD_c4_pu140_Pt_0p3_4", nFilesMax=1) +
                #specify(names="hh_bbtt_c0_pu0_20", color=r.kRed) +
                #specify(names="hh_bbtt_c3_pu140", color=r.kRed) +
                #specify(names="hh_bbtt_c4_pu140_10", color=r.kRed) +
                specify(names="hh_bbtt_c4_pu140_20", color=r.kRed) +
                []
                )


    def dumpFitResults(self, fileName=""):
        if not hasattr(self, "fitText1"):
            print "No fit results to dump."
            return
        lines = ["import ROOT as r", "", ""]
        lines += self.fitText1
        lines += ["", "", "def f(eta):"]
        lines += ["    "+s for s in self.fitText2]
        lines += [""]

        f = open(fileName, "w")
        f.write("\n".join(lines))
        f.close()


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        #org.mergeSamples(targetSpec=gopts("BB_0_3",   r.kGreen),   sources=["BB_0_3.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_3_7",   r.kCyan),    sources=["BB_3_7.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_7_13",  r.kMagenta), sources=["BB_7_13.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_13_21", r.kOrange),  sources=["BB_13_21.GenWeight"])
        org.mergeSamples(targetSpec=gopts("BB", r.kBlue), allWithPrefix="BB_")

        org.mergeSamples(targetSpec=gopts("hh_bb#tau#tau", r.kRed), sources=["hh_bbtt_c4_10"])

        #org.mergeSamples(targetSpec=gopts("H_c0_pu0",         r.kBlack),   sources=["H_0_3_c0_pu0.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c0_pu140",       r.kBlue),    sources=["H_0_3_c0_pu140.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c3_pu140",       r.kGreen),   sources=["H_0_3_c3_pu140.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c4_pu140",       r.kCyan),    sources=["H_0_3_c4_pu140.GenWeight"])

        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c3_pu140", r.kRed),     sources=["hh_bbtt_c3_pu140"])
        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_pu140", r.kMagenta), sources=["hh_bbtt_c4_pu140"])

        org.scale(1.0/fb)
        #org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     doLog=False,
                     fitFunc=lambda x: self.profFit(x, "b_v3"),
                     showStatBox=True,
                     optStat=1100,
                     ).plotAll()

        self.dumpFitResults(fileName="fitResults.py")


    def profFit(self, histo, version=""):
        if type(histo) is not r.TProfile:
            return

        assert version

        if not hasattr(self, "iFunc"):
            self.iFunc = 0
            self.fitText1 = []
            self.fitText2 = []
        else :
            self.iFunc += 1

        r.gStyle.SetOptFit(1111)

        go = getattr(self, version)
        f = go(histo=histo)
        if not f:
            return

        histo.Fit(f.GetName(), "rq", "sames")
        f.SetLineWidth(1)
        f.SetLineColor(1 + histo.GetLineColor())

        xtitle = histo.GetXaxis().GetTitle()
        s = xtitle.replace("uc.jet pT  (", "")
        s = s.replace(")", "")
        s = s.replace("|jet #", "abs(")
        s = s.replace("|", ")")
        s = s.replace("#leq", "<=")

        self.fitText2 += ["if %s:" % s,
                          "    return f%d" % self.iFunc]

        self.fitText1.append('f%d = r.TF1("f%d", "%s", %g, %g)' % (self.iFunc,
                                                                   self.iFunc,
                                                                   f.GetExpFormula("p"),
                                                                   f.GetXmin(),
                                                                   f.GetXmax())
                             )
        return f


    def b_v1(self, histo=None, min=20.0, max=200.0, x=70.0):
        xtitle = histo.GetXaxis().GetTitle()
        if ("0.9" in xtitle) and ("1.2" in xtitle):
            x = 90.0
        if ("1.2" in xtitle) and ("1.5" in xtitle):
            x = 80.0
            max = 170.0
        if ("1.8" in xtitle) and ("2.1" in xtitle):
            max = 170.0
        if ("2.4" in xtitle) and ("2.7" in xtitle):
            x = 90.0
        if ("2.7" in xtitle) and ("3.0" in xtitle):
            x = 60.0

        s = "(x <= %g)*([0] + [1]*x + [2]*x*x)" % x
        s += " + (x > %g)*([3] + [4]*x + [5]*x*x)" % x
        func = r.TF1(name, s, min, max)
        func.SetParameters(1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
        return func


    def b_v2(self, histo=None, min=10.0, max=200.0, x=70.0):
        xtitle = histo.GetXaxis().GetTitle()
        if ("0.3" in xtitle) and ("0.6" not in xtitle):
            x = 80.0
            max = 170.0
        if ("0.3" in xtitle) and ("0.6" in xtitle):
            max = 170.0
        if ("0.6" in xtitle) and ("0.9" in xtitle):
            x = 60.0
            max = 190.0
        if ("0.9" in xtitle) and ("1.2" in xtitle):
            x = 70.0
        if ("1.2" in xtitle) and ("1.5" in xtitle):
            x = 80.0
        if ("1.8" in xtitle) and ("2.1" in xtitle):
            max = 170.0
        if ("2.1" in xtitle) and ("2.4" in xtitle):
            x = 50.0
            max = 190.0
        if ("2.4" in xtitle) and ("2.7" in xtitle):
            x = 60.0
        if ("2.7" in xtitle) and ("3.0" in xtitle):
            x = 50.0
        if ("3.0" in xtitle) and ("4.0" in xtitle):
            x = 60.0
            max = 190.0

        s = "[0]"
        s += " + (x <= %g)*([1]*(x-%g) + [2]*(x-%g)**2)" % (x, x, x)
        s += " + (x  > %g)*([3]*(x-%g) + [4]*(x-%g)**2)" % (x, x, x)
        name = "func"
        func = r.TF1(name, s, min, max)
        func.SetParameters(1.0, 0.0, 0.0, 0.0, 0.0)

        if ("4.0" in xtitle) and not ("3.0" in xtitle):
            func = r.TF1("func", "[0]", 10.0, 80.0)
        return func


    def b_v3(self, histo=None, min=20.0, max=200.0, x=70.0):
        xtitle = histo.GetXaxis().GetTitle()

        if ("3.0" in xtitle) and ("4.0" in xtitle):
            max = 160.0

        s = "[0]"
        s += " + (x <= %g)*([1]*(x-%g) + [2]*(x-%g)**2)" % (x, x, x)
        s += " + (x  > %g)*([3]*(x-%g) + [4]*(x-%g)**2)" % (x, x, x)
        name = "func"
        func = r.TF1(name, s, min, max)
        func.SetParameters(1.0, 0.0, 0.0, 0.0, 0.0)

        if ("4.0" in xtitle) and not ("3.0" in xtitle):
            func = r.TF1(name, "[0]", min, 80.0)
        return func


    def tau_v2(self, histo=None, min=10.0, max=120.0, x=60.0):
        xtitle = histo.GetXaxis().GetTitle()
        if ("0.3" in xtitle) and ("0.6" not in xtitle):
            x = 70.0
            max = 150.0
        #if ("0.3" in xtitle) and ("0.6" in xtitle):
        #    x = 90.0
        #    max = 90.0
        if ("0.6" in xtitle) and ("0.9" in xtitle):
            x = 60.0
        if ("0.9" in xtitle) and ("1.2" in xtitle):
            x = 70.0
            max = 170.0
        #if ("1.2" in xtitle) and ("1.5" in xtitle):
        #    x = 80.0
        #if ("1.8" in xtitle) and ("2.1" in xtitle):
        #    max = 170.0
        if ("2.1" in xtitle) and ("2.4" in xtitle):
            x = 50.0
        if ("2.4" in xtitle) and ("2.7" in xtitle):
            x = 60.0
        if ("2.7" in xtitle) and ("3.0" in xtitle):
            x = 50.0
        if ("3.0" in xtitle) and ("4.0" in xtitle):
            x = 60.0

        s = "[0]"
        s += " + (x <= %g)*([1]*(x-%g) + [2]*(x-%g)**2)" % (x, x, x)
        s += " + (x  > %g)*([3]*(x-%g) + [4]*(x-%g)**2)" % (x, x, x)
        name = "func"
        func = r.TF1(name, s, min, max)
        func.SetParameters(1.0, 0.0, 0.0, 0.0, 0.0)

        #if ("4.0" in xtitle) and not ("3.0" in xtitle):
        #    func = r.TF1(name, "1.0", 10.0, 80.0)
        return func

