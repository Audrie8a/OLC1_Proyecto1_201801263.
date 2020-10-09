from pilaArbol import pilaArbol
from tablaTran import tablaTran
import metodos
import json
from nodo import nodo

class AFN:
    
    def AFN(self, ER, L):
        ER=ER+"#"

        ConstruirA= pilaArbol(ER)

        Raiz= ConstruirA.getRaiz()


        Raiz.getNodo()      #Se crea la información del nodo (Anulabilidad, primeros y últimos)
        Raiz.siguientes()   #Se crea la tabla siguientes con los nodos obtenidos de la ER

        Transiciones= tablaTran(Raiz)    #Se genera los datos de la tabla de transiciones

        Subgrafo = Transiciones.grafo(L)
        Subgrafo=Subgrafo.replace('digraph','subgraph')

        ConstruirA.limpiarPila()
        metodos.limpiarHojas()
        metodos.limpiarTabla()
        return Subgrafo             #Se genera la parte del dot para la ER ingresada

    
if __name__ == "__main__":
    ER = "....ab*b*|ab"

    reporte = AFN()
    reporte.AFN(ER,"l")



        