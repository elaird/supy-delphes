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
conf3.add("hh_bbtt", c3("GluGluToHHToBBTT_14TeV",
                        skip=["_4.", "_10.", "_21.", "_23.", "_24.", "_35.", "_37.", "_39.", "_44.", "_48.", "_49."]),
          xs=2.5*fb)

conf3.add("B",         c3("B-4p-0-1-v1510_14TEV"),          xs=200944.*pb)

conf3.add("Bj_0_3",    c3("Bj-4p-0-300-v1510_14TEV"),       xs=34409.*pb)
conf3.add("Bj_3_6",    c3("Bj-4p-300-600-v1510_14TEV"),     xs=2642.*pb)
conf3.add("Bj_6_11",   c3("Bj-4p-600-1100-v1510_14TEV"),    xs=294.12311*pb)
conf3.add("Bj_11_18",  c3("Bj-4p-1100-1800-v1510_14TEV"),   xs=25.95*pb)
conf3.add("Bj_18_27",  c3("Bj-4p-1800-2700-v1510_14TEV"),   xs=2.42111*pb)
conf3.add("Bj_27_37",  c3("Bj-4p-2700-3700-v1510_14TEV"),   xs=0.22690*pb)
conf3.add("Bj_37_1k",  c3("Bj-4p-3700-100000-v1510_14TEV"), xs=0.02767*pb)

conf3.add("Bjj_0_7",   c3("Bjj-vbf-4p-0-700-v1510_14TEV"),       xs=86.45604*pb)
conf3.add("Bjj_7_14",  c3("Bjj-vbf-4p-700-1400-v1510_14TEV"),    xs=4.34869*pb)
conf3.add("Bjj_14_23", c3("Bjj-vbf-4p-1400-2300-v1510_14TEV"),   xs=0.32465*pb)
conf3.add("Bjj_23_34", c3("Bjj-vbf-4p-2300-3400-v1510_14TEV"),   xs=0.03032*pb)
conf3.add("Bjj_34_1k", c3("Bjj-vbf-4p-3400-100000-v1510_14TEV"), xs=0.00313*pb)

conf3.add("H_0_3",   c3("H-4p-0-300-v1510_14TEV"), xs=21.55990*pb)
conf3.add("H_3_8",   c3("H-4p-300-800-v1510_14TEV"), xs=1.11282*pb)
conf3.add("H_8_15",  c3("H-4p-800-1500-v1510_14TEV"), xs=0.09188*pb)
conf3.add("H_15_1k", c3("H-4p-1500-100000-v1510_14TEV"), xs=0.01009*pb)

conf3.add("BB_0_3",    c3("BB-4p-0-300-v1510_14TEV"),        xs=249.97710*pb)
conf3.add("BB_3_7",    c3("BB-4p-300-700-v1510_14TEV"),      xs=35.23062*pb)
conf3.add("BB_7_13",   c3("BB-4p-700-1300-v1510_14TEV"),     xs=4.13743*pb)
conf3.add("BB_13_21",  c3("BB-4p-1300-2100-v1510_14TEV"),    xs=0.41702*pb)
conf3.add("BB_21_1k",  c3("BB-4p-2100-100000-v1510_14TEV"),  xs=0.04770*pb)

conf3.add("BBB_0_6",   c3("BBB-4p-0-600-v1510_14TEV", skip=["BBB-4p-0-600-v1510_14TEV_107277746"]), xs=2.57304*pb)
conf3.add("BBB_6_13",  c3("BBB-4p-600-1300-v1510_14TEV"),    xs=0.14935*pb)
conf3.add("BBB_13_1k", c3("BBB-4p-1300-100000-v1510_14TEV"), xs=0.01274*pb)

conf3.add("LL_0_1",   c3("LL-4p-0-100-v1510_14TEV"),       xs=1341.36923*pb)
conf3.add("LL_1_2",   c3("LL-4p-100-200-v1510_14TEV"),     xs=156.29534*pb)
conf3.add("LL_2_5",   c3("LL-4p-200-500-v1510_14TEV"),     xs=42.40132*pb)
conf3.add("LL_5_9",   c3("LL-4p-500-900-v1510_14TEV"),     xs=2.84373*pb)
conf3.add("LL_9_14",  c3("LL-4p-900-1400-v1510_14TEV"),    xs=0.20914*pb)
conf3.add("LL_14_1k", c3("LL-4p-1400-100000-v1510_14TEV"), xs=0.02891*pb)

conf3.add("LLB_0_4",  c3("LLB-4p-0-400-v1510_14TEV"),      xs=2.97380*pb)
conf3.add("LLB_4_9",  c3("LLB-4p-400-900-v1510_14TEV"),    xs=0.22854*pb)
conf3.add("LLB_9_1k", c3("LLB-4p-900-100000-v1510_14TEV"), xs=0.02080*pb)

conf3.add("tB_0_5",   c3("tB-4p-0-500-v1510_14TEV"), xs=63.88923*pb)
conf3.add("tB_5_9",   c3("tB-4p-500-900-v1510_14TEV"), xs=7.12172*pb)
conf3.add("tB_9_15",  c3("tB-4p-900-1500-v1510_14TEV"), xs=0.98030*pb)
conf3.add("tB_15_22", c3("tB-4p-1500-2200-v1510_14TEV"), xs=0.08391*pb)
conf3.add("tB_22_1k", c3("tB-4p-2200-100000-v1510_14TEV"), xs=0.00953*pb)

conf3.add("tj_0_5",   c3("tj-4p-0-500-v1510_14TEV"), xs=109.73602*pb)
conf3.add("tj_5_10",  c3("tj-4p-500-1000-v1510_14TEV"), xs=5.99325*pb)
conf3.add("tj_10_16", c3("tj-4p-1000-1600-v1510_14TEV"), xs=0.37680*pb)
conf3.add("tj_16_24", c3("tj-4p-1600-2400-v1510_14TEV"), xs=0.03462*pb)
conf3.add("tj_24_1k", c3("tj-4p-2400-100000-v1510_14TEV"), xs=0.00312*pb)

conf3.add("tt_0_600",       c3("tt-4p-0-600-v1510_14TEV"),       xs=530.89358*pb)
conf3.add("tt_600_1100",    c3("tt-4p-600-1100-v1510_14TEV"),    xs=42.55351*pb)
conf3.add("tt_1100_1700",   c3("tt-4p-1100-1700-v1510_14TEV"),   xs=4.48209*pb)
conf3.add("tt_1700_2500",   c3("tt-4p-1700-2500-v1510_14TEV"),   xs=0.52795*pb)
conf3.add("tt_2500_100000", c3("tt-4p-2500-100000-v1510_14TEV"), xs=0.05449*pb)

conf3.add("ttB_0_9",   c3("ttB-4p-0-900-v1510_14TEV"),       xs=2.6673*pb)
conf3.add("ttB_9_16",  c3("ttB-4p-900-1600-v1510_14TEV"),    xs=0.250469*pb)
conf3.add("ttB_16_25", c3("ttB-4p-1600-2500-v1510_14TEV"),   xs=0.0237441*pb)
conf3.add("ttB_25_1k", c3("ttB-4p-2500-100000-v1510_14TEV"), xs=0.00208816*pb)
