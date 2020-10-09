import re
from Rutas import Rutas
from ReporteErrores import ReporteErrores
signos=['%','#','\*', '\-' , '\{', '\}', '\;', '\,', '\.', '\:','\(','\)']
linea = 0
columna = 0
contador = 0
Recuperacion=""

Errores = []
Bitacora=[]     #[Lexema,Estado, Token, Aceptacion]
palabrasReservadas = ['mm','pt','pc','cm','in','vw','vh','em','px','position','bottom','color','display','top','float','Opacity', 'width','right','clear','height','left','text-align','border', 'border-style','font-weight', 'font-style','font-family','font-size','padding-left','padding-bottom','padding-top','padding-right','line-height','min-width','min-height','margin','margin-right','margin-bottom','margin-top','margin-left','max-height','max-width','background-image','background','background-image', ]#text-align                                                           


class AnalizadorL_CSS(ReporteErrores,Rutas):

   
    def funcMainCSS(self, Entrada):
        global contador, Errores, Recuperacion, Bitacora
        Salida=""
        clase = AnalizadorL_CSS()                
        contador=0
        Errores=[]
        Bitacora=[]
        tokens = clase.Analizador(Entrada+"#")
        PalabrasReservadas(tokens)
        for token in tokens:
            print(token)
            #Salida+=listToString(token)+"\n"
        print("---------ERRORES:--------")
        Salida+="---------------BITÁCORA:--------------"+"\n"
        Salida+="\n[Lexema, Estado, Token, Aceptación]\n"
        if(len(Errores)!=0):
            clase.GenerarReporte(Errores,"Reporte Analizador de CSS")
            for err in Errores:
                print (err)
                #Salida+=listToString(err)+"\n"
            if(len(tokens)!=0 and len(Recuperacion)!=0):
                clase.CrearRuta(tokens, Recuperacion,"css")
                Recuperacion=""
        if(len(Bitacora)!=0):
            for tok in Bitacora:
                Salida+=printBitacora(tok)+"\n"
        
        return Salida
    #END

    def Analizador(self, Entrada):
        global linea, columna, contador, Errores, Recuperacion,Bitacora
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
                    Bitacora.append([aux,"S0","Comentario","False"])
                    while(ord(Entrada[contador])!=ord("*") and ord(Entrada[contador+1])!=92 and (contador+1)<len(Entrada)-1):
                        aux+= Entrada[contador]
                        #print(Entrada[contador])
                        if(Entrada[contador]=="\n"):
                            linea+=1
                        #____________________________
                        contador+=1
                        columna+=1
                    Bitacora.append([aux,"S1","Comentario","False"])
                    if(contador+2)<len(Entrada):   
                        #print(Entrada[contador])
                        #print(Entrada[contador+1]) 
                        contador+=2
                        columna+=2
                    aux+="*/"
                    Bitacora.append(["*/","S2","Comentario","True"])
                    listaTokens.append([linea,columna,'Comentario',aux])
                    Recuperacion+=aux
                    aux=""  
                else:
                    Errores.append([linea, columna, Entrada[contador]])
                    Bitacora.append([Entrada[contador],"--","ERROR","False"])
                    contador += 1 
                    columna += 1            

            elif re.search(r"[A-Za-z]", Entrada[contador]): #IDENTIFICADOR  
                Bitacora.append([Entrada[contador],"S0","Identificador","True"])
                listaTokens.append(EstadoIdentificador(linea, columna, Entrada, Entrada[contador]))                
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
            elif Entrada[contador] == '"':
                auxCadena=Entrada[contador]                 
                Bitacora.append([Entrada[contador],"S0","Cadena","False"])              
                contador+=1
                columna +=1
                while Entrada[contador] != '"'and (contador)<len(Entrada)-1:
                    auxCadena+=Entrada[contador]
                    contador+=1
                    columna+=1
                listaTokens.append([linea, columna, "Cadena", auxCadena+Entrada[contador]]) 
                Bitacora.append([auxCadena,"S1","Cadena","False"])  
                Bitacora.append([Entrada[contador],"S2","Cadena","True"])  
                Recuperacion+=auxCadena+Entrada[contador]
                contador +=1
                columna+=1                                       
            else:
                isSign = False
                for sign in signos:
                    palabra = r"^" + sign + "$"                    
                    if re.match(palabra,Entrada[contador], re.IGNORECASE): 
                        listaTokens.append([linea, columna, 'Signo', Entrada[contador]])
                        Bitacora.append([Entrada[contador],"S0","Signo","True"])  
                        Recuperacion+=str(Entrada[contador])
                        contador += 1
                        columna += 1
                        isSign = True
                        break
                  
                if (isSign==False ):                    
                    Errores.append([linea, columna, Entrada[contador]])
                    Bitacora.append([Entrada[contador],"--","ERROR","False"])  
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
    global contador, columna, Recuperacion, Bitacora
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[contador]):#IDENTIFICADOR
            Bitacora.append([Caracter+text[contador],"S0","Identificador","True"])
            return EstadoIdentificador(linea, column, text, Caracter + text[contador]) 
        else:
            if(Caracter.lower()== 'border'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'font'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'padding'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'line'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'min'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'margin'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif (Caracter.lower()== 'max'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'background'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            elif(Caracter.lower()== 'text'.lower() and text[contador].lower()=="-".lower()):
                Bitacora.append([Caracter+text[contador],"S1","PR","False"])
                return EstadoIdentificador(linea, columna, text, Caracter + text[contador])
            else:
                Recuperacion+=Caracter
                Bitacora.append([Caracter,"S0","Identificador","True"])
                return [linea, column, 'identificador', Caracter]
    else:
        Recuperacion+=Caracter
        Bitacora.append([Caracter+text[contador],"S0","Identificador","True"])
        return [linea, column, 'identificador', Caracter]
#END

def EstadoNumero(line, column, text, numero):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#ENTERO
            Bitacora.append([numero+text[contador],"S0","Numero","True"])
            return EstadoNumero(line, column, text, numero + text[contador])
        elif re.search(r"\.", text[contador]):#DECIMAL
            Bitacora.append([numero+text[contador],"S1","Numero","True"])
            return EstadoDecimal(line, column, text, numero + text[contador])
        else:
            Recuperacion+=str(numero)
            Bitacora.append([numero,"S0","Numero","True"])
            return [line, column, 'Número', numero]
            #agregar automata de numero en el arbol, con el valor
    else:
        Recuperacion+=str(numero)
        Bitacora.append([numero,"S0","Numero","True"])
        return [line, column, 'Número', numero]
#END

def EstadoDecimal(line, column, text, decimal):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#DECIMAL
            Bitacora.append([decimal+text[contador],"S0","Numero","False"])
            return EstadoDecimal(line, column, text, decimal + text[contador])
        else:
            Recuperacion+=str(decimal)
            Bitacora.append([decimal,"S0","Numero","True"])
            return [line, column, 'decimal', decimal]
    else:
        Recuperacion+=str(decimal)
        Bitacora.append([decimal,"S0","Numero","True"])
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

def printBitacora(token):
    stri=" "
    counter=0
    while counter<len(token):
        if(counter==0):
            stri+="["+str(token[counter])+"-->"
            counter+=1
        elif (counter==1):
            stri+=str(token[counter])+"--> "
            counter+=1
        elif (counter==2):
            stri+=str(token[counter])+"--> "
            counter+=1
        elif (counter==3):
            stri+=str(token[counter])+"] "
            counter+=1    

    return stri
#END




EntradaTexto= open('entrada.olc1')
contenido = EntradaTexto.read()



if __name__ == "__main__":
    clase = AnalizadorL_CSS()
    clase.funcMainCSS(contenido)