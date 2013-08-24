import supy
from units import pb, fb

# test
test = supy.samples.SampleHolder()
test.add("tt_test", '["/tmp/elaird/ttbar140PU_Phase2.root"]', xs=500*pb)


# conf 0
conf0 = supy.samples.SampleHolder()
conf0s = "root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/upgrade/PhaseI/Configuration0/140PileUp"
conf0.add("tt.conf0_0_600", '[%s/tt-4p-0-600-v1510_14TEV/tt-4p-0-600-v1510_14TEV_354724341_PhaseI_Conf0_140PileUp.root"]' % conf0s,
          xs=500*pb)

# conf 3
def c3(dir="", skip=[]):
    stem = "root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/upgrade/PhaseII/Configuration3/140PileUp/"
    eos = "/afs/cern.ch/project/eos/installation/0.2.31/bin/eos.select"
    func = "utils.io.fileListFromEos"
    return '%s("%s", eos="%s", itemsToSkip=%s)' % (func, stem+dir+"/", eos, str(skip))


conf3 = supy.samples.SampleHolder()
conf3.add("tt_0_600",       c3("tt-4p-0-600-v1510_14TEV"),       xs=530.89358*pb)
conf3.add("tt_600_1100",    c3("tt-4p-600-1100-v1510_14TEV"),    xs=42.55351*pb)
conf3.add("tt_1100_1700",   c3("tt-4p-1100-1700-v1510_14TEV"),   xs=4.48209*pb)
conf3.add("tt_1700_2500",   c3("tt-4p-1700-2500-v1510_14TEV"),   xs=0.52795*pb)
conf3.add("tt_2500_100000", c3("tt-4p-2500-100000-v1510_14TEV"), xs=0.05449*pb)

conf3.add("hh_bbtt", c3("GluGluToHHToBBTT_14TeV",
                        skip=["_4.", "_10.", "_21.", "_23.", "_24.", "_35.", "_37.", "_39.", "_44.", "_48.", "_49."]),
          xs=2.5*fb)

conf3.add("BB_0_3",    c3("BB-4p-0-300-v1510_14TEV"),        xs=249.97710*pb)
conf3.add("BB_3_7",    c3("BB-4p-300-700-v1510_14TEV"),      xs=35.23062*pb)
conf3.add("BB_7_13",   c3("BB-4p-700-1300-v1510_14TEV"),     xs=4.13743*pb)
conf3.add("BB_13_21",  c3("BB-4p-1300-2100-v1510_14TEV"),    xs=0.41702*pb)
conf3.add("BB_21_1k",  c3("BB-4p-2100-100000-v1510_14TEV"),  xs=0.04770*pb)

conf3.add("BBB_0_6",   c3("BBB-4p-0-600-v1510_14TEV", skip=["BBB-4p-0-600-v1510_14TEV_107277746"]), xs=2.57304*pb)
conf3.add("BBB_6_13",  c3("BBB-4p-600-1300-v1510_14TEV"),    xs=0.14935*pb)
conf3.add("BBB_13_1k", c3("BBB-4p-1300-100000-v1510_14TEV"), xs=0.01274*pb)
