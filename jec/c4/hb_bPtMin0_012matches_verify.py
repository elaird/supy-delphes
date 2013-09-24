import ROOT as r


f0 = r.TF1("f0", "(1.03148+((x<=70)*((0.00606388*(x-70))+(-7.24091e-05*sq(x-70)))))+((x>70)*((-0.00051538*(x-70))+(1.60389e-06*sq(x-70))))", 20, 200)
f1 = r.TF1("f1", "(1.06117+((x<=70)*((0.00634479*(x-70))+(-1.35962e-05*sq(x-70)))))+((x>70)*((-0.00245875*(x-70))+(1.53873e-05*sq(x-70))))", 20, 200)
f2 = r.TF1("f2", "1.22085+(0.000569048*x)", 20, 80)
f3 = r.TF1("f3", "(1.01829+((x<=70)*((0.00595913*(x-70))+(-7.21467e-05*sq(x-70)))))+((x>70)*((-0.00146485*(x-70))+(1.13159e-05*sq(x-70))))", 20, 200)
f4 = r.TF1("f4", "(0.976294+((x<=70)*((0.00374374*(x-70))+(-0.000106641*sq(x-70)))))+((x>70)*((-0.000692663*(x-70))+(6.32258e-06*sq(x-70))))", 20, 200)
f5 = r.TF1("f5", "(0.957584+((x<=70)*((0.00332645*(x-70))+(-0.00010981*sq(x-70)))))+((x>70)*((-0.00064533*(x-70))+(6.36904e-06*sq(x-70))))", 20, 200)
f6 = r.TF1("f6", "(0.965827+((x<=70)*((0.00406477*(x-70))+(-8.9749e-05*sq(x-70)))))+((x>70)*((-0.00130846*(x-70))+(1.19394e-05*sq(x-70))))", 20, 200)
f7 = r.TF1("f7", "(0.993769+((x<=70)*((0.00383575*(x-70))+(-9.05845e-05*sq(x-70)))))+((x>70)*((-0.00136656*(x-70))+(1.11532e-05*sq(x-70))))", 20, 200)
f8 = r.TF1("f8", "(1.0485+((x<=70)*((0.00547339*(x-70))+(-3.35327e-05*sq(x-70)))))+((x>70)*((-0.0017146*(x-70))+(1.01709e-05*sq(x-70))))", 20, 200)
f9 = r.TF1("f9", "(1.07795+((x<=70)*((0.00573695*(x-70))+(-1.63019e-05*sq(x-70)))))+((x>70)*((-0.00187884*(x-70))+(1.19898e-05*sq(x-70))))", 20, 200)
f10 = r.TF1("f10", "(1.1042+((x<=70)*((0.00823805*(x-70))+(4.51224e-05*sq(x-70)))))+((x>70)*((-0.00194893*(x-70))+(9.50269e-06*sq(x-70))))", 20, 200)
f11 = r.TF1("f11", "(1.08863+((x<=70)*((0.008907*(x-70))+(8.36722e-05*sq(x-70)))))+((x>70)*((-0.00300359*(x-70))+(1.81358e-05*sq(x-70))))", 20, 200)


def f(eta):
    if abs(eta) <= 0.3:
        return f0
    if 3.0 < abs(eta) <= 4.0:
        return f1
    if 4.0 < abs(eta):
        return f2
    if 0.3 < abs(eta) <= 0.6:
        return f3
    if 0.6 < abs(eta) <= 0.9:
        return f4
    if 0.9 < abs(eta) <= 1.2:
        return f5
    if 1.2 < abs(eta) <= 1.5:
        return f6
    if 1.5 < abs(eta) <= 1.8:
        return f7
    if 1.8 < abs(eta) <= 2.1:
        return f8
    if 2.1 < abs(eta) <= 2.4:
        return f9
    if 2.4 < abs(eta) <= 2.7:
        return f10
    if 2.7 < abs(eta) <= 3.0:
        return f11
