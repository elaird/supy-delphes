import ROOT as r


f0 = r.TF1("f0", "(1.58359+((x<=70)*((0.00154874*(x-70))+(-0.000301497*sq(x-70)))))+((x>70)*((0.000265637*(x-70))+(-8.82874e-05*sq(x-70))))", 20, 150)
f1 = r.TF1("f1", "(1.27819+((x<=70)*((-0.0127945*(x-70))+(-0.000448995*sq(x-70)))))+((x>70)*((-0.00477175*(x-70))+(2.27008e-05*sq(x-70))))", 20, 150)
f2 = r.TF1("f2", "(1.73585+((x<=70)*((0.00213021*(x-70))+(-0.000331731*sq(x-70)))))+((x>70)*((0.00429309*(x-70))+(-2.98565e-05*sq(x-70))))", 20, 100)
f3 = r.TF1("f3", "(1.50814+((x<=70)*((-0.000964408*(x-70))+(-0.000321489*sq(x-70)))))+((x>70)*((-0.0012071*(x-70))+(-4.43099e-05*sq(x-70))))", 20, 150)
f4 = r.TF1("f4", "(1.41713+((x<=70)*((-0.00370544*(x-70))+(-0.000342755*sq(x-70)))))+((x>70)*((-0.00324066*(x-70))+(-2.35496e-05*sq(x-70))))", 20, 150)
f5 = r.TF1("f5", "(1.31492+((x<=70)*((-0.0067359*(x-70))+(-0.000365361*sq(x-70)))))+((x>70)*((-0.0020148*(x-70))+(-2.8371e-05*sq(x-70))))", 20, 150)
f6 = r.TF1("f6", "(1.22753+((x<=70)*((-0.0103663*(x-70))+(-0.00039915*sq(x-70)))))+((x>70)*((-0.00321777*(x-70))+(4.7043e-06*sq(x-70))))", 20, 150)
f7 = r.TF1("f7", "(1.28707+((x<=70)*((-0.0101049*(x-70))+(-0.000405234*sq(x-70)))))+((x>70)*((-0.00577395*(x-70))+(3.12329e-05*sq(x-70))))", 20, 150)
f8 = r.TF1("f8", "(1.37351+((x<=70)*((-0.0106375*(x-70))+(-0.000436513*sq(x-70)))))+((x>70)*((-0.00604205*(x-70))+(1.88093e-05*sq(x-70))))", 20, 150)
f9 = r.TF1("f9", "(1.44063+((x<=70)*((-0.00992323*(x-70))+(-0.000439959*sq(x-70)))))+((x>70)*((-0.00194622*(x-70))+(-3.08304e-05*sq(x-70))))", 20, 150)
f10 = r.TF1("f10", "(1.44917+((x<=70)*((-0.0101426*(x-70))+(-0.000447119*sq(x-70)))))+((x>70)*((-0.00509647*(x-70))+(3.03862e-05*sq(x-70))))", 20, 150)
f11 = r.TF1("f11", "(1.44521+((x<=70)*((-0.00956115*(x-70))+(-0.000436366*sq(x-70)))))+((x>70)*((-0.0091099*(x-70))+(5.74112e-05*sq(x-70))))", 20, 150)


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
