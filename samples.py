import supy
from units import pb, fb

holder = supy.samples.SampleHolder()
holder.add("tt_test", '["/tmp/elaird/ttbar140PU_Phase2.root"]', xs=500*pb)
holder.add("tt.conf0_0_600", '["root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/upgrade/PhaseI/Configuration0/140PileUp/tt-4p-0-600-v1510_14TEV/tt-4p-0-600-v1510_14TEV_354724341_PhaseI_Conf0_140PileUp.root"]', xs=500*pb)

conf3 = "root://eoscms.cern.ch//eos/cms/store/group/phys_higgs/upgrade/PhaseII/Configuration3/140PileUp"
holder.add("tt.conf3_0_600",
           '["%s/tt-4p-0-600-v1510_14TEV/tt-4p-0-600-v1510_14TEV_102886267_PhaseII_Conf3_140PileUp.root"]' % conf3,
           xs=530.89358*pb)

holder.add("tt.conf3_600_1100",
           '["%s/tt-4p-600-1100-v1510_14TEV/tt-4p-600-1100-v1510_14TEV_101308277_PhaseII_Conf3_140PileUp.root"]' % conf3,
           xs=42.55351*pb)

holder.add("tt.conf3_1100_1700",
           '["%s/tt-4p-1100-1700-v1510_14TEV/tt-4p-1100-1700-v1510_14TEV_102571082_PhaseII_Conf3_140PileUp.root"]' % conf3,
           xs=4.48209*pb)

holder.add("tt.conf3_1700_2500",
           '["%s/tt-4p-1700-2500-v1510_14TEV/tt-4p-1700-2500-v1510_14TEV_100102772_PhaseII_Conf3_140PileUp.root"]' % conf3,
           xs=0.52795*pb)

holder.add("tt.conf3_2500_100000",
           '["%s/tt-4p-2500-100000-v1510_14TEV/tt-4p-2500-100000-v1510_14TEV_102665566_PhaseII_Conf3_140PileUp.root"]' % conf3,
           xs=0.05449*pb)

holder.add("hh_bbtt.conf3",
           '[%s]' % ",".join(['\"%s/GluGluToHHToBBTT_14TeV/GluGluToHHToBBTT_14TeV_%d.root\"' % (conf3, i) for i in range(4)]),
           xs=40.0*fb)
