import ROOT as r


f0 = r.TF1("f0", "(0.783053+((x<=80)*((-0.0027513*(x-80))+(-0.000156868*sq(x-80)))))+((x>80)*((0.00196585*(x-80))+(-7.74296e-06*sq(x-80))))", 20, 200)
f1 = r.TF1("f1", "(1.27932+((x<=80)*((0.00536863*(x-80))+(-0.000120417*sq(x-80)))))+((x>80)*((-0.000300579*(x-80))+(-1.78436e-05*sq(x-80))))", 20, 200)
f2 = r.TF1("f2", "0.297283+(0.0136803*x)", 20, 80)
f3 = r.TF1("f3", "(0.783408+((x<=80)*((-0.00307049*(x-80))+(-0.000162231*sq(x-80)))))+((x>80)*((0.00160469*(x-80))+(-6.62244e-06*sq(x-80))))", 20, 200)
f4 = r.TF1("f4", "(0.787355+((x<=80)*((-0.00222567*(x-80))+(-0.000146615*sq(x-80)))))+((x>80)*((0.00159571*(x-80))+(-6.13655e-06*sq(x-80))))", 20, 200)
f5 = r.TF1("f5", "(0.78731+((x<=80)*((-0.00226055*(x-80))+(-0.000147114*sq(x-80)))))+((x>80)*((0.00170577*(x-80))+(-7.21308e-06*sq(x-80))))", 20, 200)
f6 = r.TF1("f6", "(0.811937+((x<=80)*((-0.00270262*(x-80))+(-0.000156959*sq(x-80)))))+((x>80)*((0.00160971*(x-80))+(-8.36644e-06*sq(x-80))))", 20, 200)
f7 = r.TF1("f7", "(0.911233+((x<=80)*((-0.00154186*(x-80))+(-0.000156294*sq(x-80)))))+((x>80)*((-0.000789444*(x-80))+(1.28179e-05*sq(x-80))))", 20, 200)
f8 = r.TF1("f8", "(1.09771+((x<=80)*((0.00187437*(x-80))+(-0.000140552*sq(x-80)))))+((x>80)*((-0.0020198*(x-80))+(1.28968e-05*sq(x-80))))", 20, 200)
f9 = r.TF1("f9", "(1.25681+((x<=80)*((0.00482983*(x-80))+(-0.00012644*sq(x-80)))))+((x>80)*((-0.00280318*(x-80))+(9.34238e-06*sq(x-80))))", 20, 200)
f10 = r.TF1("f10", "(1.34574+((x<=80)*((0.00646915*(x-80))+(-0.000127908*sq(x-80)))))+((x>80)*((-0.00196531*(x-80))+(-3.01206e-06*sq(x-80))))", 20, 200)
f11 = r.TF1("f11", "(1.32687+((x<=80)*((0.00567491*(x-80))+(-0.000125845*sq(x-80)))))+((x>80)*((0.000553704*(x-80))+(-2.64867e-05*sq(x-80))))", 20, 200)


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
