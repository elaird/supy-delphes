import math
import supy
import calculables
import steps
from units import fb, mb
import ROOT as r

class deriveCorrections(supy.analysis):
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                #supy.steps.histos.value("rho", 30, 0.0, 150.0),
                supy.steps.histos.value("HT", 300, 0.0, 3000.0),
                supy.steps.filters.multiplicity("bParticles", min=2, max=2),
                supy.steps.histos.mass("bParticlesSumP4", 50, 0.0, 250.0),
                supy.steps.histos.value("nMatches_JetMatchedTo_bParticles", 5, -0.5, 4.5),
                supy.steps.filters.value("nMatches_JetMatchedTo_bParticles", min=2, max=2),
                supy.steps.histos.value("DeltaR_JetMatchedTo_bParticles.values", 100, 0.0, 10.0),
                supy.steps.filters.value("DeltaR_JetMatchedTo_bParticles.values", min=0.2),
                
                supy.steps.histos.mass("JetMatchedTo_bParticles.valuesSumP4", 50, 0.0, 250.0),
                supy.steps.histos.mass("JetsFixedMassSumP4",                  50, 0.0, 250.0),
                supy.steps.histos.mass("JetsFixedMassCorrectedSumP4",         50, 0.0, 250.0),
                supy.steps.histos.value("jdj",                                50, 0.0, 250.0),
                #steps.displayer(),

                steps.iterHistogrammer(var="JetsFixedMass", attr="pt", func=True, labelIndex=False, nBins=20, xMin=0.0, xMax=200.0),
                supy.steps.filters.label("uncorrected"),
                steps.matchHistogrammer("JetMatchedTo_bParticles", maxDR=0.3,
                                        #etas=[0.6, 1.2, 1.8, 2.4, 3.0, 4.0],
                                        etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                                        correctPt=False,
                                        ),
                supy.steps.filters.label("corrected"),
                steps.matchHistogrammer("JetMatchedTo_bParticles", maxDR=0.3,
                                        #etas=[0.6, 1.2, 1.8, 2.4, 3.0, 4.0],
                                        etas=[0.3, 0.6, 0.9, 1.2, 1.5, 1.8, 2.1, 2.4, 2.7, 3.0, 4.0],
                                        correctPt=True,
                                        ),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.Filtered(pids=[-5, 5], label="b", status=[3]),
                              calculables.Filtered(pids=[-5, 5], label="bKine", ptMin=30.0, absEtaMax=2.4, status=[3]),
                              calculables.Filtered(pids=[23], label="Z", status=[3]),
                              calculables.Filtered(pids=[25], label="h", status=[3]),
                              calculables.JetMatchedTo(sourceKey="bParticles"),
                              calculables.SumP4("bParticles"),

                              calculables.nMatches("JetMatchedTo_bParticles", maxDR=0.3),
                              supy.calculables.other.values("JetMatchedTo_bParticles"),
                              calculables.DeltaR("JetMatchedTo_bParticles.values"),
                              # mass 1
                              calculables.SumP4("JetMatchedTo_bParticles.values"),
                              # mass 2
                              calculables.JetsFixedMass("JetMatchedTo_bParticles.values", m=mb),
                              calculables.SumP4("JetsFixedMass"),
                              calculables.JetsFixedMass("JetMatchedTo_bParticles.values", m=mb, correctPt=True),
                              calculables.SumP4("JetsFixedMassCorrected"),
                              # mass 3
                              calculables.jdj(jets="JetsFixedMass"),
                              calculables.JetsCategory(jets="JetsFixedMass"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        bb = calculables.window("JetsCategory", min="BB", max="BB")
        be = calculables.window("JetsCategory", min="BE", max="BE")
        ee = calculables.window("JetsCategory", min="EE", max="EE")

        rho0 = calculables.window("rho", max=80.)
        rho1 = calculables.window("rho", min=90., max=100.)
        rho2 = calculables.window("rho", min=110.)
        #n = 10000
        return (#specify(names="H_0_3_c0_pu0",    weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c0_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c3_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="H_0_3_c4_pu140",  weights=w, color=r.kBlack, nEventsMax=n) +

                ##specify(names="BB_0_3",   weights=w, color=r.kBlue, nEventsMax=n) +
                ##specify(names="BB_3_7",   weights=w, color=r.kBlue, nEventsMax=n) +
                ##specify(names="BB_7_13",  weights=w, color=r.kBlue, effectiveLumi=20/fb) +
                ##specify(names="BB_13_21", weights=w, color=r.kBlue, effectiveLumi=20/fb) +
                ###specify(names="BB_21_1k", weights=w, color=r.kBlue, effectiveLumi=2/fb) +
                
                specify(names="hh_bbtt",             color=r.kRed, effectiveLumi=20000/fb) +

                #specify(names="hh_bbtt", weights=bb, color=r.kRed, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt", weights=be, color=r.kRed, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt", weights=ee, color=r.kRed, effectiveLumi=20000/fb) +

                #specify(names="hh_bbtt_c3_pu140", color=r.kRed, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt_c4_pu140", color=r.kGreen, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt_c4_pu140", weights=[rho0], color=r.kBlack, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt_c4_pu140", weights=[rho1], color=r.kRed, effectiveLumi=20000/fb) +
                #specify(names="hh_bbtt_c4_pu140", weights=[rho2], color=r.kBlue, effectiveLumi=20000/fb) +
                []
                )


    def profFit(self, histo, dump=False):
        if type(histo) is not r.TProfile:
            return

        if not hasattr(self, "iFunc"):
            self.iFunc = 0
        else :
            self.iFunc += 1

        r.gStyle.SetOptFit(1111)
        name = "func"
        min = 20.0
        max = 200.0
        x = 70.0
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

        histo.Fit(name, "lrq", "sames")
        histo.GetFunction(name).SetLineWidth(1)
        histo.GetFunction(name).SetLineColor(1+histo.GetLineColor())
        if dump:
            s = xtitle.replace("jet pT  (", "")
            s = s.replace(")", "")
            s = s.replace("|#", "abs(")
            s = s.replace("|", ")")
            print "if %s:" % s
            print "    return f%d" % self.iFunc

            f = histo.GetFunction(name)
            print 'f%d = r.TF1("f%d", "%s", %g, %g)' % (self.iFunc, self.iFunc,
                                                        f.GetExpFormula("p"),
                                                        f.GetXmin(), f.GetXmax())
        return func


    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        #org.mergeSamples(targetSpec=gopts("BB_0_3",   r.kGreen),   sources=["BB_0_3.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_3_7",   r.kCyan),    sources=["BB_3_7.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_7_13",  r.kMagenta), sources=["BB_7_13.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("BB_13_21", r.kOrange),  sources=["BB_13_21.GenWeight"])
        org.mergeSamples(targetSpec=gopts("BB", r.kBlue), allWithPrefix="BB_")

        org.mergeSamples(targetSpec=gopts("hh_bb#tau#tau", r.kRed), sources=["hh_bbtt"])

        #org.mergeSamples(targetSpec=gopts("H_c0_pu0",         r.kBlack),   sources=["H_0_3_c0_pu0.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c0_pu140",       r.kBlue),    sources=["H_0_3_c0_pu140.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c3_pu140",       r.kGreen),   sources=["H_0_3_c3_pu140.GenWeight"])
        #org.mergeSamples(targetSpec=gopts("H_c4_pu140",       r.kCyan),    sources=["H_0_3_c4_pu140.GenWeight"])

        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c3_pu140", r.kRed),     sources=["hh_bbtt_c3_pu140"])
        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_pu140", r.kMagenta), sources=["hh_bbtt_c4_pu140"])

        org.mergeSamples(targetSpec=gopts("hh_bbtt_BB", r.kRed),     sources=["hh_bbtt.BB.le.JetsCategory.le.BB"])
        org.mergeSamples(targetSpec=gopts("hh_bbtt_BE", r.kMagenta), sources=["hh_bbtt.BE.le.JetsCategory.le.BE"])
        org.mergeSamples(targetSpec=gopts("hh_bbtt_EE", r.kCyan),    sources=["hh_bbtt.EE.le.JetsCategory.le.EE"])

        #org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_pu140",    r.kGreen), sources=["hh_bbtt_c4_pu140"])
        #org.mergeSamples(targetSpec=gopts("rho<80",     r.kBlack), sources=["hh_bbtt_c4_pu140.rho.le.80"])
        #org.mergeSamples(targetSpec=gopts("90<rho<100", r.kRed),   sources=["hh_bbtt_c4_pu140.90.le.rho.le.100"])
        #org.mergeSamples(targetSpec=gopts("110<rho",    r.kBlue),  sources=["hh_bbtt_c4_pu140.110.le.rho"])

        #org.scale(1.0/fb)
        org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     doLog=False,
                     #fitFunc=self.profFit,
                     showStatBox=False,
                     latexYieldTable=False,
                     #samplesForRatios=("hh_bb#tau#tau", "tt"),
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
