import supy
from units import pb, fb
import configuration

h = supy.samples.SampleHolder()

def s(d=""):
    return 'utils.fileListFromDisk(location="/afs/cern.ch/work/e/elaird/delphes/%s/%s/")' % (d, '%s')

def s3(d=""):
    loc = "/afs/cern.ch/work/e/elaird/delphes/PhaseII/Configuration4v2/140PileUp/v3/%s" % d
    return 'utils.fileListFromDisk(location="%s", isDirectory=False)' % loc


hhSkim0  = s("PhaseI/Configuration0/NoPileUp/hh_skim_v2")
hhSkim41 = s("PhaseII/Configuration4/140PileUp/hh_skim_v2")
hhSkim4  = s("PhaseII/Configuration4v2/140PileUp/hh_skim_v3")
h.add("hh_bbtt_c41_pu140_10_skim", hhSkim41 % '10GeV', xs=9.439792e-03 * 2.500000e-03)
h.add("hh_bbtt_c41_pu140_20_skim", hhSkim41 % '20GeV', xs=5.575478e-03 * 2.500000e-03)
h.add("hh_bbtt_c0_pu0_20_skim",    hhSkim0  % '20GeV', xs=2.114810e-02 * 2.500000e-03)
h.add("hh_bbtt_c4_pu140_20_skim",  hhSkim4  % '20GeV', xs=1.165776e-02 * 2.500000e-03)

bbSkim = s("PhaseII/Configuration4v2/140PileUp/BB_skim_v3")
h.add("BB_c4_pu140_0_3_skim",   bbSkim % "0_3",   xs=4.882651e-06 * 2.499771e+02)
h.add("BB_c4_pu140_3_7_skim",   bbSkim % "3_7",   xs=4.449487e-05 * 3.523062e+01)
h.add("BB_c4_pu140_7_13_skim",  bbSkim % "7_13",  xs=1.023959e-04 * 4.137430e+00)
h.add("BB_c4_pu140_13_21_skim", bbSkim % "13_21", xs=1.207603e-04 * 4.170200e-01)
h.add("BB_c4_pu140_21_1k_skim", bbSkim % "21_1k", xs=1.195612e-04 * 4.770000e-02)

bbbSkim = s("PhaseII/Configuration4v2/140PileUp/BBB_skim_v3")
h.add("BBB_c4_pu140_0_6_skim",   bbbSkim % '0_6',   xs=5.753050e-05 * 2.573040e+00)
h.add("BBB_c4_pu140_6_13_skim",  bbbSkim % '6_13',  xs=1.896258e-04 * 1.493500e-01)
h.add("BBB_c4_pu140_13_1k_skim", bbbSkim % '13_1k', xs=1.533004e-04 * 1.274000e-02)

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


