#import della libreria che si occupa della realizzazione della porta
from door import *
#import della libreria che si occupa della realizzazione della finestra
from window import *
#import della libreria che si occupa della realizzazione delle scale
from stairs import *
#import della libreria che si occupa della realizzazione del tetto
from roof import *
#import della libreria che fornisce funzioni di supporto per la realizzazione del tetto e della casa
from support import *

def building_element(filename, elementType):
    #creazione dell'elemento
    with open(filename, "rb") as file:#lettura del file
        reader = csv.reader(file, delimiter=",")
        elementsList = []
        #nel caso di porte, finestre, pavimento, scala o serrande
        if elementType=="porte" or elementType=="finestre" or elementType=="pavimento" or elementType=="scale" or elementType=="serrande":
            cuboid = []
            acc = 0
            for row in reader:#leggo ogni riga
                acc = acc + 1
                cuboid.append([float(row[1]),float(row[0])])#memorizzo le coppie di punti due a due
                if(acc == 4):
                    elementsList.append(MKPOL([cuboid,[[1,2,3,4]],None]))#creo una faccia che riempie lo spazio stabilito
                    cuboid = []
                    acc = 0
        if elementType=="perimetro" or elementType=="interni":
            for row in reader:
                elementsList.append(POLYLINE([[float(row[1]), float(row[0])],[float(row[3]), float(row[2])]]))
    elements = STRUCT(elementsList)#creo uno struct degli elementi sopra ricavati
    #tramite PROD produco un elemento tridimensionale
    #le altezze sono proporzionate alla dimensione della casa prima del resize
    if elementType=="perimetro": 
        elements = OFFSET([6,6])(elements)
        elements = PROD([elements, Q(100)])
    elif elementType=="interni":
        elements = OFFSET([3,3])(elements)        
        elements = PROD([elements, Q(99.9)])
    elif elementType=="porte":
        elements = PROD([elements, Q(70)])        
    elif elementType=="serrande":
        elements = PROD([elements, Q(70)])
        dimAndPos = getDimensionAndPosition(elements)
        elements = T([1,2,3])([dimAndPos[1][0]*.03*2,dimAndPos[1][1]*.03*2,dimAndPos[1][2]*.03*2])(elements)
    elif elementType=="finestre":
        elements = OFFSET([3,3])(elements)        
        elements = PROD([elements, Q(50)])
        elements = T(3)(25)(elements)
    elif elementType=="scale":
        elements = PROD([elements, Q(100)])
        dimAndPos = getDimensionAndPosition(elements)
        app = ggpl_building_stairs(6,3,6)
        app = resizeDim(app,dimAndPos[0][0],dimAndPos[0][1],dimAndPos[0][2])
        app = T([1,2,3])([dimAndPos[1][0]*(1/.03),dimAndPos[1][1]*(1/.03),dimAndPos[1][2]*(1/.03)])(app)
        elements = app        
    return elements


def drawPlans(npiano, walls, entries, floors, scale): 
    scale = None
    perimetro = walls[0]
    interni = walls[1]
    porte = entries[0]
    serrande = entries[1]
    finestre = entries[2]
    pavimentoP = floors[0]#pavimento generale
    pavimentoB = floors[1]#pavimento del bagno
    pavimentoG = floors[2]#pavimento del garage
    externalWall = building_element(perimetro, "perimetro")#costruisco il muro esterno
    internalWall = building_element(interni, "interni")#costruisco il muro interno
    doorBox = building_element(porte, "porte")#costruisco i box in cui dovranno essere alloggiate le porte
    if serrande!=None:
        garageBox = building_element(serrande, "porte")#costruisco i box in cui dovranno essere alloggiate le serrande
    windowsBox = building_element(finestre, "finestre")#costruisco i box in cui dovranno essere alloggiate le finestre
    wallsENoDoorEWindow=DIFFERENCE([externalWall,STRUCT([doorBox,windowsBox])])
    if serrande!=None:
        wallsENoDoorEWindow=DIFFERENCE([wallsENoDoorEWindow, garageBox])
    wallsENoDoorEWindow = TEXTURE(['texture/muri.jpg',TRUE,FALSE,1,1,0,150,150])(wallsENoDoorEWindow)
