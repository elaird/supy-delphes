import ROOT as r


f0 = r.TF1("f0", "(1.17182+((x<=70)*((0.00620839*(x-70))+(-8.04405e-05*sq(x-70)))))+((x>70)*((-0.00105105*(x-70))+(-9.66743e-06*sq(x-70))))", 20, 150)
f1 = r.TF1("f1", "(1.11024+((x<=70)*((-0.00141803*(x-70))+(-0.00017703*sq(x-70)))))+((x>70)*((-0.00270522*(x-70))+(1.60267e-05*sq(x-70))))", 20, 160)
f2 = r.TF1("f2", "(0.946644+((x<=70)*((-0.0241034*(x-70))+(-0.000580629*sq(x-70)))))+((x>70)*((-0.00213426*(x-70))+(-8.53704e-05*sq(x-70))))", 20, 100)
f3 = r.TF1("f3", "(1.14312+((x<=70)*((0.00298619*(x-70))+(-0.00014662*sq(x-70)))))+((x>70)*((0.00142062*(x-70))+(-5.64529e-05*sq(x-70))))", 20, 150)
f4 = r.TF1("f4", "(1.17616+((x<=70)*((0.0103916*(x-70))+(9.40558e-06*sq(x-70)))))+((x>70)*((-0.00332452*(x-70))+(4.10281e-06*sq(x-70))))", 20, 150)
f5 = r.TF1("f5", "(1.11684+((x<=70)*((0.00754614*(x-70))+(-2.88661e-05*sq(x-70)))))+((x>70)*((-0.0059777*(x-70))+(5.64188e-05*sq(x-70))))", 20, 150)
f6 = r.TF1("f6", "(1.09919+((x<=70)*((0.00601022*(x-70))+(-6.11236e-05*sq(x-70)))))+((x>70)*((-0.00566611*(x-70))+(5.06231e-05*sq(x-70))))", 20, 150)
f7 = r.TF1("f7", "(1.16165+((x<=70)*((0.0076101*(x-70))+(-2.0872e-05*sq(x-70)))))+((x>70)*((-0.0106432*(x-70))+(0.000102381*sq(x-70))))", 20, 150)
f8 = r.TF1("f8", "(1.16879+((x<=70)*((0.0049749*(x-70))+(-4.09652e-05*sq(x-70)))))+((x>70)*((-0.000941672*(x-70))+(-3.15529e-05*sq(x-70))))", 20, 150)
f9 = r.TF1("f9", "(1.24779+((x<=70)*((0.00677584*(x-70))+(-3.2442e-05*sq(x-70)))))+((x>70)*((-0.00647167*(x-70))+(4.08205e-05*sq(x-70))))", 20, 150)
f10 = r.TF1("f10", "(1.2091+((x<=70)*((-0.00179252*(x-70))+(-0.000177797*sq(x-70)))))+((x>70)*((-0.000203058*(x-70))+(-6.29801e-05*sq(x-70))))", 20, 150)
f11 = r.TF1("f11", "(1.17716+((x<=70)*((0.000869302*(x-70))+(-0.000116066*sq(x-70)))))+((x>70)*((-0.00172743*(x-70))+(-2.74413e-05*sq(x-70))))", 20, 150)


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
