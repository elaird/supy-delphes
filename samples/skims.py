import supy
from units import pb, fb
import configuration

h = supy.samples.SampleHolder()

def s(d=""):
    return 'utils.fileListFromDisk(location="/afs/cern.ch/work/e/elaird/delphes/%s/%s/")' % (d, '%s')


hhSkim0  = s("PhaseI/Configuration0/NoPileUp/hh_skim_v2")
hhSkim41 = s("PhaseII/Configuration4/140PileUp/hh_skim_v2")
hhSkim4  = s("PhaseII/Configuration4v2/140PileUp/hh_skim_v3")
h.add("hh_bbtt_c41_pu140_10_skim", hhSkim41 % '10GeV', xs=9.439792e-03 * 2.500000e-03)
h.add("hh_bbtt_c41_pu140_20_skim", hhSkim41 % '20GeV', xs=5.575478e-03 * 2.500000e-03)
h.add("hh_bbtt_c0_pu0_20_skim",    hhSkim0  % '20GeV', xs=2.114810e-02 * 2.500000e-03)
h.add("hh_bbtt_c4_pu140_20_skim",  hhSkim4  % '20GeV', xs=1.165776e-02 * 2.500000e-03)

bbSkim = s("PhaseII/Configuration3/140PileUp/BB_skim")
h.add("BB_c3_0_3_skim",   bbSkim % "0_3",   xs = 1.234224e-05 * 3.188143e+02*pb)
h.add("BB_c3_3_7_skim",   bbSkim % "3_7",   xs = 6.641432e-05 * 4.465846e+01*pb)
h.add("BB_c3_7_13_skim",  bbSkim % "7_13",  xs = 1.450288e-04 * 5.224014e+00*pb)
h.add("BB_c3_13_21_skim", bbSkim % "13_21", xs = 1.935039e-04 * 5.252171e-01*pb)

bbbSkim = s("PhaseII/Configuration4v2/140PileUp/BBB_skim_v3")
h.add("BBB_c4_0_6_skim",   bbbSkim % '0_6',   xs=5.753050e-05 * 2.573040e+00)
h.add("BBB_c4_6_13_skim",  bbbSkim % '6_13',  xs=1.896258e-04 * 1.493500e-01)
h.add("BBB_c4_13_1k_skim", bbbSkim % '13_1k', xs=1.533004e-04 * 1.274000e-02)

ttSkim = s("PhaseII/Configuration4v2/140PileUp/tt_skim_v3")
h.add("tt_c4_pu140_0_6_skim",   ttSkim % "0_6",   xs=9.064403e-04 * 5.308936e+02)
h.add("tt_c4_pu140_6_11_skim",  ttSkim % "6_11",  xs=2.268561e-03 * 4.255351e+01)
h.add("tt_c4_pu140_11_17_skim", ttSkim % "11_17", xs=3.647637e-03 * 4.482090e+00)
h.add("tt_c4_pu140_17_25_skim", ttSkim % "17_25", xs=4.620597e-03 * 5.279500e-01)
h.add("tt_c4_pu140_25_1k_skim", ttSkim % "25_1k", xs=5.394740e-03 * 5.449000e-02)

ttSkim = s("PhaseII/Configuration4/140PileUp/tt_skim_v2")
h.add("tt_c41_pu140_0_6_skim",   ttSkim % "0_6",   xs=4.378638e-04 * 5.308936e+02)
h.add("tt_c41_pu140_6_11_skim",  ttSkim % "6_11",  xs=1.378834e-03 * 4.255351e+01)
h.add("tt_c41_pu140_11_17_skim", ttSkim % "11_17", xs=2.391672e-03 * 4.482090e+00)
h.add("tt_c41_pu140_17_25_skim", ttSkim % "17_25", xs=3.110121e-03 * 5.279500e-01)
h.add("tt_c41_pu140_25_1k_skim", ttSkim % "25_1k", xs=3.746964e-03 * 5.449000e-02)

ttSkim = s("PhaseI/Configuration0/NoPileUp/tt_skim_v2")
h.add("tt_c0_pu0_0_6_skim",   ttSkim % '0_6',   xs=1.207047e-03 * 5.308936e+02)
h.add("tt_c0_pu0_6_11_skim",  ttSkim % '6_11',  xs=2.468778e-03 * 4.255351e+01)
h.add("tt_c0_pu0_11_17_skim", ttSkim % '11_17', xs=3.333778e-03 * 4.482090e+00)
h.add("tt_c0_pu0_17_25_skim", ttSkim % '17_25', xs=3.968942e-03 * 5.279500e-01)
h.add("tt_c0_pu0_25_1k_skim", ttSkim % '25_1k', xs=4.538753e-03 * 5.449000e-02)
