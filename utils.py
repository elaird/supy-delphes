import math


def deltaPhi(a, b):
    dphi = a.Phi - b.Phi
    if dphi > math.pi:
        dphi -= 2.0*math.pi
    elif dphi <= -math.pi:
        dphi += 2.0*math.pi
    return dphi


def deltaR(a, b):
    return math.sqrt((a.Eta-b.Eta)**2 + deltaPhi(a, b)**2)