h.add("B_skim",         s3("B.GenWeight_*_skim.root"),         xs=1.715353e-07 * 2.009440e+05)
h.add("Bj_0_3_skim",    s3("Bj_0_3.GenWeight_*_skim.root"),    xs=3.163408e-06 * 3.440900e+04)
h.add("Bj_3_6_skim",    s3("Bj_3_6.GenWeight_*_skim.root"),    xs=1.915570e-05 * 2.642000e+03)
h.add("Bj_6_11_skim",   s3("Bj_6_11.GenWeight_*_skim.root"),   xs=4.412540e-05 * 2.941231e+02)
h.add("Bj_11_18_skim",  s3("Bj_11_18.GenWeight_*_skim.root"),  xs=6.978936e-05 * 2.595000e+01)
h.add("Bj_18_27_skim",  s3("Bj_18_27.GenWeight_*_skim.root"),  xs=8.790586e-05 * 2.421110e+00)
h.add("Bj_27_37_skim",  s3("Bj_27_37.GenWeight_*_skim.root"),  xs=9.602590e-05 * 2.269000e-01)
h.add("Bj_37_1k_skim",  s3("Bj_37_1k.GenWeight_*_skim.root"),  xs=1.008278e-04 * 2.767000e-02)
h.add("Bjj_0_7_skim",   s3("Bjj_0_7.GenWeight_*_skim.root"),   xs=8.740662e-06 * 8.645604e+01)
h.add("Bjj_7_14_skim",  s3("Bjj_7_14.GenWeight_*_skim.root"),  xs=3.370936e-05 * 4.348690e+00)
h.add("Bjj_14_23_skim", s3("Bjj_14_23.GenWeight_*_skim.root"), xs=4.185523e-05 * 3.246500e-01)
h.add("Bjj_23_34_skim", s3("Bjj_23_34.GenWeight_*_skim.root"), xs=5.746706e-05 * 3.032000e-02)
h.add("H_0_3_skim",     s3("H_0_3.GenWeight_*_skim.root"),     xs=1.365308e-05 * 2.155990e+01)
h.add("H_3_8_skim",     s3("H_3_8.GenWeight_*_skim.root"),     xs=1.347919e-04 * 1.112820e+00)
h.add("H_8_15_skim",    s3("H_8_15.GenWeight_*_skim.root"),    xs=3.698741e-04 * 9.188000e-02)
h.add("H_15_1k_skim",   s3("H_15_1k.GenWeight_*_skim.root"),   xs=2.543520e-04 * 1.009000e-02)
h.add("LL_0_1_skim",    s3("LL_0_1.GenWeight_*_skim.root"),    xs=3.359573e-07 * 1.341369e+03)
h.add("LL_1_2_skim",    s3("LL_1_2.GenWeight_*_skim.root"),    xs=2.076294e-06 * 1.562953e+02)
h.add("LL_2_5_skim",    s3("LL_2_5.GenWeight_*_skim.root"),    xs=2.646676e-05 * 4.240132e+01)
h.add("LL_5_9_skim",    s3("LL_5_9.GenWeight_*_skim.root"),    xs=6.271061e-05 * 2.843730e+00)
h.add("LL_9_14_skim",   s3("LL_9_14.GenWeight_*_skim.root"),   xs=1.107710e-04 * 2.091400e-01)
h.add("LL_14_1k_skim",  s3("LL_14_1k.GenWeight_*_skim.root"),  xs=1.449367e-04 * 2.891000e-02)
h.add("LLB_0_4_skim",   s3("LLB_0_4.GenWeight_*_skim.root"),   xs=9.010149e-06 * 2.973800e+00)
h.add("LLB_4_9_skim",   s3("LLB_4_9.GenWeight_*_skim.root"),   xs=5.645423e-05 * 2.285400e-01)
h.add("LLB_9_1k_skim",  s3("LLB_9_1k.GenWeight_*_skim.root"),  xs=8.180308e-05 * 2.080000e-02)
h.add("tB_0_5_skim",    s3("tB_0_5.GenWeight_*_skim.root"),    xs=3.615550e-04 * 6.388923e+01)
h.add("tB_5_9_skim",    s3("tB_5_9.GenWeight_*_skim.root"),    xs=1.347893e-03 * 7.121720e+00)
h.add("tB_9_15_skim",   s3("tB_9_15.GenWeight_*_skim.root"),   xs=2.275916e-03 * 9.803000e-01)
h.add("tB_15_22_skim",  s3("tB_15_22.GenWeight_*_skim.root"),  xs=2.968102e-03 * 8.391000e-02)
h.add("tB_22_1k_skim",  s3("tB_22_1k.GenWeight_*_skim.root"),  xs=3.360009e-03 * 9.530000e-03)
h.add("tj_0_5_skim",    s3("tj_0_5.GenWeight_*_skim.root"),    xs=1.162067e-04 * 1.097360e+02)
h.add("tj_5_10_skim",   s3("tj_5_10.GenWeight_*_skim.root"),   xs=5.661239e-04 * 5.993250e+00)
h.add("tj_10_16_skim",  s3("tj_10_16.GenWeight_*_skim.root"),  xs=1.150231e-03 * 3.768000e-01)
h.add("tj_16_24_skim",  s3("tj_16_24.GenWeight_*_skim.root"),  xs=1.477379e-03 * 3.462000e-02)
h.add("tj_24_1k_skim",  s3("tj_24_1k.GenWeight_*_skim.root"),  xs=1.664706e-03 * 3.120000e-03)
h.add("ttB_0_9_skim",   s3("ttB_0_9.GenWeight_*_skim.root"),   xs=2.054081e-03 * 2.667300e+00)
h.add("ttB_9_16_skim",  s3("ttB_9_16.GenWeight_*_skim.root"),  xs=4.952179e-03 * 2.504690e-01)
h.add("ttB_16_25_skim", s3("ttB_16_25.GenWeight_*_skim.root"), xs=6.425267e-03 * 2.374410e-02)
h.add("ttB_25_1k_skim", s3("ttB_25_1k.GenWeight_*_skim.root"), xs=7.166812e-03 * 2.088160e-03)
