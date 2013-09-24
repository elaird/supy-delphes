import math
import supy
import calculables
import steps
from units import fb, mb, mtau
import ROOT as r

class skim_batch(supy.analysis):
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                supy.steps.histos.value("HT", 50, 0.0, 2500.0),
                supy.steps.histos.multiplicity("Jets"),
                supy.steps.filters.multiplicity("Jets", min=4),
                supy.steps.histos.multiplicity("bTagged_Jets_mask1"),
                supy.steps.filters.multiplicity("bTagged_Jets_mask1", min=2),
                supy.steps.histos.multiplicity("tauTagged_Jets"),
                supy.steps.filters.multiplicity("tauTagged_Jets", min=2),
                supy.steps.other.skimmer(),
                ]


    def listOfCalculables(self, pars):
        listOfCalculables = supy.calculables.zeroArgs(supy.calculables)
        listOfCalculables += supy.calculables.zeroArgs(calculables)
        listOfCalculables += [calculables.HT(),
                              calculables.rho(),
                              calculables.Filtered(label="", ptMin=20.0, absEtaMax=2.4, key="Jet"),
                              calculables.bTagged("Jets", mask=0x1),
                              calculables.tauTagged("Jets"),
                              ]
        return listOfCalculables


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()
        return (specify(names="tt_0_6",   weights=w) +
                specify(names="tt_6_11",  weights=w) +
                specify(names="tt_11_17", weights=w) +
                specify(names="tt_17_25", weights=w) +
                specify(names="tt_25_1k", weights=w) +
                #specify(names="hh_bbtt_c0_pu0") +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars)
        supy.utils.printSkimResults(org)

        def gopts(name="", color=1):
            return {"name":name, "color":color, "markerStyle":1, "lineWidth":2, "goptions":"ehist"}

        org.mergeSamples(targetSpec=gopts("tt_0_6",   r.kBlue),    sources=["tt_0_6.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt_6_11",  r.kGreen),   sources=["tt_6_11.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt_11_17", r.kCyan),    sources=["tt_11_17.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt_17_25", r.kMagenta), sources=["tt_17_25.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt_25_1k", r.kOrange),  sources=["tt_25_1k.GenWeight"])
        org.mergeSamples(targetSpec=gopts("tt", r.kBlack), allWithPrefix="tt_", keepSources=True)

        org.scale(3.e3/fb)
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
                     latexYieldTable=True,
                     #samplesForRatios=("hh_bbtt", "tt"),
                     #sampleLabelsForRatios=("hh", "tt"),
                     #foms=[{"value": lambda x, y: x/y,
                     #       "uncRel": lambda x, y, xUnc, yUnc: math.sqrt((xUnc/x)**2 + (yUnc/y)**2),
                     #       "label": lambda x, y:"%s/%s" % (x, y),
                     #       },
                     #      ],
                     ).plotAll()
