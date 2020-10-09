from numHoja import numHoja
from tipo import tipo
from nodo import nodo
import metodos

class pilaArbol:
    n=""
    def __init__(self, er):
        global n
        nh=numHoja(er)
        self.pila=[]

        for op in reversed(list(er)):   #Invierte la cadena

            if op == "|":
                izq = self.pila.pop(len(self.pila) - 1)
                der = self.pila.pop(len(self.pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)): #Se verifica si son del tipo nodo
                    n = nodo(op, tipo.OR, 0, izq, der)
                    self.pila.append(n)

            elif op == ".":
                izq = self.pila.pop(len(self.pila) - 1)
                der = self.pila.pop(len(self.pila) - 1)

                if (isinstance(izq,nodo) and isinstance(der,nodo)):
                    n = nodo(op, tipo.AND, 0, izq, der)
                    self.pila.append(n)
            
            elif op == "*":
                unario = self.pila.pop(len(self.pila) - 1)

                if (isinstance(unario,nodo)):
                    n = nodo(op, tipo.KLEENE, 0, unario, None)  #Como es unario, sólo tiene un hijo
                    self.pila.append(n)
                
            else:
                n = nodo(op, tipo.HOJA, nh.getNumHoja(), None, None)
                self.pila.append(n)
                metodos.addHoja(n) # Se agregan las hojas


        self.raiz = self.pila.pop(len(self.pila) - 1)
    #END

    def getRaiz(self):
        return self.raiz
    #END

    def limpiarPila(self):
        global n
        tamanio= len(self.pila)
        if tamanio !=0:
            self.pila.clear()
            n.limpiarPrimeros()
            n.limpiarUltimos()
        
       

