from tkinter import *
from tkinter import ttk
from tkinter import Tk, Menu, messagebox, filedialog, ttk, Label, scrolledtext, INSERT, END, Button, Scrollbar,BOTTOM, RIGHT, Y, Frame, Canvas, HORIZONTAL, VERTICAL, simpledialog,X,Text
from AnalizadorL_JS import AnalizadorL_JS
from AnalizadorL_CSS import AnalizadorL_CSS
from colorama import *
from AnalizadorSintactico import Analizadorsintactico
from AnalizadorL_HTML import AnalizadorL_HTML

class ML_WEB(AnalizadorL_JS,AnalizadorL_CSS, AnalizadorL_HTML):
    
    def __init__ (self, window):  
        
        self.root = window
        self.root.title("ML WEB")
        self.Entrada=""
        self.extension="Audrie8a"

        frame = Frame(root, bg="dark slate gray")
        frame = Frame(root, bg="dark slate gray")

        canvas = Canvas(frame, bg="dark slate gray")
        scroll = Frame(canvas, bg="dark slate gray")
        self.editor = scrolledtext.ScrolledText(scroll, undo = True, width = 50, height = 20, font = ("Arial", 15), background = 'dark slate gray',  foreground = "dark slate gray")
        scrollbar = Scrollbar(frame, orient=VERTICAL, command=canvas.yview)


        MenuOpciones = Menu(root)
        root.config(menu = MenuOpciones, width = 1000, height = 600)

        archivoMenu = Menu(MenuOpciones, tearoff=0)

        MenuOpciones.add_cascade(label = "Archivo", menu = archivoMenu)
        archivoMenu.add_command(label = "Abrir",  command = self.abrir)
        archivoMenu.add_command(label = "Guardar", command= self.guardar)
        archivoMenu.add_command(label = "Guardar Como",command= self.guardarComo)
        MenuOpciones.add_command(label = "Analizar",  command = self.analizar)
        MenuOpciones.add_command(label = "Salir",  command = self.salir)


        scroll.bind("<Configure>",lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scroll, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set, width = 1280, height = 800)

        ttk.Label(scroll, text = "Editor", font = ("Arial", 20), background='dark slate gray', foreground = "pale green").grid(column = 1, row = 0)

        self.editor = scrolledtext.ScrolledText(scroll, undo = True, width = 50, height = 20, font = ("Arial", 15), background = 'pale green',  foreground = "black")

        self.editor.grid(column = 1, row = 1, pady = 25, padx = 25)

        ttk.Label(scroll, text = "Consola", font = ("Arial", 20), background='dark slate gray', foreground = "pale green").grid(column = 2, row = 0)

        self.consola = scrolledtext.ScrolledText(scroll, undo = True, width = 50, height = 20, font = ("Arial", 15), background = 'pale green',  foreground = "black")

        self.consola.grid(column = 2, row = 1, pady = 10, padx = 10)


        frame.grid(sticky='news')
        canvas.grid(row=0,column=1)
        scrollbar.grid(row=0, column=2, sticky='ns')

        self.editor.focus()
        self.consola.focus()

        
    #END

    #FUNCIONES----------------------------------------------------------------------------------------------------------

    def salir(self):
        value = messagebox.askokcancel("Salir", "Está seguro que desea salir?")
        if value :
            root.destroy()
    #END

    def abrir(self):
        global archivo
        archivo = filedialog.askopenfilename(title = "Abrir", initialdir = "C:/")        
        entrada = open(archivo)
        contenido = entrada.read()
        strArchivo=str(archivo)
        Direccion=strArchivo.split('.')
        self.extension=Direccion[-1]
        print(Direccion[-1])
        self.editor.delete(1.0, END)
        self.editor.insert(INSERT, contenido)
        #print(Fore.BLUE+"Abierto")
        
        entrada.close()
    #END

    def guardarComo(self):
        global archivo
        guardar = filedialog.asksaveasfilename(title = "Guardar Como", initialdir = "C:/")
        fileguardar = open(guardar, "w+")
        fileguardar.write(self.editor.get(1.0, END))
        fileguardar.close()
        archivo = guardar
    #END

    def guardar(self):
        global archivo
        if archivo == "":
            self.guardarComo()
        else:
            guardarc = open(archivo, "w")
            guardarc.write(self.editor.get(1.0, END))
            guardarc.close()
    #END

    def obtenerTexto(self, Texto):
        return Texto

    def analizar(self):
        try:
            self.Entrada=self.editor.get("1.0",END)
            AuxEntrada= self.Entrada.strip()
            if(len(AuxEntrada) != 0):
                if(self.extension=="Audrie8a"):
                    pregunta=messagebox.askquestion("Pregunta", "Desea utilizar el Analizador de JS?")
                    if(pregunta=='yes'):
                         Errores= app.funcMain(self.Entrada)
                    else:
                        pregunta2=messagebox.askquestion("Pregunta","Desea utilizar el Analizador de CSS?")  
                        if(pregunta2=='yes'):
                            Errores =app.funcMainCSS(self.Entrada)
                        else:
                            pregunta3=messagebox.askquestion("Pregunta","Desea utilizar el Analizador de HTML?")
                            if(pregunta3=='yes'):
                                Errores=app.funcMainHTML(self.Entrada)
                            else:
                                pregunta4=messagebox.askquestion("Pregunta","Desea utilizar el Analizador Sintactico?") 
                                if(pregunta4=='yes'):
                                    Texto=self.Entrada.strip().split("\n")
                                    Respuesta=""
                                    for lexema in Texto:
                                        clase=Analizadorsintactico(lexema)
                                        Respuesta+=str(clase.Resultado)+"\n"
                                                            
                                    Resultados=Respuesta.split("\n")
                                    contador=0
                                    lista=[]
                                    for lex in Texto:
                                        lista.append([lex,Resultados[contador]])
                                        contador+=1

                                    Errores=""                            
                                    clase.generarReporte(lista)
                                else:    
                                    messagebox.showinfo("Respuesta", "Lo sentimos, no contamos con más analizadores. :(")
                    
                else:
                    if(self.extension.lower()=='js'.lower()):
                        Errores= app.funcMain(self.Entrada)
                        self.extension="Audrie8a"
                    elif (self.extension.lower()=='css'.lower()):
                        Errores =app.funcMainCSS(self.Entrada)
                        self.extension="Audrie8a"
                    elif (self.extension.lower()=='html'.lower()):
                        Errores=app.funcMainHTML(self.Entrada)
                        self.extension="Audrie8a"
                    elif(self.extension.lower()=='rmt'.lower()):
                        Texto=self.Entrada.strip().split("\n")
                        Respuesta=""
                        for lexema in Texto:
                            clase=Analizadorsintactico(lexema)
                            Respuesta+=str(clase.Resultado)+"\n"
                                                
                        Resultados=Respuesta.split("\n")
                        contador=0
                        lista=[]
                        for lex in Texto:
                            lista.append([lex,Resultados[contador]])
                            contador+=1

                        Errores=""                            
                        clase.generarReporte(lista)
                        self.extension="Audrie8a"
                                

                self.consola.delete(1.0,END)
                if (len(Errores)!=0):
                    self.consola.insert(INSERT, Errores)                
                messagebox.showinfo("Respuesta","El Análisis finalizado")
            else:
                messagebox.showinfo("Respuesta","No se ha ingresado ningún texto a Analizar")
        except Exception as e:
            print (e)
            messagebox.showinfo("Respuesta","Ocurrió un error al Analizar el archivo")
            
    #END    


if __name__== '__main__':
    root= Tk()
    app= ML_WEB(root)
    root.mainloop()