import re
from graphviz import Digraph
from Rutas import Rutas
from ReporteErrores import ReporteErrores
import metodos
from AFN import AFN
import os
import pydotplus
from sklearn import tree
from sklearn.tree import export_graphviz
from PIL import Image


signos=['\(', '\)' , '\{', '\}', '\;', '\,', '\.', '\:']
operadores=['\=', '\*', '\>','\+', '\-','\!', '\<']    #Math.pow, &&, ||
linea = 0
columna = 0
contador = 0
Recuperacion=""
ABC=['A','B','C','D','E','F','G','H']
Errores = []
palabrasReservadas = ['var','if','else','console.log', 'for','while','do','true','false','return', 'function', 'constructor', 'class','this','return', "math.pow"]

bComentario=False
bIdentificadores=False
bNumeros=False
bCadena= False
bCaracter=False
bSimbolo=False
bDecimal = False        
class AnalizadorL_JS(ReporteErrores, Rutas):

   
    def funcMain(self, Entrada):
        global contador, Errores,Recuperacion
        Salida=""
        clase = AnalizadorL_JS()
        contador=0
        Errores=[]
        tokens = clase.Analizador(Entrada+"#")
        PalabrasReservadas(tokens)
        for token in tokens:
            print(token)
            #Salida+=listToString(token)+"\n"
        print("---------ERRORES:--------")
        Salida+="ERRORES:"+"\n"
        if(len(Errores)!=0):
            clase.GenerarReporte(Errores,"Reporte Errores Analizador JS")
            for err in Errores:
                print (err)
                Salida+=listToString(err)+"\n"
        if(len(tokens)!=0 and len(Recuperacion)!=0):
            clase.CrearRuta(tokens, Recuperacion,"js")
            Recuperacion=""
        reporteGrafico(clase.getRuta())
        return Salida
    #END

    def Analizador(self, Entrada):
        global linea, columna, contador, Errores,Recuperacion,bCadena,bCaracter,bComentario,bDecimal,bIdentificadores,bNumeros,bSimbolo
        linea = 1
        columna = 1
        listaTokens = []

        while contador < len(Entrada)-1:
            if Entrada[contador]=="/":  #COMENTARIOS
                aux=""
                if Entrada[contador+1]=="*" and (contador+1)<len(Entrada):    #multilínea
                    contador+=2
                    columna+=2
                    aux="/*"

                    while(Entrada[contador]!="\*" and Entrada[contador+1]!="/" and (contador+1)<len(Entrada)-1):
                        aux+= Entrada[contador]
                        if(Entrada[contador]=="\n"):
                            linea+=1
                        #____________________________
                        contador+=1
                        columna+=1
                    if(contador+2)<len(Entrada):
                        contador+=2
                        columna+=2
                    aux+="*/"
                    listaTokens.append([linea,columna,'Comentario',aux])
                    Recuperacion+=aux
                    bComentario=True
                    aux=""

                elif Entrada[contador+1]=="/" and (contador+1)<len(Entrada):  #unilinea
                    aux+="/"
                    contador+=1
                    columna+=1
                    while(Entrada[contador]!="\n" and (contador)<len(Entrada)):
                        aux+= Entrada[contador]                        
                        contador+=1
                        columna+=1

                    listaTokens.append([linea,columna,'Comentario',aux])
                    bComentario=True
                    Recuperacion+=aux
                    aux=""
                else:                           #signo aritmético
                    listaTokens.append([linea,columna,'Operador',Entrada[contador]])
                    Recuperacion+=str(Entrada[contador])   
                    contador+=1
                    bSimbolo=True

            elif re.search(r"[A-Za-z]", Entrada[contador]): #IDENTIFICADOR  
                listaTokens.append(EstadoIdentificador(linea, columna, Entrada, Entrada[contador]))                
                bIdentificadores=True
            elif re.search(r"[\n]", Entrada[contador]): #SALTO DE LINEA
                Recuperacion+=str(Entrada[contador])
                contador += 1
                linea += 1
                columna = 1 
            elif re.search(r"[ \t]", Entrada[contador]):#ESPACIOS Y TABULACIONES
                Recuperacion+=str(Entrada[contador])
                contador += 1
                columna += 1 
            elif re.search(r"[0-9]", Entrada[contador]): #NUMERO
                listaTokens.append(EstadoNumero(linea, columna, Entrada, Entrada[contador]))
                bSimbolo=True
            elif Entrada[contador] == '"':
                auxCadena=Entrada[contador]
                contador+=1
                columna +=1
                while Entrada[contador] != '"'and (contador)<len(Entrada)-1:
                    auxCadena+=Entrada[contador]
                    contador+=1
                    columna+=1
                listaTokens.append([linea, columna, "Cadena", auxCadena+Entrada[contador]]) 
                Recuperacion+=auxCadena+Entrada[contador]
                bCadena=True
                contador +=1
                columna+=1  
                                      
            elif Entrada[contador]=="'":
                auxCaracter=Entrada[contador]
                contador+=1
                columna+=1
                while(Entrada[contador]!="'"and (contador)<len(Entrada)-1):
                    auxCaracter+=Entrada[contador]
                    contador+=1
                    columna+=1
                auxCaracter+=Entrada[contador]               
                listaTokens.append([linea, columna, 'Caracter', auxCaracter])
                Recuperacion+=auxCaracter
                bCaracter=True
                contador+=1
                columna+=1
            else:
                isSign = False
                isOper= False
                for sign in signos:
                    palabra = r"^" + sign + "$"                    
                    if re.match(palabra,Entrada[contador], re.IGNORECASE): 
                        listaTokens.append([linea, columna, 'Signo', Entrada[contador]])
                        Recuperacion+=str(Entrada[contador])
                        contador += 1
                        columna += 1
                        isSign = True
                        break

                if(isSign==False):
                    for operador in operadores:
                        oper=r"^" + operador + "$"
                        if re.match(oper, Entrada[contador], re.IGNORECASE):
                            listaTokens.append([linea, columna, 'Operador', Entrada[contador]])
                            Recuperacion+=str(Entrada[contador])
                            bSimbolo=True
                            contador += 1
                            columna += 1
                            isOper = True
                            break
                    if(Entrada[contador]=='&' and Entrada[contador+1]=='&' and (contador+1)<len(Entrada)):
                        concatenado=Entrada[contador]+Entrada[contador+1]
                        listaTokens.append([linea,columna,'Operador',concatenado])
                        Recuperacion+=concatenado
                        bSimbolo=True
                        contador+=2
                        columna +=2
                        isOper=True
                    if(Entrada[contador]=='|' and Entrada[contador+1]=='|' and (contador+1)<len(Entrada)):
                        concatenado2=Entrada[contador]+Entrada[contador+1]
                        listaTokens.append([linea,columna,'Operador', concatenado2 ])
                        Recuperacion+=concatenado2
                        bSimbolo=True
                        contador+=2
                        columna +=2
                        isOper=True
                                        
                if (isSign==False and isOper==False):                    
                    Errores.append([linea, columna, Entrada[contador]])
                    contador += 1 
                    columna += 1
                           
        #END

        return listaTokens    
    #END   

