import webbrowser

class ReporteErrores:
    
    def GenerarReporte (self, Lista, Titulo):
        f=open('ReporteErrores.html','w')        
        self.Texto="<h1>"+Titulo+"</h1>\n"
        self.Texto+="<table border=\"1\">"
        self.Texto+=self.Tabla(Lista)
        
        f.write(str(self.Texto))
        f.close()

        webbrowser.open_new_tab('ReporteErrores.html')
    #END

    def Tabla(self,Lista):
        self.Texto+="<tr>\n"
        self.Texto+="<th>Linea</th>\n"
        self.Texto+="<th>Columna</th>\n"
        self.Texto+="<th>Error</th>\n"
        self.Texto+="</tr>\n"

        contador=0
        for token in Lista:
            self.Texto+="<tr>\n"
            self.Texto+="<td>"+str(token[0])+"</td>\n"
            self.Texto+="<td>"+str(token[1])+"</td>\n"
            self.Texto+="<td>"+str(token[2])+"</td>\n"
            self.Texto+="</tr>\n"           

        self.Texto+="</table>"

        return self.Texto
    #END

    



