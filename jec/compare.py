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
    for iModule, (module, label) in enumerate(sorted(modules.iteritems())):
        func = getattr(eval(module), "f")(eta).Clone("func_%d_%d_%s" % (iEta, iModule, module))
        func.SetLineColor(1 + iModule)
        if iModule:
            func.Draw("same")
        else:
            func.Draw()
            h = func.GetHistogram()
            h.GetYaxis().SetRangeUser(0.0, 2.0)
            h.SetTitle("#eta = %g; uncorrected jet p_{T} (GeV); correction factor" % eta)
        if not iEta:
            leg.AddEntry(func, label, "l")
        out.append(func)
    leg.Draw()
    return out


def makePdf(pdf="compared.pdf"):
    canvas = r.TCanvas()
    canvas.Print(pdf+"[")
    funcs = []
    for iEta, eta in enumerate(etas()):
        if not iEta:
            leg = r.TLegend(0.5, 0.60, 0.85, 0.85)
            leg.SetBorderSize(0)
            leg.SetFillStyle(0)

        jEta = iEta % 4
        if not jEta:
            canvas.cd(0)
            canvas.Clear()
            canvas.Divide(2, 2)

        canvas.cd(1 + jEta)
        r.gPad.SetTickx()
        r.gPad.SetTicky()

        funcs += drawFuncs(iEta, eta, leg)

        if jEta == 3:
            canvas.Print(pdf)

    if jEta != 3:
        canvas.Print(pdf)
    canvas.Print(pdf+"]")

modules = {#"conf4_b_bptMin0_2matches": "0 < b-quark p_{T}",
           "conf4_b_bPtMin0_012matches": "0 < b-quark p_{T}",
           "conf4_b_bPtMin10_012matches": "10 < b-quark p_{T}",
           "conf4_b_bPtMin20_012matches": "20 < b-quark p_{T}",
           "conf4_b_bPtMin30_012matches": "30 < b-quark p_{T}",
           #"conf4_b_bPtMin30_2matches": "30 < b-quark p_{T}",
           "conf4_b_genJetPtMin20_012matches": "20 < b-gen-jet p_{T}",
           "conf4_b_genJetPtMin30_012matches": "30 < b-gen-jet p_{T}",
           #"conf4_j_v1": "30 < j gen-jet p_{T}",
           }

for module in modules.keys():
    exec("import %s" % module)


makePdf()
