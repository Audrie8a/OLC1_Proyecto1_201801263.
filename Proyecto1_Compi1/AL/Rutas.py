import platform as pl
import os.path as osp
import os 
Ruta =""
class Rutas:
    def CrearRuta(self,LSTtoken, Texto,Extension):
        global Ruta
        self.sistema=""
        Ruta= self.obtenerPaths(LSTtoken)
        existencia=osp.exists(Ruta)

        if(existencia==True):
            print("Se guardaran archivos aquí"+Ruta)
            self.CrearGuardar(Ruta,Texto,Extension)
        else:       #Se crea ruta si no encuentra la ruta ingresada
            if not os.path.isdir(Ruta):
                oldmask=os.umask(0)             
                os.makedirs(Ruta.rstrip(),mode =755)
                os.umask(oldmask)
            existencia=osp.exists(Ruta)
            if(existencia==True):
                self.CrearGuardar(Ruta,Texto,Extension)

    #END

    def CrearGuardar(self,Ruta,Texto,Extension):
        if self.sistema.lower()=="linux".lower():
            Archivo = open(Ruta+"/Recuperacion."+Extension, "w")
            Archivo.write(Texto)
            Archivo.close()
        elif self.sistema.lower()=="windows".lower():
            Archivo = open(Ruta+"\Recuperacion."+Extension, "w")
            Archivo.write(Texto)
            Archivo.close()
    #END

    def obtenerPaths(self,listTokens):
        PathObtenida=""
        Path1=listTokens[0]
        Path2=listTokens[1]

        Buscando1= str(Path1[3])
        Buscando2= str(Path2[3])

        buquedaSegura1=Buscando1.lower()
        buquedaSegura2=Buscando2.lower()
        palabra1="pathl".lower()
        palabra2="pathw".lower()

        self.sistema = pl.system()

        if(str(self.sistema).lower() =="linux".lower()):
            if(buquedaSegura1.find(palabra1)!=-1):
                PathObtenida=self.extraerRuta(Buscando1)
                return PathObtenida
            elif (buquedaSegura2.find(palabra1)!=-1):
                PathObtenida=self.extraerRuta(Buscando2)
                return PathObtenida
        elif (str(self.sistema).lower=="windows".lower()):
            if(buquedaSegura1.find(palabra2)!=-1):
                PathObtenida=self.extraerRuta(Buscando1)
                return PathObtenida
            elif (buquedaSegura2.find(palabra2)!=-1):
                PathObtenida=self.extraerRuta(Buscando2)
                return PathObtenida
        else:
            PathObtenida="No se encontró"
            return PathObtenida
    #END

    def extraerRuta(self, rut):
        contador=0
        cadena=""
        while(rut[contador]!=":"):
            cadena+=rut[contador]
            contador+=1
        contador+=1
        cadena=""
        tamnioRuta=len(rut)-1
        while(contador<tamnioRuta):
            cadena+=rut[contador]
            contador+=1
        cadena+=str(rut[contador])
        return cadena.lstrip()
    #END

    def setRuta(self,ruta):
        global Ruta
        Ruta=ruta
    #END

    def getRuta(self):
        global Ruta
        return Ruta
    #END
    


#END
        



                