#    wallsINoDoor=DIFFERENCE([internalWall,doorBox])#costruisco il muro interno con i buchi per le porte
#    wallsINoDoor = TEXTURE(['texture/interni.jpg',TRUE,FALSE,1,1,0,15,20])(wallsINoDoor)
#    walls = STRUCT([wallsENoDoorEWindow,wallsINoDoor])#accorpo in un unica variabile i muri della casa
    walls = STRUCT([wallsENoDoorEWindow])#accorpo in un unica variabile i muri della casa
#    floorP = building_element(pavimentoP,"pavimento")#costruisco il pavimento generale
#    floorP = TEXTURE(['texture/parquet.jpg',TRUE,FALSE,1,1,0,15,20])(floorP)
#    floorB = building_element(pavimentoB,"pavimento")#costruisco il pavimento del bagno
#    floorB = TEXTURE(['texture/pavimentoBagno.jpg',TRUE,FALSE,1,1,0,15,20])(floorB)    
#    if pavimentoG!=None:
#        floorG = building_element(pavimentoG,"pavimento")#costruisco il pavimento del garage
#        floorG = TEXTURE(['texture/pavimentoGarage.jpg',TRUE,FALSE,1,1,0,15,20])(floorG)
#        floor = STRUCT([floorP, floorG, floorB])#accorpo in un unica variabile i pavimenti
#    else:
#        floor = STRUCT([floorP, floorB])        
    if scale != None:
        stairs = building_element(scale,"scale")#costruisco le scale
        stairs = TEXTURE(['texture/scale.jpg',TRUE,FALSE,1,1,0,1,1])(stairs)
    if npiano=="terra":
        principDoor = insertElement(porte,"porte",externalWall) 
#    doors = insertElement(porte,"porte",internalWall) 
    windows = insertElement(finestre,"finestre",externalWall)
    if serrande!=None:
        garageDoor = building_element(serrande, "serrande")#costruisco la serranda
        garageDoor = TEXTURE(['texture/serranda.jpg',TRUE,FALSE,1,1,0,1,1])(garageDoor)
    if scale != None and serrande!=None: 
#        plan = STRUCT([walls, floor, stairs, garageDoor])
        plan = STRUCT([walls, stairs, garageDoor])
    elif serrande!=None: 
#        plan = STRUCT([walls, floor, garageDoor])
        plan = STRUCT([walls, garageDoor])
    else: 
#        plan = STRUCT([walls, floor])        
        plan = STRUCT([walls])        
    plan = S([1,2,3])([.03,.03,.03])(plan)
    if npiano=="terra":
#        plan = STRUCT([plan,doors,principDoor,windows])
        plan = STRUCT([plan,principDoor,windows])
    else:
#        plan = STRUCT([plan,doors,windows])
        plan = STRUCT([plan,windows])
    return plan

def positionElement(filename, elementType, wall):
    with open(filename, "rb") as file:
        reader = csv.reader(file, delimiter=",")
        elementsList = []
        if elementType=="porte" or elementType=="finestre":
            cuboid = []
            acc = 0
            for row in reader:
                acc = acc + 1
                cuboid.append([float(row[1]),float(row[0])])
                if(acc == 4):
                    cub = STRUCT([MKPOL([cuboid,[[1,2,3,4]],None])])
                    if elementType=="porte":
                        cub = PROD([cub,Q(70)])
                    elif elementType=="finestre":
                        cub = PROD([cub, Q(SIZE([3])(wall)[0]/2.)])
                        cub = T(3)(SIZE([3])(wall)[0]/4.)(cub)
                    elementsList.append(cub)
                    cuboid = []
                    acc = 0
    return elementsList

