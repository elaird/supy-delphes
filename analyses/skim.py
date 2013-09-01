import supy
import calculables
import steps
from units import fb
import ROOT as r

class skim(supy.analysis):
    def listOfSteps(self, pars):
        return [supy.steps.printer.progressPrinter(),
                supy.steps.filters.multiplicity("ZParticles", min=2, max=2),
                supy.steps.filters.multiplicity("bParticles", min=2, max=2),
                supy.steps.filters.multiplicity("bKineParticles", min=2, max=2),
                supy.steps.filters.multiplicity("tauParticles", min=2, max=2),
                supy.steps.filters.multiplicity("tauKineParticles", min=2, max=2),
                supy.steps.other.skimmer(),
                ]


    def listOfCalculables(self, pars):
        out = supy.calculables.zeroArgs(supy.calculables)
        out += supy.calculables.zeroArgs(calculables)
        out += [calculables.Filtered(pids=[-5, 5], label="b", status=[3]),
                calculables.Filtered(pids=[-15, 15], label="tau", status=[3]),
                calculables.Filtered(pids=[-5, 5], label="bKine", ptMin=40.0, absEtaMax=2.4, status=[3]),
                calculables.Filtered(pids=[-15, 15], label="tauKine", ptMin=40.0, absEtaMax=2.4, status=[3]),
                calculables.Filtered(pids=[23], label="Z", status=[3]),
                calculables.Filtered(pids=[25], label="h", status=[3]),
                ]
        return out


    def listOfSampleDictionaries(self):
        from samples import h
        return [h]


    def listOfSamples(self, pars):
        from supy.samples import specify
        w = calculables.GenWeight()

        return (specify(names="BB_0_3",    weights=w) +
                specify(names="BB_3_7",    weights=w) +
                specify(names="BB_7_13",   weights=w) +
                specify(names="BB_13_21",  weights=w) +
                #specify(names="BB_21_1k", weights=w) +
                []
                )


    def conclude(self, pars):
        org = self.organizer(pars)
        supy.utils.printSkimResults(org)
