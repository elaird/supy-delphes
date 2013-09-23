import supy
import calculables
import steps
from units import fb
import ROOT as r

class response(supy.analysis):
    def listOfSteps(self, _):
        pt = {"attr": "PT",  "func": False, "nBins": 200, "xMin": 0.0, "xMax": 1000.0}
        eta= {"attr": "Eta", "func": False, "nBins": 120, "xMin": -6.0, "xMax": 6.0}
        #g = "GenJet"
        g = "70GenJets"
        return [supy.steps.printer.progressPrinter(),
                #supy.steps.histos.value("rho", 30, 0.0, 150.0),
                #supy.steps.histos.value("HT", 100, 0.0, 1000.0),
                #steps.iterHistogrammer(var="GenJet", attr="PT", func=False, nBins=30, xMin=0.0, xMax=300.0),
                #supy.steps.histos.multiplicity("JetMatchedTo_GenJet"),

                steps.iterHistogrammer(var=g, **pt),
                steps.iterHistogrammer(var=g, **eta),

                steps.iterHistogrammer(var="Jet", **pt),
                steps.iterHistogrammer(var="Jet", **eta),

                steps.matchDRHistogrammer("JetMatchedTo_%s_noMaxDR" % g),
                steps.matchDRHistogrammer("JetMatchedTo_%s" % g),

                steps.iterHistogrammer(var="JetMatchedTo_%s.keys" % g, **pt),
                steps.iterHistogrammer(var="JetMatchedTo_%s.keys" % g, **eta),

                steps.iterHistogrammer(var="JetMatchedTo_%s.values" % g, **pt),
                steps.iterHistogrammer(var="JetMatchedTo_%s.values" % g, **eta),

                steps.matchPtHistogrammer("JetMatchedTo_%s" % g,
                                          etas=[],
                                          particleLabel="gen. jet",
                                          correctPtAxis=False,
                                          correctRatio=False,
                                          alsoVsParticle=True,
                                          alsoVsEta=True,
                                          ),
                #steps.matchPtHistogrammer("JetMatchedTo_GenJet",
                #                          etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                #                          correctPtAxis=False,
                #                          correctRatio=False,
                #                          particleLabel="gen. jet",
                #                          ),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.JetMatchedTo(sourceKey="GenJet"),
                              calculables.JetMatchedTo(sourceKey="GenJet", maxDR=0.6),
                              supy.calculables.other.values("JetMatchedTo_GenJet"),
                              supy.calculables.other.keys("JetMatchedTo_GenJet"),

                              calculables.Filtered(label="70", key="GenJet", ptMin=70.0),
                              calculables.JetMatchedTo(sourceKey="70GenJets"),
                              calculables.JetMatchedTo(sourceKey="70GenJets", maxDR=0.6),
                              supy.calculables.other.values("JetMatchedTo_70GenJets"),
                              supy.calculables.other.keys("JetMatchedTo_70GenJets"),
                              
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        return (specify(names="QCD_c4_pu140_Pt_0p3_4") +

                #specify(names="H_0_3",  weights=w, nFilesMax=5) +
                #specify(names="H_3_8",  weights=w, nFilesMax=3) +
                #specify(names="H_8_15",  weights=w, nFilesMax=5) +
                #specify(names="H_15_1k",  weights=w, nFilesMax=5) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}
        org.mergeSamples(targetSpec=gopts("QCD", r.kBlue), sources=["QCD_c4_pu140_Pt_0p3_4"])
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
