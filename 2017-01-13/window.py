from pyplasm import *
#parametri di costruzione della finestra
XW =[.05,.4,.02,.4,.1,.4,.02,.4,.05]
YW =[.05]
ZW =[.05,.4,.02,.4,.05,.4,.02,.4,.1,.4,.05]
occupancyW = [[1,1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1,1],[1,0,1,0,1,0,1,0,1],[1,1,1,1,1,1,1,1,1],[1,0,0,0,1,0,0,0,1],[1,1,1,1,1,1,1,1,1]]


#funzione che costruisce la finestra
def createWindow(coordinate, occupancy):
    def param(dx,dy,dz):
        x = coordinate[0]
        y = coordinate[1]
        z = coordinate[2]
        lunghezzaX = 0
        altezzaZ = 0#altezza finestra
        dCorner = [y[0]*.5]#dimensione cornice decorativa
        dGlass = y[0]*.5#dimensione vetro
        for i in x: 
            lunghezzaX=lunghezzaX+i
        for i in z:
            altezzaZ=altezzaZ+i
        if dx<(lunghezzaX*2.):
            percent=dx/(lunghezzaX*2.)
            for i in range(0, len(x)):
                x[i] = x[i]*percent
            lunghezzaX = lunghezzaX*percent
        if dy<y[0]:
            print y
            percent=dy/(y[0]*1.)
            y[0] = y[0]*percent
        if dz<altezzaZ:
            print z
            percent=dx/(altezzaZ*1.)
            for i in range(0, len(z)):
                z[i] = z[i]*percent
            altezzaZ = altezzaZ*percent
        window = []
        for i in range(0,2):#come sopra
            for iz in range(0,len(z)):#come sopra
                vect = occupancy[iz]#come sopra
                cont = 0#come sopra
                for ix in vect:#come sopra
                    if ix==1:#come sopra
                        prodXY = PROD([QUOTE([x[cont]]),QUOTE(y)])
                        prod = PROD([prodXY,QUOTE([z[iz]])])
                        window.append(COLOR([51./255.,25./255.,0,1]))
                        window.append(prod)
                    if ix==0:#come sopra
                        if(iz<len(z)-2):#se non ci troviamo a costruire i lucernai
                            #cornice
                            prodXY = PROD([QUOTE([x[cont]-.01]),QUOTE(dCorner)])
                            prod = PROD([prodXY,QUOTE([z[iz]-.01])])
                            window.append(T([1,2,3])([0,y[0]/2.-dCorner[0]/2-.005,0]))
                            window.append(COLOR([153./255.,76./255.,0,1]))
                            window.append(OFFSET([.01,.01,.01])(SKEL_1(prod)))
                            window.append(T([1,2,3])([0,-(y[0]/2.-dCorner[0]/2-.005),0]))
                        #vetro
                        prodXY = PROD([QUOTE([x[cont]]),QUOTE([dGlass])])
                        prod = PROD([prodXY,QUOTE([z[iz]])])
                        window.append(T([1,2,3])([0,y[0]/2.-dGlass/2,0]))
                        window.append(COLOR([150./255.,225./255.,1,1]))
                        window.append(prod)
                        window.append(T([1,2,3])([0,-(y[0]/2.-dGlass/2),0]))
                    window.append(T([1,2,3])([x[cont],0,0]))
                    cont = cont+1
                window.append(T([1,2,3])([-lunghezzaX,0,z[iz]]))#come sopra 
            window.append(T([1,2,3])([lunghezzaX+.005,0,-altezzaZ]))#come sopra
#        maniglia = CUBOID([-.02,.02,.15])
#        window.append(T([1,2,3])([-lunghezzaX-.005-.005-.03,y[0],altezzaZ*.5]))
#        window.append(COLOR([1,191./255.,0,1]))
#        window.append(maniglia)
#        window.append(T([1,2,3])([.03+.05+.005,0,0]))
#        window.append(maniglia)
        return STRUCT(window)
    return param