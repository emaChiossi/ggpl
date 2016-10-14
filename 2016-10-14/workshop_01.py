from pyplasm import *
from larlib import *

def create(beamSection, pillarSection,distanceBetweenPillar, interstoryHeight):
	bx = beamSection[0]
	bz = beamSection[1]
	px = pillarSection[0]
	py = pillarSection[1]
	pz = interstoryHeight[0]
	Xpil = []
	Ypil = []
	Zpil = []
	Xbea = []
	Ybea = [py]
	Zbea = []
	lunghezza = 0
	#costruzione pilastro
	for i in distanceBetweenPillar:
		Xpil = Xpil+[px,-i]
		Ypil = [py]
		lunghezza=lunghezza+i+px
	for i in interstoryHeight:
		Zpil = Zpil+[i,-bz]
		Zbea = Zbea+[-i,bz]
	Xbea = [lunghezza+px] 
	Xpil = Xpil+[px]	
	aPil = PROD([QUOTE(Ypil),QUOTE(Zpil)])
	piloni = PROD([QUOTE(Xpil),aPil])
	#costruzione trave
	aTrav = PROD([QUOTE(Ybea),QUOTE(Zbea)])
	travi=PROD([QUOTE(Xbea),aTrav])

	VIEW(STRUCT([piloni,travi]))

create((.4,.4),(.4,.4),[4,4,4],[3,3,3])