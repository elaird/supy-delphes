import ROOT as r


f0 = r.TF1("f0", "(0.736072+((x<=70)*((0.0024959*(x-70))+(-6.83544e-05*sq(x-70)))))+((x>70)*((0.00247174*(x-70))+(-8.56342e-06*sq(x-70))))", 20, 200)
f1 = r.TF1("f1", "(1.25744+((x<=70)*((-0.00155586*(x-70))+(-0.00026829*sq(x-70)))))+((x>70)*((-0.00115363*(x-70))+(-1.26296e-05*sq(x-70))))", 20, 160)
f2 = r.TF1("f2", "0.92257", 20, 80)
f3 = r.TF1("f3", "(0.729563+((x<=70)*((0.00202521*(x-70))+(-8.36146e-05*sq(x-70)))))+((x>70)*((0.00243814*(x-70))+(-7.87243e-06*sq(x-70))))", 20, 200)
f4 = r.TF1("f4", "(0.729232+((x<=70)*((0.00247617*(x-70))+(-6.87059e-05*sq(x-70)))))+((x>70)*((0.00273447*(x-70))+(-1.03072e-05*sq(x-70))))", 20, 200)
f5 = r.TF1("f5", "(0.743244+((x<=70)*((0.00341859*(x-70))+(-4.9976e-05*sq(x-70)))))+((x>70)*((0.00225501*(x-70))+(-7.9423e-06*sq(x-70))))", 20, 200)
f6 = r.TF1("f6", "(0.773933+((x<=70)*((0.00290553*(x-70))+(-6.66628e-05*sq(x-70)))))+((x>70)*((0.00179542*(x-70))+(-4.49524e-06*sq(x-70))))", 20, 200)
f7 = r.TF1("f7", "(0.832735+((x<=70)*((0.00219822*(x-70))+(-6.74964e-05*sq(x-70)))))+((x>70)*((0.00162096*(x-70))+(-4.17185e-06*sq(x-70))))", 20, 200)
f8 = r.TF1("f8", "(0.982919+((x<=70)*((-0.000978201*(x-70))+(-0.000170917*sq(x-70)))))+((x>70)*((0.000626606*(x-70))+(-2.77055e-06*sq(x-70))))", 20, 200)
f9 = r.TF1("f9", "(1.18093+((x<=70)*((0.00170642*(x-70))+(-0.000135377*sq(x-70)))))+((x>70)*((-0.00230292*(x-70))+(1.29571e-05*sq(x-70))))", 20, 200)
f10 = r.TF1("f10", "(1.22868+((x<=70)*((-0.00481173*(x-70))+(-0.000297504*sq(x-70)))))+((x>70)*((-0.00126188*(x-70))+(4.06016e-06*sq(x-70))))", 20, 200)
f11 = r.TF1("f11", "(1.26017+((x<=70)*((-0.00767176*(x-70))+(-0.000427196*sq(x-70)))))+((x>70)*((-0.00207816*(x-70))+(8.71652e-06*sq(x-70))))", 20, 200)


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
