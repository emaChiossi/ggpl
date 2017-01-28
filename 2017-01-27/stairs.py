from pyplasm import *
from larlib import *
"""Funzione che realizza il disegno di una scalinata prendendo
   in input i valori dx,dy e dz dello spazio a disposizione"""
def ggpl_building_stairs(dx,dy,dz):
    #Variabili principali
    platformX = 1   #dimensione X del pianerottolo
    platformY = dy   #dimensione Y del pianerottolo,
    idealTread = .29   #dimensione ideale pedata
    idealRiser = .17   #dimensione ideale alzata
    treadWidth = DIV([dy,2])   #dimensione Y della singola rampa di scale
    halfDz = DIV([dz,2])   #dimensione Z della singola rampa di scale
    treadTot = dx - platformX   #dimensione X della rampa di scale senza il pianerottolo
    steps = modf(treadTot/idealTread)[1]   #numero gradini
    tread = DIV([treadTot,steps])  #pedata reale
    riser = DIV([halfDz,steps+.5])  #alzata reale

    stairs = []   #scale
    diagonal = []  #sostegno scale
    vertex = [[tread,0,0],[tread,0,riser],[2*tread,0,riser],[tread,treadWidth,0],[tread,treadWidth,riser],[2*tread,treadWidth,riser]]
    cells = [1,2,3,4,5,6]
    diagonal.append(MKPOL([vertex,[cells],None]))
    #Ciclo che costruisce la prima rampa di scale con il rispettivo sostegno
    for x in range(0,int(steps)):
        stairs.append(CUBOID([tread,treadWidth,riser]))
        stairs.append(T([1,2,3])([tread,0,riser]))
        diagonal.append(MKPOL([vertex,[cells],None]))
        diagonal.append(T([1,2,3])([tread,0,riser]))
    stairs.append(CUBOID([platformX,platformY,riser])) #si inserisce il pianerottolo
    stairs.append(R([1,2])(PI)) 
    stairs.append(T([1,2,3])([0,-2*treadWidth,riser])) #traslazione per spostare la seconda scala al posto giusto
    diagonal.append(R([1,2])(PI)) 
    diagonal.append(T([1,2,3])([0,-2*treadWidth,riser]))#traslazione per spostare il secondo sostegno al posto giusto
    #Ciclo che costruisce la seconda , altro codice come nel primo ciclo
    for x in range(0,int(steps)):
        stairs.append(CUBOID([tread,treadWidth,riser]))
        stairs.append(T([1,2,3])([tread,0,riser]))
        if(x<(steps-1)):
            diagonal.append(MKPOL([vertex,[cells],None]))
            diagonal.append(T([1,2,3])([tread,0,riser]))
    stairs.append(R([1,2])(PI))
  
    return STRUCT([STRUCT(diagonal),STRUCT(stairs)])
