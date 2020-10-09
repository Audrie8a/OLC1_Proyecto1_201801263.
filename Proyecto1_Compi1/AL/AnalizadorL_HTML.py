import re
from Rutas import Rutas
from ReporteErrores import ReporteErrores
signos=['=']
linea = 0
columna = 0
contador = 0
Recuperacion=""
bPath1=False
bPath2=False

Errores = []
palabrasReservadas = ['html','li','head','title','body','h1','h2','h3','h4','h5','h6','p','br','img','href','a','o','u','style','table','th','tr','td','caption','colgroup','col','thead','tbody','tfoot']                                                           


class AnalizadorL_HTML(ReporteErrores,Rutas):

   
    def funcMainHTML(self, Entrada):
        global contador, Errores, Recuperacion
        Salida=""
        clase = AnalizadorL_HTML()                
        contador=0
        Errores=[]
        tokens = clase.Analizador(Entrada+"#")
        PalabrasReservadas(tokens)
        for token in tokens:
            print(token)
            #Salida+=listToString(token)+"\n"
        print("---------ERRORES:--------")
        Salida+="---------------ERRORES:--------------"+"\n"
        if(len(Errores)!=0):
            clase.GenerarReporte(Errores,"Reporte Analizador de HTML")
            for err in Errores:
                print (err)
                #Salida+=listToString(err)+"\n"
            if(len(tokens)!=0 and len(Recuperacion)!=0):
                clase.CrearRuta(tokens, Recuperacion,"html")
                Recuperacion=""
        clase.CrearRuta(tokens, Recuperacion,"html")
        
        return Salida
    #END

    def Analizador(self, Entrada):
        global linea, columna, contador, Errores, Recuperacion,bPath1, bPath2
        linea = 1
        columna = 1
        listaTokens = []

        while contador < len(Entrada)-1:
            if(Entrada[contador]=='<'):
                contador+=1
                if bPath1==False:
                    if(Entrada[contador]=='!'and Entrada[contador+1]=='-'and Entrada[contador+2]=='-'):
                        auxEntrada=Entrada[contador]+Entrada[contador+1]
                        contador+=3
                        while Entrada[contador]!='-'and Entrada[contador+1]!='-'and Entrada[contador+1]!='>':
                            auxEntrada+=Entrada[contador]
                            contador+=1
                        auxEntrada+=Entrada[contador]+Entrada[contador+1]+Entrada[contador+2]
                        contador+=5
                        listaTokens.append([linea,columna,"Comentario",auxEntrada])
                    #listaTokens.append(EstadoComentario(linea,columna, Entrada,Entrada[contador]))
                    bPath1=True
                    if bPath2==False:
                        if(Entrada[contador]=='<' and Entrada[contador+1]=='!'and Entrada[contador+2]=='-'and Entrada[contador+3]=='-'):
                            auxEntrada2=Entrada[contador]+Entrada[contador+1]+Entrada[contador+2]
                            contador+=4
                            while Entrada[contador]!='-'and Entrada[contador+1]!='-'and Entrada[contador+1]!='>':
                                auxEntrada2+=Entrada[contador]
                                contador+=1
                            auxEntrada2+=Entrada[contador]+Entrada[contador+1]+Entrada[contador+2]
                            contador+=5
                            listaTokens.append([linea,columna,"Comentario",auxEntrada2])
                            #listaTokens.append(EstadoComentario(linea,columna, Entrada,Entrada[contador]))
                            bPath2=True
                elif re.search(r"[A-Za-z]", Entrada[contador]): #IDENTIFICADOR  
                    listaTokens.append(EstadoIdentificador(linea, columna, Entrada, Entrada[contador]))
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
                    contador +=1
                    columna+=1
                elif  Entrada[contador]=="'":
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
                    contador+=1
                    columna+=1
                elif Entrada[contador]=='=':
                    listaTokens.append([linea, columna, "Signo", Entrada[contador]]) 
                    Recuperacion+=Entrada[contador]
                    contador +=1
                    columna+=1
                elif Entrada[contador]=='/':
                    listaTokens.append([linea, columna, "Signo", Entrada[contador]]) 
                    Recuperacion+=Entrada[contador]
                    contador +=1
                    columna+=1
                elif Entrada[contador]=='>':
                    listaTokens.append([linea, columna, "Signo", Entrada[contador]]) 
                    Recuperacion+=Entrada[contador]
                    contador +=1
                    columna+=1

            elif Entrada[contador]=='/':
                    listaTokens.append([linea, columna, "Signo", Entrada[contador]]) 
                    Recuperacion+=Entrada[contador]
                    contador +=1
                    columna+=1
            elif Entrada[contador]=='>':
                listaTokens.append([linea, columna, "Signo", Entrada[contador]]) 
                Recuperacion+=Entrada[contador]
                contador +=1
                columna+=1
            else:
                while(Entrada[contador]!='<' and contador<len(Entrada)-1):
                    if re.search(r"[\n]", Entrada[contador]): #SALTO DE LINEA
                        Recuperacion+=str(Entrada[contador])
                        contador += 1
                        linea += 1
                        columna = 1 
                    elif re.search(r"[ \t]", Entrada[contador]):#ESPACIOS Y TABULACIONES
                        Recuperacion+=str(Entrada[contador])
                        contador += 1
                        columna += 1 
                    elif re.search(r"[0-9]", Entrada[contador]): #NUMERO
                        listaTokens.append(EstadoNumeroTXT(linea, columna, Entrada, Entrada[contador]))
                    elif re.search(r"[A-Za-z]", Entrada[contador]): #IDENTIFICADOR  
                        listaTokens.append(EstadoIdentificadorTXT(linea, columna, Entrada, Entrada[contador]))                
                
                    else:
                        if Entrada[contador]!='<':
                            listaTokens.append([linea, columna,'Texto',Entrada[contador]])
                            contador += 1 
                            columna += 1
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

