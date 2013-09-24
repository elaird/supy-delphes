import ROOT as r


f0 = r.TF1("f0", "(0.908687+((x<=70)*((0.00173453*(x-70))+(-7.81915e-05*sq(x-70)))))+((x>70)*((0.00111627*(x-70))+(-2.45934e-06*sq(x-70))))", 20, 200)
f1 = r.TF1("f1", "(0.995416+((x<=70)*((0.000525062*(x-70))+(-7.53383e-05*sq(x-70)))))+((x>70)*((-0.00173309*(x-70))+(1.99095e-05*sq(x-70))))", 20, 200)
f2 = r.TF1("f2", "1.37016+(-0.00388576*x)", 20, 80)
f3 = r.TF1("f3", "(0.877923+((x<=70)*((-0.00032697*(x-70))+(-0.000127688*sq(x-70)))))+((x>70)*((0.00190198*(x-70))+(-8.72258e-06*sq(x-70))))", 20, 200)
f4 = r.TF1("f4", "(0.863945+((x<=70)*((-0.000571671*(x-70))+(-0.000121751*sq(x-70)))))+((x>70)*((0.0018087*(x-70))+(-6.84975e-06*sq(x-70))))", 20, 200)
f5 = r.TF1("f5", "(0.869725+((x<=70)*((0.00238394*(x-70))+(-6.56449e-05*sq(x-70)))))+((x>70)*((0.00111695*(x-70))+(-1.84572e-06*sq(x-70))))", 20, 200)
f6 = r.TF1("f6", "(0.856435+((x<=70)*((0.00074261*(x-70))+(-8.46967e-05*sq(x-70)))))+((x>70)*((0.00139733*(x-70))+(-3.8633e-06*sq(x-70))))", 20, 200)
f7 = r.TF1("f7", "(0.901415+((x<=70)*((0.00167946*(x-70))+(-3.49279e-05*sq(x-70)))))+((x>70)*((0.000931254*(x-70))+(-2.08371e-06*sq(x-70))))", 20, 200)
f8 = r.TF1("f8", "(0.946839+((x<=70)*((-0.000241775*(x-70))+(-8.15287e-05*sq(x-70)))))+((x>70)*((0.000615484*(x-70))+(-1.45062e-06*sq(x-70))))", 20, 200)
f9 = r.TF1("f9", "(0.986914+((x<=70)*((7.10464e-05*(x-70))+(-1.15233e-05*sq(x-70)))))+((x>70)*((-0.000154348*(x-70))+(4.97105e-06*sq(x-70))))", 20, 200)
f10 = r.TF1("f10", "(1.0004+((x<=70)*((0.00175737*(x-70))+(3.54187e-06*sq(x-70)))))+((x>70)*((1.83003e-05*(x-70))+(2.74014e-06*sq(x-70))))", 20, 200)
f11 = r.TF1("f11", "(0.978671+((x<=70)*((-0.00119691*(x-70))+(-7.49029e-05*sq(x-70)))))+((x>70)*((-0.000565139*(x-70))+(9.66633e-06*sq(x-70))))", 20, 200)


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