def PalabrasReservadas(lstTokens):
    for token in lstTokens:
        if token[2] == 'identificador':
            for reservada in palabrasReservadas:
                palabra = r"^" + reservada + "$"
                if re.match(palabra, token[3], re.IGNORECASE):
                    token[2] = 'reservada'
                    break
#END

def EstadoIdentificador (linea, column, text, Caracter):
    global contador, columna,Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[contador]):#IDENTIFICADOR
            return EstadoIdentificador(linea, column, text, Caracter + text[contador])
        else:
            if(Caracter.lower()== 'math'.lower() and text[contador].lower()==".".lower()):
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            else:
                Recuperacion+=Caracter
                return [linea, column, 'identificador', Caracter]                
            #agregar automata de identificador en el arbol, con el valor
    else:
        Recuperacion+=Caracter
        return [linea, column, 'identificador', Caracter]
#END

def EstadoNumero(line, column, text, numero):
    global contador, columna,Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#ENTERO
            return EstadoNumero(line, column, text, numero + text[contador])
        elif re.search(r"\.", text[contador]):#DECIMAL
            return EstadoDecimal(line, column, text, numero + text[contador])
        else:
            Recuperacion+=str(numero)
            return [line, column, 'Número', numero]
            #agregar automata de numero en el arbol, con el valor
    else:
        Recuperacion+=str(numero)
        return [line, column, 'Número', numero]
