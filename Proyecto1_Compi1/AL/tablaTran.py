import metodos
from transicion import transicion
from graphviz import Digraph
class tablaTran:

    def __init__(self, raiz):
        self.estados = []
        self.cont = 0

        # [ nombre, elementos, transiciones, Aceptacion]
        self.estados.append( ["S"+str(self.cont), raiz.primeros, [], False] )
        self.cont += 1

        for estado in self.estados:
            elementos = estado[1]

            for hoja in elementos:

                lexema, siguientes = metodos.getSig(hoja)

                estado_existe = False
                estado_encontrado = ""
                for e in self.estados:
                    if "".join(str(v) for v in e[1]) == "".join(str(v) for v in siguientes):
                        estado_existe = True
                        estado_encontrado = e[0]
                        break


                if not estado_existe:
                    if metodos.aceptacion(hoja):
                        estado[3] = True
                    
                    if lexema == "":
                        continue

                    nuevo = ["S"+str(self.cont), siguientes, [], False]
                    trans = transicion(estado[0], lexema, nuevo[0])
                    estado[2].append(trans)

                    self.cont += 1
                    self.estados.append(nuevo)

                else:
                    if metodos.aceptacion(hoja):
                        estado[3] = True
                    
                    trans_existe = False

                    for trans in estado[2]:
                        if trans.comparar(estado[0], lexema):
                            trans_existe = True
                            break

                    if not trans_existe:
                        trans = transicion(estado[0], lexema, estado_encontrado)
                        estado[2].append(trans)
    #END

    def grafo(self,L):
        dot = Digraph(name='child')
        dot.attr('node', shape='circle')

        # Creamos los nodos
        for e in self.estados:
            dot.node(e[0]+L,e[0]+L)
            if e[3]:
                dot.node(e[0]+L, shape='doublecircle')

        #Creamos las transiciones
        for e in self.estados:
            for t in e[2]:
                dot.edge(t.eIni+L, t.eFin+L, label=t.tran)
        texto=dot.source
        #dot.render('/home/audrie8a/Escritorio/Estados.gv', view=False)
        #print("Grafo de Estados Generado")
        return texto    
    #END