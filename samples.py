import supy
from units import pb, fb

eos = supy.sites.eos()+"/eos/cms/store/group/phys_higgs/upgrade"

conf = {(0, 0): "/PhaseI/Configuration0/NoPileUp/",
        (0, 140): "/PhaseI/Configuration0/140PileUp/",
        (3, 140): "/PhaseII/Configuration3/140PileUp/"
        }[(3, 140)]

def l(dir="", skip=[]):
    return eos+conf+'%s/", itemsToSkip=%s)' % (dir, str(skip))

h = supy.samples.SampleHolder()

sigSkip = ["_4.", "_10.", "_21.", "_23.", "_24.", "_35.", "_37.", "_39.", "_44.", "_48.", "_49."] if "n3" in conf else []
h.add("hh_bbtt", l("GluGluToHHToBBTT_14TeV", skip=sigSkip), xs=2.5*fb)

h.add("B",         l("B-4p-0-1-v1510_14TEV"),          xs=200944.*pb)

h.add("Bj_0_3",    l("Bj-4p-0-300-v1510_14TEV"),       xs=34409.*pb)
h.add("Bj_3_6",    l("Bj-4p-300-600-v1510_14TEV"),     xs=2642.*pb)
h.add("Bj_6_11",   l("Bj-4p-600-1100-v1510_14TEV"),    xs=294.12311*pb)
h.add("Bj_11_18",  l("Bj-4p-1100-1800-v1510_14TEV"),   xs=25.95*pb)
h.add("Bj_18_27",  l("Bj-4p-1800-2700-v1510_14TEV"),   xs=2.42111*pb)
h.add("Bj_27_37",  l("Bj-4p-2700-3700-v1510_14TEV"),   xs=0.22690*pb)
h.add("Bj_37_1k",  l("Bj-4p-3700-100000-v1510_14TEV"), xs=0.02767*pb)

h.add("Bjj_0_7",   l("Bjj-vbf-4p-0-700-v1510_14TEV"),       xs=86.45604*pb)
h.add("Bjj_7_14",  l("Bjj-vbf-4p-700-1400-v1510_14TEV"),    xs=4.34869*pb)
h.add("Bjj_14_23", l("Bjj-vbf-4p-1400-2300-v1510_14TEV"),   xs=0.32465*pb)
h.add("Bjj_23_34", l("Bjj-vbf-4p-2300-3400-v1510_14TEV"),   xs=0.03032*pb)
h.add("Bjj_34_1k", l("Bjj-vbf-4p-3400-100000-v1510_14TEV"), xs=0.00313*pb)

h.add("H_0_3",   l("H-4p-0-300-v1510_14TEV"), xs=21.55990*pb)
h.add("H_3_8",   l("H-4p-300-800-v1510_14TEV"), xs=1.11282*pb)
h.add("H_8_15",  l("H-4p-800-1500-v1510_14TEV"), xs=0.09188*pb)
h.add("H_15_1k", l("H-4p-1500-100000-v1510_14TEV"), xs=0.01009*pb)

h.add("BB_0_3",    l("BB-4p-0-300-v1510_14TEV"),        xs=249.97710*pb)
h.add("BB_3_7",    l("BB-4p-300-700-v1510_14TEV"),      xs=35.23062*pb)
h.add("BB_7_13",   l("BB-4p-700-1300-v1510_14TEV"),     xs=4.13743*pb)
h.add("BB_13_21",  l("BB-4p-1300-2100-v1510_14TEV"),    xs=0.41702*pb)
h.add("BB_21_1k",  l("BB-4p-2100-100000-v1510_14TEV"),  xs=0.04770*pb)

h.add("BBB_0_6",   l("BBB-4p-0-600-v1510_14TEV", skip=["BBB-4p-0-600-v1510_14TEV_107277746"]), xs=2.57304*pb)
h.add("BBB_6_13",  l("BBB-4p-600-1300-v1510_14TEV"),    xs=0.14935*pb)
h.add("BBB_13_1k", l("BBB-4p-1300-100000-v1510_14TEV"), xs=0.01274*pb)

h.add("LL_0_1",   l("LL-4p-0-100-v1510_14TEV"),       xs=1341.36923*pb)
h.add("LL_1_2",   l("LL-4p-100-200-v1510_14TEV"),     xs=156.29534*pb)
h.add("LL_2_5",   l("LL-4p-200-500-v1510_14TEV"),     xs=42.40132*pb)
h.add("LL_5_9",   l("LL-4p-500-900-v1510_14TEV"),     xs=2.84373*pb)
h.add("LL_9_14",  l("LL-4p-900-1400-v1510_14TEV"),    xs=0.20914*pb)
h.add("LL_14_1k", l("LL-4p-1400-100000-v1510_14TEV"), xs=0.02891*pb)

h.add("LLB_0_4",  l("LLB-4p-0-400-v1510_14TEV"),      xs=2.97380*pb)
h.add("LLB_4_9",  l("LLB-4p-400-900-v1510_14TEV"),    xs=0.22854*pb)
h.add("LLB_9_1k", l("LLB-4p-900-100000-v1510_14TEV"), xs=0.02080*pb)

h.add("tB_0_5",   l("tB-4p-0-500-v1510_14TEV"), xs=63.88923*pb)
h.add("tB_5_9",   l("tB-4p-500-900-v1510_14TEV"), xs=7.12172*pb)
h.add("tB_9_15",  l("tB-4p-900-1500-v1510_14TEV"), xs=0.98030*pb)
h.add("tB_15_22", l("tB-4p-1500-2200-v1510_14TEV"), xs=0.08391*pb)
h.add("tB_22_1k", l("tB-4p-2200-100000-v1510_14TEV"), xs=0.00953*pb)

h.add("tj_0_5",   l("tj-4p-0-500-v1510_14TEV"), xs=109.73602*pb)
h.add("tj_5_10",  l("tj-4p-500-1000-v1510_14TEV"), xs=5.99325*pb)
h.add("tj_10_16", l("tj-4p-1000-1600-v1510_14TEV"), xs=0.37680*pb)
h.add("tj_16_24", l("tj-4p-1600-2400-v1510_14TEV"), xs=0.03462*pb)
h.add("tj_24_1k", l("tj-4p-2400-100000-v1510_14TEV"), xs=0.00312*pb)

h.add("tt_0_600",       l("tt-4p-0-600-v1510_14TEV"),       xs=530.89358*pb)
h.add("tt_600_1100",    l("tt-4p-600-1100-v1510_14TEV"),    xs=42.55351*pb)
h.add("tt_1100_1700",   l("tt-4p-1100-1700-v1510_14TEV"),   xs=4.48209*pb)
h.add("tt_1700_2500",   l("tt-4p-1700-2500-v1510_14TEV"),   xs=0.52795*pb)
h.add("tt_2500_100000", l("tt-4p-2500-100000-v1510_14TEV"), xs=0.05449*pb)

h.add("ttB_0_9",   l("ttB-4p-0-900-v1510_14TEV"),       xs=2.6673*pb)
h.add("ttB_9_16",  l("ttB-4p-900-1600-v1510_14TEV"),    xs=0.250469*pb)
h.add("ttB_16_25", l("ttB-4p-1600-2500-v1510_14TEV"),   xs=0.0237441*pb)
h.add("ttB_25_1k", l("ttB-4p-2500-100000-v1510_14TEV"), xs=0.00208816*pb)
