import re
import webbrowser

class Analizadorsintactico:

    

    def __init__(self, Entrada):
        self.Resultado=True
        self.contador=0
        self.Signos=['\+','\-',' ','\*','/','\(','\)']#Num e identificador
        self.Estados=['E','T','G','R','F']

        Entrada= Entrada+"#"
        self.pila=[]
        self.pila.append("#")
        self.P(Entrada)
        self.pila.clear()
        

    #END

    def P(self,Entrada):
        self.pila.append('E')
        self.q(Entrada)
    #END

    def q(self, Entrada):        
        self.contador=0
        auxPila=[]
        while(len(self.pila)!=0 or auxPila!="#"):
            auxPila=self.pila.pop()            
            CondicionE=self.pruebaEstados(auxPila, Entrada)
            if(CondicionE==False):
                CondicionEN=self.pruebaEntrada(auxPila,Entrada)
                if CondicionEN==False:
                    self.Resultado=False
                    break   
                
            print(self.imprimirPila())     
    #END

    def imprimirPila(self):
        texto=""
        for item in reversed(self.pila):
            texto+=item
        return texto

    def pruebaEstados(self,auxPila, Entrada):
        condicionE=False
        for state in self.Estados:
            palabra = state
            if re.match(palabra,auxPila, re.IGNORECASE): 
                condicionE=True
                if(palabra=='E'):
                    self.pila.append('G')
                    self.pila.append('T')                
                elif(palabra=='G'):
                    if(Entrada[self.contador]=='+'):
                        self.pila.append('G')
                        self.pila.append('T')
                        self.pila.append('+')
                    elif(Entrada[self.contador]=='-'):                                           
                        self.pila.append('G')
                        self.pila.append('T')
                        self.pila.append('-')
                    else:
                        print(" ")
                elif(palabra=='T'):
                    self.pila.append('R')
                    self.pila.append('F')
                elif(palabra=='R'):
                    if(Entrada[self.contador]=='*'):
                        self.pila.append('R')
                        self.pila.append('F')
                        self.pila.append('*')
                    elif(Entrada[self.contador]=='/'):                                           
                        self.pila.append('R')
                        self.pila.append('F')
                        self.pila.append('/')
                    else:
                        print(" ")
                elif(palabra=='F'):
                    if re.search(r"[A-Za-z]", Entrada[self.contador]): #IDENTIFICADOR 
                        self.pila.append('ID')                                            
                        #self.EstadoIdentificador(Entrada,Entrada[self.contador],self.contador)
                    elif (Entrada[self.contador]=='('):
                        self.pila.append(')')
                        self.pila.append('E')
                        self.pila.append('(')
                    elif re.search(r"[0-9]", Entrada[self.contador]): #NUMERO
                        self.pila.append('NUM')
                    else:
                        condicionE=False
        return condicionE
    #END

    def pruebaEntrada(self, auxPila,Entrada):
        condicionEn=False
        for indx in self.Signos:
            pedazo=str(indx)

            if re.match(pedazo,auxPila,re.IGNORECASE):
                condicionEn=True
                self.contador+=1
            elif auxPila=='ID':
                if re.search(r"[A-Za-z]", Entrada[self.contador]): #IDENTIFICADOR 
                   self.EstadoIdentificador(Entrada,Entrada[self.contador])
                   condicionEn=True
                else:
                    self.Resultado=False
                    return
            elif auxPila=='NUM':
                if re.search(r"[0-9]", Entrada[self.contador]): #NUMERO
                    self.EstadoNumero(Entrada, Entrada[self.contador])
                    condicionEn=True
            else:
                if auxPila=='#':
                    return        
                      
        return condicionEn
    #END

    def EstadoNumero(self,text, numero):
        self.contador += 1
        
        if self.contador < len(text):
            if re.search(r"[0-9]", text[self.contador]):#ENTERO
                return self.EstadoNumero(text, numero + text[self.contador])
            elif re.search(r"\.", text[self.contador]):#DECIMAL
                return self.EstadoDecimal(text, numero + text[self.contador])
            else:
                return numero
                #agregar automata de numero en el arbol, con el valor
        else:
            return numero
    #END

    def EstadoDecimal(self, text, decimal):

        self.contador += 1

        if self.contador < len(text):
            if re.search(r"[0-9]", text[self.contador]):#DECIMAL
                return self.EstadoDecimal(text, decimal + text[self.contador])
            else:
                return decimal
                #agregar automata de decimal en el arbol, con el valor
        else:
            return decimal
    #END


    def EstadoIdentificador (self,text,Caracter):
        self.contador += 1
        if self.contador < len(text):
            if re.search(r"[a-zA-Z_0-9]", text[self.contador]):#IDENTIFICADOR
                return self.EstadoIdentificador(text, Caracter + text[self.contador])
            else:                
                return Caracter               
                #agregar automata de identificador en el arbol, con el valor
        else:

            return Caracter

    def getRespuesta(self):
        Respuesta = str(self.Resultado)
        return Respuesta

    def generarReporte(self,Lista):
        f=open('ReporteErrores.html','w')        
        self.Texto="<h1>"+"Reporte Analizador Sintactico"+"</h1>\n"
        self.Texto+="<table border=\"1\">"
        self.Texto+=self.Tabla(Lista)

        f.write(str(self.Texto))
        f.close()

        webbrowser.open_new_tab('ReporteErrores.html')
        
    #END

    def Tabla(self,Lista):
        self.Texto+="<tr>\n"
        self.Texto+="<th>Linea</th>\n"
        self.Texto+="<th>Expresion</th>\n"
        self.Texto+="<th>Evaluacion</th>\n"
        self.Texto+="</tr>\n"

        contador=0
        for token in Lista:
            self.Texto+="<tr>\n"
            self.Texto+="<td>"+str(contador)+"</td>\n"
            self.Texto+="<td>"+str(token[0])+"</td>\n"
            self.Texto+="<td>"+str(token[1])+"</td>\n"
            self.Texto+="</tr>\n"     
            contador+=1    

        self.Texto+="</table>"

        return self.Texto
    #END
#END              

if __name__ == "__main__":
    clase = Analizadorsintactico("4+5-7+(3+x)")#"((4-6*(1/8)/2)+(6-9*(2))-(5)*(3*x)/(var1))")
    print(clase.Resultado)

        
