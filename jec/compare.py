#!/usr/bin/env python

import ROOT as r
r.gErrorIgnoreLevel = 2000

def etas(nEta=10, min=0.0, max=3.0, offset=0.1):
    out = []
    for iEta in range(1 + nEta):
        eta = offset + min + (max-min)*iEta/(0.0 + nEta)
        out.append(eta)
    return out


def drawFuncs(iEta=None, eta=None, leg=None):
    out = []
    for iModule, ((d, module), label) in enumerate(sorted(modules.iteritems())):
        func = getattr(eval(module), "f")(eta).Clone("func_%d_%d_%s" % (iEta, iModule, module))
        func.SetLineColor(1 + iModule)
        if iModule:
            func.Draw("same")
        else:
            func.Draw()
            h = func.GetHistogram()
            h.GetYaxis().SetRangeUser(0.0, 2.0)
            h.SetTitle("#eta = %g; uncorrected jet p_{T} (GeV);1.0 / (correction factor)" % eta)
        if not iEta:
            leg.AddEntry(func, label, "l")
        out.append(func)
    leg.Draw()
    return out


def makePdf(pdf="compared.pdf", multi=None):
    canvas = r.TCanvas()
    canvas.SetTickx()
    canvas.SetTicky()

    canvas.Print(pdf+"[")
    funcs = []
    for iEta, eta in enumerate(etas()):
        if not iEta:
            leg = r.TLegend(0.5, 0.60, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)

        if multi:
            jEta = iEta % 4
            if not jEta:
                canvas.cd(0)
                canvas.Clear()
                canvas.Divide(2, 2)

            canvas.cd(1 + jEta)
            r.gPad.SetTickx()
            r.gPad.SetTicky()

        funcs += drawFuncs(iEta, eta, leg)

        if multi:
            if jEta == 3:
                canvas.Print(pdf)
        else:
            canvas.Print(pdf)

    if multi and jEta != 3:
        canvas.Print(pdf)
    canvas.Print(pdf+"]")


modules = {("c4", "hb_bPtMin0_012matches"): "0 < b-quark p_{T} (h/012m)",
           ("c4", "hh_bPtMin0_2matches"): "0 < b-quark p_{T} (hh/2m)",
           ("c4", "hh_bPtMin0_012matches"): "0 < b-quark p_{T} (hh/012m)",
           ("c4", "hb_bPtMin30_012matches"): "30 < b-quark p_{T} (h/012m)",
           #"conf4_v2_hb_genJetPtMin30_012matches": "30 < b-gen-jet p_{T} (h)",

           #"conf4_v2_hg_gPtMin0_012matches": "0 < gluon p_{T} (h)",
           #"conf4_v2_hg_gPtMin30_012matches": "30 < gluon p_{T} (h)",

           #"conf4_v2_h_genJetPtMin30_012matches":  "30 < gen-jet p_{T} (h/c4v2)",
           ##"conf4_v2_h_2b_genJetPtMin30_012matches_lowstats":  "30 < gen-jet p_{T} (h2b ls/c4v2)",

           #"conf4_v2_qcd_genJetPtMin30_012matches_v2": "30 < gen-jet p_{T} (qcd)",

           #"conf4_b_bPtMin0_2matches": "0 < b-quark p_{T} (hh/2m/1)",
           #"conf0_b_v3": "0 < b-quark p_{T} (conf0)",
           #"conf4_b_bPtMin0_012matches": "0 < b-quark p_{T} (old)",
           #"conf4_hb_bPtMin0_012matches_70": "0 < b-quark p_{T} (h/c4/70)",
           #"conf4_hb_bPtMin30_012matches": "30 < b-quark p_{T} (h/c4/70)",
           ##"conf4_hb_bPtMin30_012matches_80": "30 < b-quark p_{T} (h/c4/80)",
           #"conf4_b_bPtMin0_012matches_v2": "0 < b-quark p_{T} (hh/c4)",
           ##"conf4_b_bPtMin10_012matches": "10 < b-quark p_{T}",
           ##"conf4_b_bPtMin20_012matches": "20 < b-quark p_{T}",
           ###"conf4_b_bPtMin30_012matches": "30 < b-quark p_{T} (old)",
           #"conf4_b_bPtMin30_012matches_v2": "30 < b-quark p_{T} (hh/c4)",
           ##"conf4_b_bPtMin30_2matches": "30 < b-quark p_{T}",
           #"conf4_b_genJetPtMin20_012matches": "20 < b-gen-jet p_{T}",
           #"conf4_b_genJetPtMin30_012matches": "30 < b-gen-jet p_{T}",
           }

for d, module in modules.keys():
    exec("from %s import %s" % (d, module))


makePdf(multi=True)
