#-----------------------------------------------HOJAS----------------------------------------------
lista = []

def addHoja(nodo):
    global lista
    lista.append(nodo)
#END

def getHoja(numHoja):
    global lista

    for hoja in lista:
        if hoja.numero == numHoja:
            return hoja
    
    return None
#END

def aceptacion(numHoja):
    global lista

    for h in lista:
        if h.numero == numHoja:
            return h.aceptacion
    
    return False
#END

def limpiarHojas():
    global lista
    lista.clear()

#------------------------------------------TABLA SIGUIENTES----------------------------------------

tabla = []

def append(numNodo, lexema, sigLista):
    global tabla

    for sig in tabla:
        if (sig[0] == numNodo) and (sig[1] == lexema):
            for new in sigLista:
                if not(new in sig[2]):
                    sig[2].append(new)

            return

    tabla.append( [numNodo, lexema, sigLista] )
#END

def getSig(numNodo):
    global tabla

    for sig in tabla:
        if (sig[0] == numNodo):
            return sig[1],sig[2]

    return "",[]
#END

def limpiarTabla():
    global tabla
    tabla.clear()

#----------------------------------------Grafo------------------------------------------

listER=[]

def addER(er):
    global listER
    listER.append(er)

def getListER():
    global listER
    return listER

def limpiarER():
    global listER
    listER.clear()
#--------------------------------------Analisis Sintactico-------------------------------
 
pila = []

def addPila(Caracter):
    global pila
    pila.append(Caracter)

def popPila():
    global pila
    pila.pop()

def limpiarPila():
    global pila
    pila.clear()

def getPila():
    global pila
    return pila