def EstadoIdentificadorTXT (linea, column, text, Caracter):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[contador]):#IDENTIFICADOR
            return EstadoIdentificadorTXT(linea, column, text, Caracter + text[contador]) 
        else:
            Recuperacion+=Caracter
            return [linea, column, 'Texto', Caracter]           
    else:
        Recuperacion+=Caracter
        return [linea, column, 'Texto', Caracter]
#END

def EstadoIdentificador (linea, column, text, Caracter):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[a-zA-Z_0-9]", text[contador]):#IDENTIFICADOR
            return EstadoIdentificador(linea, column, text, Caracter + text[contador]) 
        else:
            Recuperacion+=Caracter
            return [linea, column, 'identificador', Caracter]           
    else:
        Recuperacion+=Caracter
        return [linea, column, 'identificador', Caracter]
#END

def EstadoNumeroTXT(line, column, text, numero):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#ENTERO
            return EstadoNumeroTXT(line, column, text, numero + text[contador])
        elif re.search(r"\.", text[contador]):#DECIMAL
            return EstadoDecimalTXT(line, column, text, numero + text[contador])
        else:
            Recuperacion+=str(numero)
            return [line, column, 'Texto', numero]
            #agregar automata de numero en el arbol, con el valor
    else:
        Recuperacion+=str(numero)
        return [line, column, 'Texto', numero]
#END

def EstadoDecimalTXT(line, column, text, decimal):
    global contador, columna, Recuperacion
    contador += 1
    columna += 1
    if contador < len(text):
        if re.search(r"[0-9]", text[contador]):#DECIMAL
            return EstadoDecimalTXT(line, column, text, decimal + text[contador])
        else:
            Recuperacion+=str(decimal)
            return [line, column, 'decimal', decimal]
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
def EstadoComentario(line, column, text, Caracter):
    global contador, columna, Recuperacion
    if contador < len(text):
        if re.search(r"(\<\!\-\-(\s*|.*?)*\-\-\!\>)",Caracter):
            Recuperacion+= Caracter
            return [line, column, 'Comentario', Caracter]
        else:
            contador+=1
            column+=1
            if re.search(r"[\n]", text[contador]): #SALTO DE LINEA
                line += 1
            Caracter+=text[contador]                
            EstadoComentario(line,column,text,Caracter)
    
        


EntradaTexto= open('entrada.olc1')
contenido = EntradaTexto.read()



if __name__ == "__main__":
    clase = AnalizadorL_HTML()
    clase.funcMainHTML(contenido)