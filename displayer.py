import ROOT as r
import supy

try:
    import pdgLookup
    pdgLookupExists = True
except ImportError:
    pdgLookupExists = False

class displayer(supy.steps.displayer):
    def __init__(self, scale=200.0, nMaxJets=7,
                 jets=[("Jet", r.kBlue, 1),
                       ("GenJet", r.kBlack, 1),
                       ],
                 ):
        self.moreName = "(see below)"

        for item in ["scale", "jets", "nMaxJets"]:
            setattr(self, item, eval(item))

        self.titleSizeFactor = 1.0
        
        self.legendDict = {}
        self.legendList = []

        self.ellipse = r.TEllipse()
        self.ellipse.SetFillStyle(0)

        self.line = r.TLine()
        self.arrow = r.TArrow()
        self.text = r.TText()
        self.latex = r.TLatex()

    def prepareText(self, params, coords) :
        self.text.SetTextSize(params["size"])
        self.text.SetTextFont(params["font"])
        self.text.SetTextColor(params["color"])
        self.textSlope = params["slope"]

        self.textX = coords["x"]
        self.textY = coords["y"]
        self.textCounter = 0

    def printText(self, message, color=r.kBlack):
        self.text.SetTextColor(color)
        self.text.DrawText(self.textX, self.textY - self.textCounter * self.textSlope, message)
        self.textCounter += 1
        self.text.SetTextColor(r.kBlack)

    def printEvent(self, eventVars, params, coords):
        if "Event" not in eventVars:
            return
        event = eventVars["Event"][0]
        self.prepareText(params, coords)
        self.printText("Event %10d / Weight %g" % (event.Number, event.Weight))

    def printVertices(self, eventVars, params, coords, nMax):
        if "vertexIndices" not in eventVars:
            return
        self.prepareText(params, coords)
        self.printText("Vertices")
        self.printText("ID   Z(cm)%s"%(" sumPt(GeV)" if not self.prettyMode else ""))
        self.printText("----------%s"%("-----------" if not self.prettyMode else ""))

        nVertices = eventVars["vertexNdof"].size()
        for i in range(nVertices) :
            if nMax<=i :
                self.printText("[%d more not listed]"%(nVertices-nMax))
                break
            
            out = "%2s  %6.2f"%("G " if i in eventVars["vertexIndices"] else "  ", eventVars["vertexPosition"].at(i).z())
            if not self.prettyMode : out += " %5.0f"%eventVars["vertexSumPt"].at(i)
            self.printText(out)

    def printPhotons(self, eventVars, params, coords, photons, nMax) :
        self.prepareText(params, coords)
        p4Vector = eventVars["%sP4%s"        %photons]
        loose    = eventVars["%sIDLooseFromTwiki%s"%photons]
        tight    = eventVars["%sIDTightFromTwiki%s"%photons]
            
        self.printText(self.renamedDesc(photons[0]+photons[1]))
        self.printText("ID   pT  eta  phi")
        self.printText("-----------------")

        nPhotons = p4Vector.size()
        for iPhoton in range(nPhotons) :
            if nMax<=iPhoton :
                self.printText("[%d more not listed]"%(nPhotons-nMax))
                break
            photon=p4Vector[iPhoton]

            outString = "%1s%1s"% ("L" if loose[iPhoton] else " ", "T" if tight[iPhoton] else " ")
            outString+="%5.0f %4.1f %4.1f"%(photon.pt(), photon.eta(), photon.phi())
            self.printText(outString)

    def printElectrons(self, eventVars, params, coords, electrons, nMax) :
        self.prepareText(params, coords)
        p4Vector = eventVars["%sP4%s"        %electrons]
        cIso = eventVars["%sIsoCombined%s"%electrons]
        ninetyFive = eventVars["%sID95%s"%electrons]
     
        self.printText(self.renamedDesc(electrons[0]+electrons[1]))
        self.printText("ID   pT  eta  phi")#  cIso")
        self.printText("-----------------")#------")

        nElectrons = p4Vector.size()
        for iElectron in range(nElectrons) :
            if nMax<=iElectron :
                self.printText("[%d more not listed]"%(nElectrons-nMax))
                break
            electron=p4Vector[iElectron]

            outString = "%2s"%("95" if ninetyFive[iElectron] else "  ")
            outString+="%5.0f %4.1f %4.1f"%(electron.pt(), electron.eta(), electron.phi())
            #outString+=" %5.2f"%cIso[iElectron] if cIso[iElectron]!=None else " %5s"%"-"
            self.printText(outString)

    def printMuons(self, eventVars, params, coords, muons, nMax) :
        self.prepareText(params, coords)
        p4Vector = eventVars["%sP4%s"     %muons]
        tight    = eventVars["%sIdPog2012Tight%s"%muons]
        iso      = eventVars["%sPfIsolationR04DeltaBCorrected%s"%muons]
        gl       = eventVars["%sIsGlobalMuon%s"%muons]
        pf       = eventVars["%sIsPFMuon%s"%muons]
        
        self.printText(self.renamedDesc(muons[0]+muons[1]))
        self.printText(" ID  pT  eta  phi pfIso")
        self.printText("-----------------------")

        nMuons = p4Vector.size()
        for iMuon in range(nMuons) :
            if nMax<=iMuon :
                self.printText("[%d more not listed]"%(nMuons-nMax))
                break
            muon=p4Vector[iMuon]

            outString = "%s%s%s"%("G" if gl[iMuon] else " ", "P" if pf[iMuon] else " ", "T" if tight[iMuon] else " ")
            outString+= "%4.0f %4.1f %4.1f"%(muon.pt(), muon.eta(), muon.phi())
            outString+= " %5.2f"%(iso[iMuon]) if iso[iMuon]<100.0 else ">100".rjust(6)

            self.printText(outString)

    def printJets(self, eventVars=None, params=None, coords=None, jets=None, nMax=None, highlight=False):
        self.prepareText(params, coords)
        self.printText(jets)
        headers = "bbt    pT  eta  phi  Mass"
        self.printText(headers)
        self.printText("-" * len(headers))

        for iJet, jet in enumerate(eventVars[jets]):
            if nMax <= iJet:
                self.printText("[%d more not listed]" % (len(eventVars[jets]) - nMax))
                break

            outString = "%1s%1s%1s" % (jet.BTag % 0x1, jet.BTag % 0x2, jet.TauTag)
            outString += " %5.0f %4.1f %4.1f %5.0f" % (jet.PT, jet.Eta, jet.Phi, jet.Mass)

            color = r.kBlack
            if highlight:
                for jetsHighlight, indicesHighlight, colorHighlight, _, _ in self.jetIndices:
                    if jetsHighlight != jets:
                        continue
                    if (indicesHighlight in eventVars) and (iJet in eventVars[indicesHighlight]):
                        color = colorHighlight

            self.printText(outString, color)

    def printGenJets(self, eventVars, params, coords, nMax):
        p4Key = "%sP4%s" % self.genJets
        if p4Key not in eventVars:
            return
        p4Vector = eventVars[p4Key]
            
        self.prepareText(params, coords)
        self.printText(self.renamedDesc(p4Key))
        self.printText("   pT  eta  phi")
        self.printText("---------------")

        nJets = p4Vector.size()
        for iJet in range(nJets):
            if nMax <= iJet:
                self.printText("[%d more not listed]"%(nJets-nMax))
                break
            jet = p4Vector.at(iJet)
            self.printText("%5.0f %4.1f %4.1f"%(jet.pt(), jet.eta(), jet.phi()))

    def printGenParticles(self, eventVars=None, params=None, coords=None,
                          nMax=None, indices=None, color=r.kBlack):
        self.prepareText(params, coords)
        p4s = eventVars["genP4"]
        ids = eventVars["genPdgId"]
        
        self.printText(indices.replace("Indices", ""))
        self.printText("  name  pdgId   pT  eta  phi")
        self.printText("----------------------------")

        nParticles = len(eventVars[indices])
        iPrint = 0
        for iParticle in eventVars[indices]:
            if nMax <= iPrint:
                self.printText("[%d more not listed]"%(nParticles-nMax))
                break
            pdgId = ids.at(iParticle)
            p4 = p4s.at(iParticle)
            name = pdgLookup.pdgid_to_name(pdgId) if pdgLookupExists else ""
            self.printText("%6s %6d%5.0f %4.1f %4.1f" % (name[-6:], pdgId, p4.pt(), p4.eta(), p4.phi()),
                           color=color)
            iPrint += 1
        return


    def printKinematicVariables(self, eventVars, params, coords, jets, jets2) :
        self.prepareText(params, coords)
        
        def go(j) :
            dps = eventVars[self.deltaPhiStarName]
            l = [eventVars["%sHtBin%s"%j],
                 eventVars["%s%s%s"  %(j[0], "SumEt",        j[1])],
                 eventVars["%s%s%s"  %(j[0], "SumP4",        j[1])].pt() if eventVars["%s%s%s"%(j[0], "SumP4",  j[1])] else 0,
                 eventVars["%s%s%s"  %(j[0], "AlphaTEt",     j[1])],
                 dps[0][0] if dps else -1.0,
                 ]
            for i in range(len(l)) :
                if l[i]==None : l[i] = -1.0
            self.printText("%14s %4.0f %4.0f %4.0f %6.3f %5.2f"%tuple([self.renamedDesc(j[0]+j[1])]+l))

        self.printText("jet collection  bin   HT  MHT alphaT Dphi*")
        self.printText("------------------------------------------")
        
        go(jets)
        if jets2!=None :
            go(jets2)
        
    def drawSkeleton(self, coords, color) :
        r.gPad.AbsCoordinates(False)
        
        self.ellipse.SetLineColor(color)
        self.ellipse.SetLineWidth(1)
        self.ellipse.SetLineStyle(1)
        self.ellipse.DrawEllipse(coords["x0"], coords["y0"], coords["radius"], coords["radius"], 0.0, 360.0, 0.0, "")

        self.line.SetLineColor(color)
        self.line.DrawLine(coords["x0"]-coords["radius"], coords["y0"]                 , coords["x0"]+coords["radius"], coords["y0"]                 )
        self.line.DrawLine(coords["x0"]                 , coords["y0"]-coords["radius"], coords["x0"]                 , coords["y0"]+coords["radius"])

    def drawScale(self, color, size, scale, point) :
        self.latex.SetTextSize(size)
        self.latex.SetTextColor(color)
        self.latex.DrawLatex(point["x"], point["y"],"radius = "+str(scale)+" GeV p_{T}")

    def drawP4(self,
               rhoPhiPad=None,
               etaPhiPad=None,
               coords=None,
               p4=None,
               lineColor=None,
               lineWidth=1,
               lineStyle=1,
               arrowSize=1.0,
               circleRadius=1.0):

        c = coords
        x0 = c["x0"]
        y0 = c["y0"]
        x1 = x0 + p4.px()*c["radius"]/c["scale"]
        y1 = y0 + p4.py()*c["radius"]/c["scale"]

        rhoPhiPad.cd()
        self.arrow.SetLineColor(lineColor)
        self.arrow.SetLineWidth(lineWidth)
        self.arrow.SetLineStyle(lineStyle)
        self.arrow.SetArrowSize(arrowSize)
        self.arrow.SetFillColor(lineColor)
        self.arrow.DrawArrow(x0, y0, x1, y1)

        etaPhiPad.cd()
        self.ellipse.SetLineColor(lineColor)
        self.ellipse.SetLineWidth(lineWidth)
        self.ellipse.SetLineStyle(lineStyle)
        self.ellipse.DrawEllipse(p4.eta(), p4.phi(), circleRadius, circleRadius, 0.0, 360.0, 0.0, "")


    def legendFunc(self, lineColor=None, lineStyle=1, name="", desc=""):
        if name not in self.legendDict:
            self.legendDict[name] = True
            self.legendList.append((lineColor, lineStyle, desc, "l"))

    def drawGenParticles(self, eventVars=None, indices="",
                         coords=None, lineColor=None,
                         lineWidth=1, lineStyle=1,
                         arrowSize=-1.0, circleRadius=None):

        self.legendFunc(lineColor=lineColor,
                        lineStyle=lineStyle,
                        name=indices,
                        desc=indices)

        for iParticle in eventVars[indices]:
            particle = eventVars["genP4"].at(iParticle)
            if circleRadius is None:
                self.drawP4(coords=coords,
                            p4=particle,
                            lineColor=lineColor,
                            lineWidth=lineWidth,
                            arrowSize=arrowSize)
            else :
                self.drawCircle(p4=particle,
                                lineColor=lineColor,
                                lineWidth=lineWidth,
                                circleRadius=circleRadius)


    def drawJets(self, eventVars=None, jets=None,
                 coords=None, lineColor=None, lineWidth=1, lineStyle=1,
                 arrowSize=-1.0, circleRadius=None, rhoPhiPad=None, etaPhiPad=None):

        self.legendFunc(lineColor=lineColor,
                        lineStyle=lineStyle,
                        name=jets, desc=jets)

        for jet in eventVars[jets]:
            self.drawP4(rhoPhiPad=rhoPhiPad,
                        etaPhiPad=etaPhiPad,
                        coords=coords,
                        p4=supy.utils.LorentzV(jet.PT, jet.Eta, jet.Phi, jet.Mass),
                        lineColor=lineColor,
                        lineWidth=lineWidth,
                        lineStyle=lineStyle,
                        arrowSize=arrowSize,
                        circleRadius=circleRadius)


    def drawMht(self, eventVars, coords, color, lineWidth, arrowSize) :
        self.legendFunc(lineColor=color, name="%smht%s"%self.jets, desc="MHT (%s%s)"%self.jets)

        sump4 = eventVars["%sSumP4%s"%self.jets]
        if self.tipToTail :
            phiOrder = eventVars["%sIndicesPhi%s"%self.jets]
            partials = eventVars["%sPartialSumP4%s"%self.jets]
            mean = eventVars["%sPartialSumP4Centroid%s"%self.jets]
            if sump4 : self.drawP4(coords, -sump4,color,lineWidth,
                                   arrowSize=arrowSize, p4Initial=partials[-1]-mean)
            return
        if sump4 : self.drawP4(coords, -sump4, color, lineWidth, arrowSize=arrowSize)
            
    def drawGenMet(self, eventVars, coords, color, lineWidth, arrowSize) :
        if self.genMet==None : return
        self.legendFunc(lineColor=color,
                        name="genMet",
                        desc="GEN MET (%s)" % self.genMet)
        self.drawP4(coords, eventVars[self.genMet], color, lineWidth, arrowSize=arrowSize)
            
    def etaPhiPad(self, eventVars, corners):
        pad = r.TPad("etaPhiPad", "etaPhiPad",
                     corners["x1"], corners["y1"],
                     corners["x2"], corners["y2"])
        pad.cd()
        pad.SetTickx()
        pad.SetTicky()

        etaPhiPlot = r.TH2D("etaPhi", ";#eta;#phi;",
                            1, -r.TMath.Pi(), r.TMath.Pi(),
                            1, -r.TMath.Pi(), r.TMath.Pi())
        etaPhiPlot.SetStats(False)
        etaPhiPlot.Draw()
        return pad, etaPhiPlot


    def rhoPhiPad(self, eventVars, coords, corners):
        pad = r.TPad("rhoPhiPad", "rhoPhiPad", corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        pad.cd()

        skeletonColor = r.kYellow+1
        self.drawSkeleton(coords, skeletonColor)
        self.drawScale(color=skeletonColor, size=0.03, scale=coords["scale"],
                       point={"x":0.0, "y":coords["radius"]+coords["y0"]+0.03})
        return pad

    def drawObjects(self, eventVars=None, etaPhiPad=None, rhoPhiPad=None, rhoPhiCoords=None):
        defArrowSize=0.5*self.arrow.GetDefaultArrowSize()
        defWidth=1

        #if self.genMet and not eventVars["isRealData"]:
        #    rhoPhiPad.cd()
        #    self.drawGenMet(eventVars, rhoPhiCoords, r.kMagenta, defWidth, defArrowSize*2/6.0)

        arrowSize = defArrowSize
        #if not eventVars["isRealData"]:
        #    for indices, color, nMaxPrint in self.genParticleIndices:
        #        rhoPhiPad.cd()
        #        self.drawGenParticles(eventVars=eventVars,
        #                              indices=indices,
        #                              coords=rhoPhiCoords,
        #                              lineColor=color,
        #                              arrowSize=arrowSize)
        #        arrowSize *= 0.8
        #
        #        etaPhiPad.cd()
        #        self.drawGenParticles(eventVars=eventVars,
        #                              indices=indices,
        #                              lineColor=color,
        #                              circleRadius=0.15)
        #
        for jets, color, style in self.jets:
            self.drawJets(eventVars=eventVars,
                          jets=jets,
                          coords=rhoPhiCoords,
                          lineColor=color,
                          lineStyle=style,
                          arrowSize=arrowSize,
                          circleRadius=0.5,
                          rhoPhiPad=rhoPhiPad,
                          etaPhiPad=etaPhiPad,
                          )
            arrowSize *= 0.8

        #rhoPhiPad.cd()
        #coords = rhoPhiCoords
        #
        #items = [("met", r.kGreen),
        #         ("muons", r.kYellow),
        #         ("electrons", r.kOrange+7),
        #         ("photons", r.kOrange),
        #         ] + ([] if self.prettyMode else [("taus", r.kYellow)])
        #
        #for item, color in items:
        #    fixes = getattr(self, item)
        #    if type(fixes) is str:
        #        self.legendFunc(lineColor=color, name=fixes, desc=fixes)
        #        self.drawP4(coords, eventVars[fixes], color, defWidth, arrowSize=defArrowSize*2/6.0)
        #    elif type(fixes) is tuple and len(fixes) == 2:
        #        p4Name = "%sP4%s" % fixes
        #        self.legendFunc(lineColor=color, name=p4Name, desc=p4Name)
        #        p4Vector = eventVars[p4Name]
        #        for i in range(len(p4Vector)):
        #            self.drawP4(coords, p4Vector.at(i), color, defWidth, arrowSize=defArrowSize*2/6.0)

    def drawLegend(self, corners) :
        pad = r.TPad("legendPad", "legendPad", corners["x1"], corners["y1"], corners["x2"], corners["y2"])
        pad.cd()
        
        legend = r.TLegend(0.0, 0.0, 1.0, 1.0)
        for color, style, desc, gopts in self.legendList:
            self.line.SetLineColor(color)
            self.line.SetLineStyle(style)
            someLine = self.line.DrawLine(0.0, 0.0, 0.0, 0.0)
            legend.AddEntry(someLine, desc, gopts)
        legend.Draw("same")
        self.canvas.cd()
        pad.Draw()
        return [pad,legend]

    def printAllText(self, eventVars, corners):
        pad = r.TPad("textPad", "textPad",
                     corners["x1"], corners["y1"],
                     corners["x2"], corners["y2"])
        pad.cd()

        defaults = {}
        defaults["size"] = 0.035
        defaults["font"] = 80
        defaults["color"] = r.kBlack
        defaults["slope"] = 0.017
        s = defaults["slope"]

        smaller = {}
        smaller.update(defaults)
        smaller["size"] = 0.034
        
        yy = 0.98
        x0 = 0.01
        x1 = 0.51
        self.printEvent(eventVars, params=defaults, coords={"x": x0, "y": yy})

        for iCollection, jetSpec in enumerate(self.jets):
            self.printJets(eventVars,
                           params=smaller,
                           coords={"x": x0, "y": yy-2*s-iCollection*s*(6 + self.nMaxJets)},
                           jets=jetSpec[0],
                           nMax=self.nMaxJets,
                           highlight=False)

        #nYR = 6 + self.nMaxJets
        #nYL = nYR + 4 + nMaxGenJets
        #for iCollection, particles in enumerate(self.particles):
        #    left = iCollection % 2
        #    if left:
        #        dx = -0.01
        #        nY = nYL
        #    else:
        #        dx = 0.49
        #        nY = nYR
        #    self.printGenParticles(eventVars,
        #                           params=smaller,
        #                           indices=indices,
        #                           color=color,
        #                           coords={"x": x0+dx,
        #                                   "y": yy-nY*s},
        #                           nMax=nMax)
        #    if left:
        #        nYL += 4+nMax
        #    else:
        #        nYR += 4+nMax

        #    if self.jetsOtherAlgo:
        #        self.printJets(eventVars,
        #                       params=smaller,
        #                       coords={"x": x0,
        #                               "y": yy-(6+self.nMaxJets)*s},
        #                       jets=self.jetsOtherAlgo,
        #                       nMax=self.nMaxJets)
        #
        #    if self.muons:
        #        self.printMuons(eventVars,
        #                        params=defaults,
        #                        coords={"x": x0,
        #                                "y": yy-35*s},
        #                        muons=self.muons,
        #                        nMax=3)
        #    self.printVertices(eventVars,
        #                       params=defaults,
        #                       coords={"x": x1,
        #                               "y": yy-35*s},
        #                       nMax=3)
        #
        #    if self.photons:
        #        self.printPhotons(eventVars,
        #                          params=defaults,
        #                          coords={"x": x0,
        #                                  "y": yy-42*s},
        #                          photons=self.photons,
        #                          nMax=3)
        #    if self.electrons:
        #        self.printElectrons(eventVars,
        #                            params=defaults,
        #                            coords={"x": x1,
        #                                    "y": yy-42*s},
        #                            electrons=self.electrons,
        #                            nMax=3)

        self.canvas.cd()
        pad.Draw()
        return [pad]


    def display(self, eventVars):
        rhoPhiPadYSize = 0.50*self.canvas.GetAspectRatio()
        rhoPhiPadXSize = 0.50
        radius = 0.4

        rhoPhiCoords = {"scale":self.scale, "radius":radius,
                        "x0":radius, "y0":radius+0.05}

        rhoPhiCorners = {"x1":0.0,
                         "y1":0.0,
                         "x2":rhoPhiPadXSize,
                         "y2":rhoPhiPadYSize}

        etaPhiCorners = {"x1":rhoPhiPadXSize - 0.18,
                         "y1":rhoPhiPadYSize - 0.08*self.canvas.GetAspectRatio(),
                         "x2":rhoPhiPadXSize + 0.12,
                         "y2":rhoPhiPadYSize + 0.22*self.canvas.GetAspectRatio()}

        legendCorners = {"x1":0.0,
                         "y1":rhoPhiPadYSize,
                         "x2":1.0-rhoPhiPadYSize,
                         "y2":1.0}

        textCorners =  {"x1":rhoPhiPadXSize + 0.11,
                        "y1":0.0,
                        "x2":1.0,
                        "y2":1.0}

        rhoPhiPad = self.rhoPhiPad(eventVars, rhoPhiCoords, rhoPhiCorners)
        etaPhiPad, etaPhiPlot = self.etaPhiPad(eventVars, etaPhiCorners)

        keep = [rhoPhiPad, etaPhiPad, etaPhiPlot]
        self.drawObjects(eventVars, etaPhiPad, rhoPhiPad, rhoPhiCoords)

        self.canvas.cd()
        rhoPhiPad.Draw()
        etaPhiPad.Draw()

        keep.append(self.drawLegend(corners=legendCorners))
        keep.append(self.printAllText(eventVars, corners=textCorners))
        return keep
