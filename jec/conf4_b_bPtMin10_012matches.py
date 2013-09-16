import ROOT as r


f0 = r.TF1("f0", "(0.747247+((x<=70)*((0.00314894*(x-70))+(-5.73004e-05*sq(x-70)))))+((x>70)*((0.00201439*(x-70))+(-5.80606e-06*sq(x-70))))", 20, 200)
f1 = r.TF1("f1", "(1.25852+((x<=70)*((-0.00495821*(x-70))+(-0.000279047*sq(x-70)))))+((x>70)*((-0.00035314*(x-70))+(-2.30123e-05*sq(x-70))))", 20, 160)
f2 = r.TF1("f2", "0.94399", 20, 80)
f3 = r.TF1("f3", "(0.73145+((x<=70)*((0.00233005*(x-70))+(-7.5057e-05*sq(x-70)))))+((x>70)*((0.00238325*(x-70))+(-8.23146e-06*sq(x-70))))", 20, 200)
f4 = r.TF1("f4", "(0.730644+((x<=70)*((0.00287246*(x-70))+(-5.80231e-05*sq(x-70)))))+((x>70)*((0.00257626*(x-70))+(-9.51226e-06*sq(x-70))))", 20, 200)
f5 = r.TF1("f5", "(0.745379+((x<=70)*((0.00364529*(x-70))+(-4.3464e-05*sq(x-70)))))+((x>70)*((0.0021202*(x-70))+(-7.2875e-06*sq(x-70))))", 20, 200)
f6 = r.TF1("f6", "(0.767124+((x<=70)*((0.002265*(x-70))+(-7.44179e-05*sq(x-70)))))+((x>70)*((0.0017952*(x-70))+(-4.34294e-06*sq(x-70))))", 20, 200)
f7 = r.TF1("f7", "(0.846047+((x<=70)*((0.00352169*(x-70))+(-3.37399e-05*sq(x-70)))))+((x>70)*((0.00110731*(x-70))+(-1.31516e-06*sq(x-70))))", 20, 200)
f8 = r.TF1("f8", "(0.98901+((x<=70)*((-0.000624989*(x-70))+(-0.00014166*sq(x-70)))))+((x>70)*((0.000408073*(x-70))+(-1.7788e-06*sq(x-70))))", 20, 200)
f9 = r.TF1("f9", "(1.18774+((x<=70)*((-0.000158729*(x-70))+(-0.000110828*sq(x-70)))))+((x>70)*((-0.00269646*(x-70))+(1.61521e-05*sq(x-70))))", 20, 200)
f10 = r.TF1("f10", "(1.25201+((x<=70)*((-0.0100167*(x-70))+(-0.000357494*sq(x-70)))))+((x>70)*((-0.00179496*(x-70))+(5.75864e-06*sq(x-70))))", 20, 200)
f11 = r.TF1("f11", "(1.26818+((x<=70)*((-0.00854645*(x-70))+(-0.000319285*sq(x-70)))))+((x>70)*((-0.0026802*(x-70))+(1.3132e-05*sq(x-70))))", 20, 200)


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