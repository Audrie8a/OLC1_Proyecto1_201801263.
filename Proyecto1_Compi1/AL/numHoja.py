class numHoja:
    def __init__(self, Expresion):
        self.Expresion = self.limpiar(Expresion) + 1
    #END    

    
    def limpiar(self, Expresion):
        return len(Expresion.replace(".","").replace("|","").replace("*",""))
    #END

    def getNumHoja(self):
        self.Expresion=self.Expresion-1
        return self.Expresion
    #END