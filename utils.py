import math

def size(eventVars={}, key=""):
    """works, e.g., for
    (a) TClonesArray with size stored in separate branch;
    (b) list"""

    pKey = key+"_size"
    if pKey in eventVars:
        return eventVars[pKey]
    else:
        return len(eventVars[key])


def eta(obj):
    return "%4.1f" % obj.Eta if abs(obj.Eta)<10.0 else "    "


def deltaPhi(a, b):
    dphi = a.Phi - b.Phi
    if dphi > math.pi:
        dphi -= 2.0*math.pi
    elif dphi <= -math.pi:
        dphi += 2.0*math.pi
    return dphi


def deltaR(a, b):
    return math.sqrt((a.Eta-b.Eta)**2 + deltaPhi(a, b)**2)

#lv1 = supy.utils.LorentzV()
#lv2 = supy.utils.LorentzV()
#
#def deltaR(a, b):
#    lv1.SetCoordinates(a.PT, a.Eta, a.Phi, a.Mass)
#    lv2.SetCoordinates(b.PT, b.Eta, b.Phi, b.Mass)
#    return r.Math.VectorUtil.DeltaR(lv1, lv2)
