import math
import supy
import calculables
import steps
from units import fb, mb, mtau
import ROOT as r

class reco2(supy.analysis):
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

                #supy.steps.histos.mass("bTagged_Jets_mask1_SumP4",              50, 0.0, 250.0),
                #supy.steps.histos.mass("JetsFixedMass_bTagged_SumP4",           50, 0.0, 250.0),
                supy.steps.histos.mass("JetsFixedMass_bTagged_Corrected_SumP4", 50, 0.0, 250.0),
                supy.steps.filters.mass("JetsFixedMass_bTagged_Corrected_SumP4", min=85.0, max=150.0),
                supy.steps.histos.mass("JetsFixedMass_bTagged_Corrected_SumP4", 50, 0.0, 250.0),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.Filtered(label="", ptMin=10.0, absEtaMax=2.4, key="Jet"),
                              calculables.bTagged("Jets", mask=0x1),
                              calculables.tauTagged("Jets"),

                              calculables.SumP4("bTagged_Jets_mask1"),
                              calculables.JetsFixedMass("bTagged_Jets_mask1", m=mb, label="bTagged"),
                              calculables.SumP4("JetsFixedMass_bTagged"),
                              calculables.JetsFixedMass("bTagged_Jets_mask1", m=mb, correctPt=True, label="bTagged"),
                              calculables.SumP4("JetsFixedMass_bTagged_Corrected"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        n = 100000
        nSmall = 40000
        el = 2000/fb
        return (specify(names="tt_c4_0_6_skim",   weights=w, color=r.kBlue, nEventsMax=nSmall) +
                specify(names="tt_c4_6_11_skim",  weights=w, color=r.kBlue, nEventsMax=nSmall) +
                specify(names="tt_c4_11_17_skim", weights=w, color=r.kBlue, nEventsMax=nSmall) +
                specify(names="tt_c4_17_25_skim", weights=w, color=r.kBlue, nEventsMax=nSmall) +
                specify(names="tt_c4_25_1k_skim", weights=w, color=r.kBlue, nEventsMax=nSmall) +

                #specify(names="tt_0_6",   weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="tt_6_11",  weights=w, color=r.kBlack, nEventsMax=n) +
                #specify(names="tt_11_17", weights=w, color=r.kBlack, effectiveLumi=40/fb) +
                #specify(names="tt_17_25", weights=w, color=r.kBlack, nEventsMax=n) + #effectiveLumi=20/fb) +
                #specify(names="tt_25_1k", weights=w, color=r.kBlack, nEventsMax=n) + #effectiveLumi=200/fb) +

                specify(names="hh_bbtt_c4_10", color=r.kBlack,  effectiveLumi=el) +
                specify(names="hh_bbtt_c4_20", color=r.kBlack,  effectiveLumi=el) +
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
        org.mergeSamples(targetSpec=gopts("tt_skim", r.kBlack), allWithPrefix="tt_")

        org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_10", r.kRed), sources=["hh_bbtt_c4_10"])
        org.mergeSamples(targetSpec=gopts("hh_bbtt_c4_20", r.kBlue), sources=["hh_bbtt_c4_20"])

        org.scale(3.e3/fb)
        #org.scale(toPdf=True)

        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[r.kBlack, r.kViolet+4],

                     doLog=True,
                     #optStat=1100,
                     optStat=1111,
                     #fitFunc=self.profFit,
                     showStatBox=False,
                     latexYieldTable=False,
                     #samplesForRatios=("hh_bb#tau#tau", "tt"),
                     #sampleLabelsForRatios=("hh", "tt"),
                     #foms=[{"value": lambda x, y: x/y,
                     #       "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y)**2),
                     #       "label": lambda x, y:"%s/%s" % (x, y),
                     #       },
                     #      #{"value": lambda x,y: x/(y**0.5),
                     #      # "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y/2.)**2),
                     #      # "label": lambda x,y: "%s/sqrt(%s)" % (x, y),
                     #      # },
                     #      ],
                     ).plotAll()
