import ROOT as r


f0 = r.TF1("f0", "1.0", 20, 200)

def f(eta):
    return f0
