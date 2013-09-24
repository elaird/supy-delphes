import ROOT as r


f0 = r.TF1("f0", "(0.977774+((x<=70)*((0.00495066*(x-70))+(-0.000125161*sq(x-70)))))+((x>70)*((-0.000446044*(x-70))+(1.00553e-05*sq(x-70))))", 20, 200)
f1 = r.TF1("f1", "(0.98002+((x<=70)*((0.00382356*(x-70))+(-0.000129123*sq(x-70)))))+((x>70)*((5.04457e-05*(x-70))+(-2.33491e-06*sq(x-70))))", 20, 200)
f2 = r.TF1("f2", "0.302477+(0.0125511*x)", 20, 80)
f3 = r.TF1("f3", "(0.950389+((x<=70)*((0.004003*(x-70))+(-0.000131327*sq(x-70)))))+((x>70)*((0.000592387*(x-70))+(-5.37287e-07*sq(x-70))))", 20, 200)
f4 = r.TF1("f4", "(0.933785+((x<=70)*((0.0035442*(x-70))+(-0.000135495*sq(x-70)))))+((x>70)*((0.000374798*(x-70))+(2.04044e-06*sq(x-70))))", 20, 200)
f5 = r.TF1("f5", "(0.908816+((x<=70)*((0.00275929*(x-70))+(-0.000143651*sq(x-70)))))+((x>70)*((0.000226645*(x-70))+(5.81143e-06*sq(x-70))))", 20, 200)
f6 = r.TF1("f6", "(0.8941+((x<=70)*((0.00185089*(x-70))+(-0.000150911*sq(x-70)))))+((x>70)*((0.000567875*(x-70))+(3.18062e-06*sq(x-70))))", 20, 200)
f7 = r.TF1("f7", "(0.942515+((x<=70)*((0.00338675*(x-70))+(-0.000131684*sq(x-70)))))+((x>70)*((-0.000490624*(x-70))+(9.30842e-06*sq(x-70))))", 20, 200)
f8 = r.TF1("f8", "(0.99625+((x<=70)*((0.00416463*(x-70))+(-0.000130387*sq(x-70)))))+((x>70)*((-0.000593714*(x-70))+(7.09871e-06*sq(x-70))))", 20, 200)
f9 = r.TF1("f9", "(1.02314+((x<=70)*((0.00395631*(x-70))+(-0.000141639*sq(x-70)))))+((x>70)*((-0.000815672*(x-70))+(6.19041e-06*sq(x-70))))", 20, 200)
f10 = r.TF1("f10", "(1.01568+((x<=70)*((0.00333596*(x-70))+(-0.000155002*sq(x-70)))))+((x>70)*((-0.0015344*(x-70))+(1.26335e-05*sq(x-70))))", 20, 200)
f11 = r.TF1("f11", "(1.01001+((x<=70)*((0.00454556*(x-70))+(-0.00011594*sq(x-70)))))+((x>70)*((-0.00106893*(x-70))+(1.1073e-05*sq(x-70))))", 20, 200)


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