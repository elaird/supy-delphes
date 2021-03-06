import ROOT as r


f0 = r.TF1("f0", "(0.691807+((x<=70)*((0.000566243*(x-70))+(-0.000123059*sq(x-70)))))+((x>70)*((0.00661868*(x-70))+(-7.11021e-05*sq(x-70))))", 10, 150)
f1 = r.TF1("f1", "(1.07537+((x<=60)*((-0.0429949*(x-60))+(-0.00107276*sq(x-60)))))+((x>60)*((0.00369977*(x-60))+(-9.7195e-05*sq(x-60))))", 10, 120)
#f2 = r.TF1("f2", "(-0.168475+((x<=60)*((-0.108929*(x-60))+(-0.00160235*sq(x-60)))))+((x>60)*((0.0367583*(x-60))+(-0.00061264*sq(x-60))))", 10, 120)
f3 = r.TF1("f3", "(0.644832+((x<=60)*((0.00256496*(x-60))+(-0.000102457*sq(x-60)))))+((x>60)*((0.00503381*(x-60))+(-2.19516e-05*sq(x-60))))", 10, 120)
f4 = r.TF1("f4", "(0.655989+((x<=60)*((0.0033246*(x-60))+(-9.72304e-05*sq(x-60)))))+((x>60)*((0.00512*(x-60))+(-5.9171e-05*sq(x-60))))", 10, 120)
f5 = r.TF1("f5", "(0.71524+((x<=70)*((0.00517581*(x-70))+(-3.50665e-05*sq(x-70)))))+((x>70)*((0.00502437*(x-70))+(-4.5666e-05*sq(x-70))))", 10, 170)
f6 = r.TF1("f6", "(0.656024+((x<=60)*((4.08174e-05*(x-60))+(-0.000152504*sq(x-60)))))+((x>60)*((0.00593933*(x-60))+(-8.21211e-05*sq(x-60))))", 10, 120)
f7 = r.TF1("f7", "(0.681725+((x<=60)*((0.00044069*(x-60))+(-0.000123924*sq(x-60)))))+((x>60)*((0.00926202*(x-60))+(-0.000105806*sq(x-60))))", 10, 120)
f8 = r.TF1("f8", "(0.781144+((x<=60)*((-0.011046*(x-60))+(-0.000354183*sq(x-60)))))+((x>60)*((0.0114579*(x-60))+(-0.000153075*sq(x-60))))", 10, 120)
f9 = r.TF1("f9", "(1.14781+((x<=50)*((0.00436381*(x-50))+(-0.000107552*sq(x-50)))))+((x>50)*((-0.00435978*(x-50))+(6.16526e-05*sq(x-50))))", 10, 120)
f10 = r.TF1("f10", "(1.18812+((x<=60)*((-0.0190359*(x-60))+(-0.000606743*sq(x-60)))))+((x>60)*((0.00255661*(x-60))+(-1.33593e-05*sq(x-60))))", 10, 120)
f11 = r.TF1("f11", "(1.39002+((x<=50)*((-0.00765888*(x-50))+(-0.000677937*sq(x-50)))))+((x>50)*((0.00339752*(x-50))+(-0.000138647*sq(x-50))))", 10, 120)


def f(eta):
    if abs(eta) <= 0.3:
        return f0
    if 3.0 < abs(eta) <= 4.0:
        return f1
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
