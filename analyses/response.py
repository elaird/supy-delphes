import supy
import calculables
import steps
from units import fb
import ROOT as r

class response(supy.analysis):
    def listOfSteps(self, _):
        pt = {"attr": "PT",  "func": False, "nBins": 200, "xMin": 0.0, "xMax": 1000.0}
        eta= {"attr": "Eta", "func": False, "nBins": 120, "xMin": -6.0, "xMax": 6.0}
        j = "GenJet"
        #g = "GenJet"
        #g = "70GenJets"
        g = "bParticles"
        require2b = True

        out = [supy.steps.printer.progressPrinter(),
               #supy.steps.histos.value("rho", 30, 0.0, 150.0),
               supy.steps.histos.value("HT", 100, 0.0, 1000.0),
               #steps.iterHistogrammer(var="GenJet", attr="PT", func=False, nBins=30, xMin=0.0, xMax=300.0),
               #supy.steps.histos.multiplicity("JetMatchedTo_GenJet"),
               ]

        if require2b:
            out += [supy.steps.filters.multiplicity("bParticles", min=2, max=2),
                    supy.steps.histos.mass("bParticles_SumP4", 50, 0.0, 250.0),
                    supy.steps.filters.mass("bParticles_SumP4", min=124.0, max=126.0),
                    ]

        out += [steps.iterHistogrammer(var=g, **pt),
                steps.iterHistogrammer(var=g, **eta),

                steps.iterHistogrammer(var=j, **pt),
                steps.iterHistogrammer(var=j, **eta),

                steps.matchDRHistogrammer("%sMatchedTo_%s_noMaxDR" % (j, g)),
                steps.matchDRHistogrammer("%sMatchedTo_%s" % (j, g)),

                steps.iterHistogrammer(var="%sMatchedTo_%s.keys" % (j, g), **pt),
                steps.iterHistogrammer(var="%sMatchedTo_%s.keys" % (j, g), **eta),

                steps.iterHistogrammer(var="%sMatchedTo_%s.values" % (j, g), **pt),
                steps.iterHistogrammer(var="%sMatchedTo_%s.values" % (j, g), **eta),

                steps.matchPtHistogrammer("%sMatchedTo_%s" % (j, g),
                                          etas=[],
                                          #particleLabel="gen. jet",
                                          correctPtAxis=False,
                                          correctRatio=False,
                                          alsoVsParticle=True,
                                          alsoVsEta=True,
                                          ),
                ]
        return out


    def listOfCalculables(self, pars):
        maxDR = 0.3
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.JetMatchedTo(sourceKey="GenJet"),
                              calculables.JetMatchedTo(sourceKey="GenJet", maxDR=maxDR),
                              supy.calculables.other.values("JetMatchedTo_GenJet"),
                              supy.calculables.other.keys("JetMatchedTo_GenJet"),

                              calculables.Filtered(label="70", key="GenJet", ptMin=70.0),
                              calculables.JetMatchedTo(sourceKey="70GenJets"),
                              calculables.JetMatchedTo(sourceKey="70GenJets", maxDR=maxDR),
                              supy.calculables.other.values("JetMatchedTo_70GenJets"),
                              supy.calculables.other.keys("JetMatchedTo_70GenJets"),

                              calculables.Filtered(pids=[-5, 5], label="b", status=[3], key="Particle", ptMin=0.0),
                              calculables.SumP4("bParticles"),

                              calculables.JetMatchedTo(sourceKey="bParticles"),
                              calculables.JetMatchedTo(sourceKey="bParticles", maxDR=maxDR),
                              supy.calculables.other.values("JetMatchedTo_bParticles"),
                              supy.calculables.other.keys("JetMatchedTo_bParticles"),

                              calculables.JetMatchedTo(sourceKey="bParticles", jetKey="GenJet"),
                              calculables.JetMatchedTo(sourceKey="bParticles", jetKey="GenJet", maxDR=maxDR),
                              supy.calculables.other.values("GenJetMatchedTo_bParticles"),
                              supy.calculables.other.keys("GenJetMatchedTo_bParticles"),

                              calculables.PtRatio("GenJetMatchedTo_bParticles"),
                              calculables.minItem("GenJetMatchedTo_bParticles_PtRatio"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        return (#specify(names="QCD_c4_pu140_Pt_0p3_4") +

                specify(names="H_0_3",  weights=w, nFilesMax=5) +
                specify(names="H_3_8",  weights=w, nFilesMax=3) +
                specify(names="H_8_15",  weights=w, nFilesMax=5) +
                specify(names="H_15_1k",  weights=w, nFilesMax=5) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}
        org.mergeSamples(targetSpec=gopts("QCD", r.kBlue), sources=["QCD_c4_pu140_Pt_0p3_4"])
        org.mergeSamples(targetSpec=gopts("H", r.kBlue), allWithPrefix="H_")
        org.scale(1.0/fb)
        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     fitFunc=lambda x: self.profFit(x, "eta"),
                     doLog=False,
                     drawYx=True,
                     showStatBox=True,
                     optStat=1100,
                     ).plotAll()

        self.dumpFitResults(fileName="fitResults.py")


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


    def profFit(self, histo, version=""):
        assert version

        if type(histo) is not r.TProfile:
            return

        histo.GetYaxis().SetRangeUser(0.0, 2.0)
        xtitle = histo.GetXaxis().GetTitle()

        if "jet eta" not in xtitle:
            return

        if "gen." in xtitle:
            return

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
        #f.Draw("sames")
        f.SetLineWidth(1)
        f.SetLineColor(1 + histo.GetLineColor())

        self.fitText2 += ["  return f%d" % self.iFunc]

        self.fitText1.append('f%d = r.TF1("f%d", "%s", %g, %g)' % (self.iFunc,
                                                                   self.iFunc,
                                                                   f.GetExpFormula("p"),
                                                                   f.GetXmin(),
                                                                   f.GetXmax())
                             )
        return f


    def eta(self, histo=None, min=-3.5, max=3.5, t=2.2):
        xtitle = histo.GetXaxis().GetTitle()

        s = "[0]"
        s += " + (fabs(x)<%g)*(cos([1]*x)*([2]+[3]*fabs(x)))" % t
        s += " + (fabs(x)>=%g)*([4] + [5]*fabs(x)+[6]*x*x)" % t
        func = r.TF1("func", s, min, max)
        func.SetParameters(0.95, 2.5, 0.05, 0.01,
                           1.0, 0.0, 0.0,
                           )
        return func
