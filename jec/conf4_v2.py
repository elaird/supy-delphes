import ROOT as r

f0 = r.TF1("f0", "(0.811397+((x<=80)*((0.00118455*(x-80))+(-8.54142e-05*sq(x-80)))))+((x>80)*((0.00213169*(x-80))+(-1.24026e-05*sq(x-80))))", 10, 170)
f1 = r.TF1("f1", "(1.36338+((x<=60)*((-0.00859917*(x-60))+(-0.000341591*sq(x-60)))))+((x>60)*((-0.00544275*(x-60))+(2.98166e-05*sq(x-60))))", 10, 190)
f2 = r.TF1("f2", "1.11514", 10, 80)
f3 = r.TF1("f3", "(0.738836+((x<=70)*((-0.000756009*(x-70))+(-0.000142038*sq(x-70)))))+((x>70)*((0.00423632*(x-70))+(-2.734e-05*sq(x-70))))", 10, 170)
f4 = r.TF1("f4", "(0.708548+((x<=60)*((0.00093057*(x-60))+(-0.000152454*sq(x-60)))))+((x>60)*((0.00416501*(x-60))+(-2.12554e-05*sq(x-60))))", 10, 190)
f5 = r.TF1("f5", "(0.771539+((x<=70)*((0.00160393*(x-70))+(-0.000105885*sq(x-70)))))+((x>70)*((0.00259237*(x-70))+(-1.23183e-05*sq(x-70))))", 10, 200)
f6 = r.TF1("f6", "(0.815597+((x<=80)*((0.000854313*(x-80))+(-8.19657e-05*sq(x-80)))))+((x>80)*((0.00180569*(x-80))+(-7.01866e-06*sq(x-80))))", 10, 200)
f7 = r.TF1("f7", "(0.848155+((x<=70)*((-0.00187487*(x-70))+(-0.000159604*sq(x-70)))))+((x>70)*((0.00286061*(x-70))+(-1.7379e-05*sq(x-70))))", 10, 200)
f8 = r.TF1("f8", "(1.02349+((x<=70)*((-0.000455128*(x-70))+(-0.000115069*sq(x-70)))))+((x>70)*((-0.000206354*(x-70))+(1.78891e-06*sq(x-70))))", 10, 170)
f9 = r.TF1("f9", "(1.21498+((x<=50)*((-0.0146829*(x-50))+(-0.000738146*sq(x-50)))))+((x>50)*((-0.00226167*(x-50))+(1.5194e-05*sq(x-50))))", 10, 190)
f10 = r.TF1("f10", "(1.39735+((x<=60)*((-0.0198145*(x-60))+(-0.000684695*sq(x-60)))))+((x>60)*((-0.00441638*(x-60))+(1.97248e-05*sq(x-60))))", 10, 200)
f11 = r.TF1("f11", "(1.39433+((x<=50)*((-0.0377563*(x-50))+(-0.00133566*sq(x-50)))))+((x>50)*((-0.00207763*(x-50))+(2.87396e-06*sq(x-50))))", 10, 200)

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

                                                
