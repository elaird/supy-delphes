import supy, calculables
import ROOT as r

class skimTest(supy.analysis):
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                supy.steps.histos.value("32", 1, 31.5, 32.5),
                supy.steps.histos.multiplicity("nuParticles"),
                supy.steps.filters.multiplicity("Jets", min=4),
                supy.steps.filters.multiplicity("tauTagged_Jets", min=2, max=2),
                supy.steps.histos.multiplicity("nuParticles"),
                supy.steps.other.skimmer(),
                ]

    def listOfCalculables(self, pars):
        return supy.calculables.zeroArgs(supy.calculables) + supy.calculables.zeroArgs(calculables) +\
               [calculables.Filtered(label="", ptMin=10.0, absEtaMax=2.4, key="Jet"),
                calculables.Filtered(pids=[-16, -14, -12, 12, 14, 16], label="nu", status=[3]),
                calculables.tauTagged("Jets"),
                supy.calculables.other.fixedValue(label="32", value=32.0),
                ]

    def listOfSampleDictionaries(self):
        from samples import h
        h.add("tt_25_1k_skim", '["tt_25_1k.GenWeight_1_0_skim.root"]', xs=1.222114e-02 * 5.449000e-02)
        return [h]

    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()
        return (specify(names="tt_25_1k",        weights=w, color=r.kBlack, nFilesMax=1) +
                #specify(names="tt_25_1k_skim",   weights=w, color=r.kBlue,  nFilesMax=1) +
                []
                )

    def conclude(self, pars):
        org = self.organizer(pars, prefixesNoScale=["efficiency_"])
        supy.utils.printSkimResults(org)
        org.scale(1.e3)
        supy.plotter(org,
                     pdfFileName=self.pdfFileName(org.tag),
                     printImperfectCalcPageIfEmpty=False,
                     printXs=True,
                     blackList=["lumiHisto", "xsHisto", "nJobsHisto"],
                     rowColors=[1, 2],
                     doLog=True,
                     optStat=1111,
                     showStatBox=False,
                     ).plotAll()
