from conf4_v1 import f

def factor(pt, eta):
    func = f(eta)
    if not func:
        return 1.0
    xMax = func.GetXmax()
    xMin = func.GetXmin()
    x = pt
    if xMax < x:
        x = xMax
    if x < xMin:
        x = xMin
    v = func.Eval(x)
    return 1.0 if not v else 1.0/v
