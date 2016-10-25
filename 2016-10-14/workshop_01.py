from pyplasm import *
from larlib import *

def create(beamSection, pillarSection,distanceBetweenPillar, interstoryHeight):
	bx = beamSection[0]
	bz = beamSection[1]
	px = pillarSection[0]
	py = pillarSection[1]
	Xpil = []	
	Xbea = [bx]
	if bx>px:
		Xpil = [-(DIV([bx,2])-DIV([px,2]))]
	if bx<px:
		Xbea = [-(DIV([px,2])-DIV([bx,2])),bx]	
	Ypil = []
	Zpil = []
	Ybea = []
	Zbea = []
	lunghezza = 0
	for i in distanceBetweenPillar:
		Ypil = Ypil+[py,-i]
		lunghezza=lunghezza+i+py
	Xpil = Xpil+[px]
	for i in interstoryHeight:
		Zpil = Zpil+[i,-bz]
		Zbea = Zbea+[-i,bz]
	Ybea = [lunghezza+py] 
	Ypil = Ypil+[py]	
	#costruzione pilastro
	aPil = PROD([QUOTE(Ypil),QUOTE(Zpil)])
	piloni = PROD([QUOTE(Xpil),aPil])
	#costruzione trave
	aTrav = PROD([QUOTE(Ybea),QUOTE(Zbea)])
	travi=PROD([QUOTE(Xbea),aTrav])
	VIEW(STRUCT([piloni,travi]))

create((.4,.4),(.8,.8),[4,4,4],[3,3,3])