def insertElement(fileName, elementType, wall):#fileName, elementType, wall    
    dimAndPosElements = []
    if elementType=="porte" or elementType=="finestre":
        for elem in positionElement(fileName,elementType, wall):
            wall2 = DIFFERENCE([wall, elem])#spazio che rappresenta il box disegnato con inkscape per l'elemento
            element = DIFFERENCE([wall, wall2])#spazio che rappresenta il box in cui alloggiare l'elemento
            sizeElement = SIZE([1,2])(element)
            if sizeElement[0]!=0.0 and sizeElement[1]!=0.0:
                dimAndPosElements.append(getDimensionAndPosition(element))
        elements =[]
        for d in dimAndPosElements:#per ogni box da riempire
            if d[0][0]>d[0][1]:#se l'oggetto si sviluppa sull'asse x
                if elementType=="porte":
                    element = createDoor([XD,YD,ZD],occupancyD)(1.2,.05,2.1)
                    element = rotation(element,2)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
                elif elementType=="finestre":
                    element = createWindow([XW,YW,ZW],occupancyW)(3.6,.05,2.29)
                    element = rotation(element,2)
                    element = resizeDim(element,d[0][0]*.0315,d[0][1]*.03,d[0][2]*.03)
            else:#se l'oggetto si sviluppa sull'asse y, come sopra ma orientato sull'asse y
                if elementType=="porte":                                
                    element = createDoor([XD,YD,ZD],occupancyD)(1.2,.05,2.1)
                    element = rotation(element,1)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.03,d[0][2]*.03)
                elif elementType=="finestre":
                    element = createWindow([XW,YW,ZW],occupancyW)(3.6,.05,2.29)
                    element = rotation(element,1)
                    element = resizeDim(element,d[0][0]*.03,d[0][1]*.031,d[0][2]*.03)
            element = STRUCT([T([1,2,3])(d[1]),element])
            #aggiusto la posizione delle porte e delle finestre se occorre, alcuni elementi potrebbero essere
            #posizionati troppo all'interno o all'esterno della casa e non con precisione a filo del muro a causa
            #di errori da parte dell'utilizzatore di inkscape
            if elementType=="porte":
                if d[0][0]>d[0][1]:
                    element = STRUCT([T(2)(-YD[0]),element])
                else:
                    element = STRUCT([T(1)(-YD[0]),element])
            elif elementType=="finestre":
                if d[0][0]>d[0][1]:
                    element = STRUCT([T(2)(-6*YW[0]),element])
                else:
                    element = STRUCT([T(1)(-4*YW[0]),element])
            elements.append(element)
        return STRUCT(elements)

#dati gli elementi di ogni piano in un array, la funzione costruisce la casa ed il relativo tetto
def multistoreyHouse():
    #parametri per la costruzione del piano terra
    entriesT = ["pianoTerra/porte.lines","pianoTerra/serrande.lines","pianoTerra/finestre.lines"]
    floorsT = ["pianoTerra/pavimentoP.lines","pianoTerra/pavimentoB.lines","pianoTerra/pavimentoG.lines"]
    wallsT = ["pianoTerra/perimetro.lines","pianoTerra/interni.lines"]
    elementsOfPlanT = [entriesT, floorsT, wallsT]
    #parametri per la costruzione del piano terra
    entriesP = ["primoPiano/porte.lines",None,"primoPiano/finestre.lines"]
    floorsP = ["primoPiano/pavimentoP.lines","primoPiano/pavimentoB.lines",None]
    wallsP = ["primoPiano/perimetro.lines","primoPiano/interni.lines"]
    elementsOfPlanP = [entriesP, floorsP, wallsP]
    entriesT = elementsOfPlanT[0]#porte, finestre e serranda del piano terra
    floorsT = elementsOfPlanT[1]#pavimenti del piano terra
    wallsT = elementsOfPlanT[2]#muri del piano terra
    entriesP = elementsOfPlanP[0]#porte, finestre e serranda del primo piano
    floorsP = elementsOfPlanP[1]#pavimenti del primo piano
    wallsP = elementsOfPlanP[2]#muri del primo piano
    plan1 = drawPlans("terra",wallsT,entriesT,floorsT,"pianoTerra/scale.lines")#costruzione del piano terra 
#    plan2 = T(3)(3)(drawPlans("primo",wallsP,entriesP,floorsP, None))#costruzione del primo piano
#    house = STRUCT([plan1,plan2])#costruzione della casa
    roofMeasure = getDimensionAndPosition(plan1)#calcolo delle misure e della posizione del tetto
    #creo il tetto richiamando la funzione generata nell'homework_09 e presente nel package roof.py
    roof = T([1,2])([roofMeasure[1][0]/.03,roofMeasure[1][1]/.03])(myRoofTerrace(plan1,PI/5,3))
    house = STRUCT([plan1,T(3)(3)(roof)])
    return house