#END

def EstadoDecimal(line, column, text, decimal):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#DECIMAL
            return EstadoDecimal(line, column, text, decimal + text[contador])
        else:
            Recuperacion+=str(decimal)
            return [line, column, 'decimal', decimal]
            #agregar automata de decimal en el arbol, con el valor
    else:
        Recuperacion+=str(decimal)
        return [line, column, 'decimal', decimal]
#END

def listToString(token):
    stri=" "
    counter=0
    while counter<len(token):
        if(counter==0):
            stri+="["+str(token[counter])+", "
            counter+=1
        elif (counter==1):
            stri+=str(token[counter])+", "
            counter+=1
        elif (counter==2):
            stri+=str(token[counter])+"] "
            counter+=1


        

    return stri
#END

def subGrafosRG():
    global bCadena,bCaracter,bComentario,bDecimal,bIdentificadores,bNumeros,bSimbolo
    if(bCadena):
        metodos.addER("...\"*C\"")  
    if (bCaracter):
        metodos.addER("...'*C'")
    if (bComentario):
        metodos.addER(".|..//*C.../A*.*C*E.A/")
    if (bDecimal):
        metodos.addER("...*NP*N")   #DECIMAL   ...+NP+N
    if (bIdentificadores):
        metodos.addER("..*L*||LN_") #IDENTIFICADORES ..+L*||LN_
    if (bNumeros):
        metodos.addER(".*N")        #NUMERO  .+N
    if(bSimbolo):
        metodos.addER(".*S")        #Simbolo .+S

#END

def reporteGrafico(Ruta):
    global ABC
    claseAFN=AFN()
    dot = Digraph(name='parent')
    dot.attr('node', shape='circle')
    subGrafosRG()
    listaER=metodos.getListER()
    contar=len(listaER)
    dot.node("A0","A0")
    conteo =0
    while contar!=0:
        dot.edge("A0","S0"+ABC[conteo])
        contar-=1
        conteo+=1

    contar=0
    TextoG=dot.source.replace('}'," ")
    TextoSG=""
    print (TextoG)
    for sg in listaER:
        SubGrafo=claseAFN.AFN(sg, ABC[contar])
        print("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        print(SubGrafo)
        print ("°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°°")
        TextoSG+="\n"+SubGrafo
        contar+=1
    print("----------------------------------------")    
    Texto=TextoG+"\n"+TextoSG+"\n}"
    print(Texto)       
    arch = open(Ruta+"/ArbolJS.dot", "w")
    arch.write(Texto)
    arch.close()
    os.environ["PATH"]+=os.pathsep+Ruta+'/ArbolJS.dot'
    os.system('dot -Tpng '+Ruta+'/ArbolJS.dot -o '+Ruta+'/ArbolJS.png')
    f= Image.open(Ruta+"ArbolJS.png")
    f.show()
    #END

    




EntradaTexto= open('entrada.olc1')
contenido = EntradaTexto.read()



if __name__ == "__main__":
    clase = AnalizadorL_JS()
    clase.funcMain(contenido)