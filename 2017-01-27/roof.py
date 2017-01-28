from pyplasm import *
from support import * 
import math
import csv


#crea e restituisce un tetto dati come parametri la casa, l'angolo che si vuole del tetto e la lunghezza della falda
def myRoofTerrace(house,angle,length):
    dimAndPos=getDimensionAndPosition(house)
    vertexs=[]#calcolo dei vertici inferiori che costituiscono il tetto
    vertexs.append([dimAndPos[1][0]*.03,dimAndPos[1][1]*.02])
    vertexs.append([dimAndPos[1][0]*.03,+dimAndPos[0][1]-dimAndPos[1][1]*.4])
    vertexs.append([dimAndPos[0][0]+dimAndPos[1][0]/4,dimAndPos[0][1]-dimAndPos[1][1]*.4])
    vertexs.append([dimAndPos[0][0]+dimAndPos[1][0]/4,dimAndPos[1][1]*.02])
    roof=createRoof(vertexs,angle,length)
    return roof


def createRoof(vertexes,angle,length):
    directions = getDirections(vertexes)#calcolo delle direzioni delle rette che uniscono i vertici del tetto
    listOfPlan = getListOfPlan(vertexes, directions, angle, length)#calcolo della lista dei piani che compongono il tetto
    lines = getLines(listOfPlan)#calcolo delle linee che uniscono due vertici consecutivi del tetto
    intersections = getIntersections(lines)#calcolo delle intersezioni delle linee sopra-calcolate
    drawListOfPlan = createListOfPlan(directions, intersections, listOfPlan)#costuzione dei vari piani che compongono il tetto 
    vertexsOfTerrace = getVertexsOfTerrace(intersections)#calcolo dei vertici superiori che compongono il tetto
    subroof = POLYLINE(vertexes)#costruzione del sottotetto
    subroof = SOLIDIFY(subroof)
    subroof = COLOR([1,1,1,1])(subroof)
    terrace = POLYLINE(vertexsOfTerrace)#costruzione del terrazzo
    terrace = SOLIDIFY(terrace)
    terrace = T(3)(listOfPlan[0][2][2])(terrace)
    terrace = TEXTURE(["texture/tegole.jpg", TRUE, FALSE, 1, 1, 0, 15, 15])(terrace)
    roof = STRUCT(drawListOfPlan)
    roof=TEXTURE(["texture/tegole.jpg", TRUE, FALSE, 1, 1, 0, 15, 15])(roof)
    return STRUCT([terrace,roof,subroof])
