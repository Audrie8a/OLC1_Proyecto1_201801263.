from tipo import tipo
import metodos


class nodo:

    def __init__(self, lexema, tipo, numero, izq, der):     
        self.primeros = []
        self.ultimos = []
        self.anulable = True

        self.lexema = lexema
        self.tipo = tipo
        self.numero = numero

        self.aceptacion = False
        if lexema == "#":
            self.aceptacion = True
        
        self.izq = izq
        self.der = der
    #END


    def getNodo(self):
        izq = self.izq.getNodo() if isinstance(self.izq, nodo) else None
        der = self.der.getNodo() if isinstance(self.der, nodo) else None


        if self.tipo == tipo.HOJA:      #TIPO HOJA

            self.anulable = False
            self.primeros.append(self.numero)
            self.ultimos.append(self.numero)

        elif self.tipo == tipo.AND:     #TIPO CONCATENACION

            if ( isinstance(izq, nodo) and isinstance(der, nodo) ):
                # Anulable
                self.anulable = izq.anulable and der.anulable

                # Primeros
                if izq.anulable:    #C1 Anulable    Se Unen
                    self.primeros.extend(izq.primeros)  #Primeros C1
                    self.primeros.extend(der.primeros)  #Primeros C2
                else:
                    self.primeros.extend(izq.primeros)  

                # Ultimos
                if der.anulable:    #C2 Anulable    Se Unen
                    self.ultimos.extend(izq.ultimos)    #Ultimos C1
                    self.ultimos.extend(der.ultimos)    #Ultimos C2
                else:
                    self.ultimos.extend(der.ultimos)

        elif self.tipo == tipo.OR:      #TIPO ALTERNANCIA

            if ( isinstance(izq, nodo) and isinstance(der, nodo) ):
                # Anulable
                self.anulable = izq.anulable or der.anulable    #Anulable si cualquier hijo es anulable

                # Primeros
                self.primeros.extend(izq.primeros)  #Siempre se unen los first de los hijos
                self.primeros.extend(der.primeros)

                # Ultimos
                self.ultimos.extend(izq.ultimos)    #Siempre se unen los last de los hijos
                self.ultimos.extend(der.ultimos)

        elif self.tipo == tipo.KLEENE:      #TIPO CERRADURA DE KLEENE

            if isinstance(izq, nodo):
                self.anulable = True        #Siempre es anulable
                self.primeros.extend(izq.primeros)  #Se copial los first y last del hijo
                self.ultimos.extend(izq.ultimos)

        else:
            pass

        return self
    #END    

    def siguientes(self):
        izq = None if (self.izq == None) else self.izq.siguientes()
        der = None if (self.der == None) else self.der.siguientes()


        if self.tipo == tipo.AND:       #TIPO CONCATENACION
            for i in izq.ultimos:
                nodo = metodos.getHoja(i)
                metodos.append(nodo.numero, nodo.lexema, der.primeros) #Creo la tabla Siguientes


        elif self.tipo == tipo.KLEENE:      #TIPO CERRADURA DE KLEENE
            for i in izq.ultimos:
                nodo = metodos.getHoja(i)
                metodos.append(nodo.numero, nodo.lexema, izq.primeros)


        else:
            pass

        return self
    #END

    def limpiarPrimeros(self):
        self.primeros.clear()
    #END

    def limpiarUltimos(self):
        self.ultimos.clear()
    #END