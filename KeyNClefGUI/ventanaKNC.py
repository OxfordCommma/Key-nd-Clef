from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from albumesKNC import *

class Ventana(Frame): #Frame es la clase Padre. Es decir, la instancia de Ventana es un Frame (el frame principal)
    
    albumes = Albumes() #Variable a nivel de clase. Instancia de clase Albumes

    def __init__(self, master = None): 

        super().__init__(master, width = 956, height = 356, bg = "#171717") # Establecemos el frame principal, indicando su contenedor (será la raíz) y sus dimensiones 
        self.master = master # guardamos en una variable al contenedor (la raíz)
        self.pack() # colocamos este frame principal en la raíz del GUI
        self.create_widgets() # ejecutamos la función que coloca los widgets en el frame principal (widgets, otros frames hijos)
        self.llenarTabla() #Cuando se abre el programa, se cargan todos los datos de la BBDD

        #Al abrirse el programa, se habilitan sólo los botones azules, para que el usuario pueda dar inicio 
        #al proceso de ingreso de datos con el botón "Nuevo" u otra operación. Se deshabilitan los botones Guardar y Cancelar
        self.habilitarCajas("disabled")
        self.habilitarBtnOper("normal")
        self.habilitarBtnGuardarCancelar("disabled")

        self.id = -1 # Sirve para el botón "Guardar", si guardamos un nuevo registro o guardamos una modificación

        self.grid.bind("<Button-1>", self.on_treeview_click)


    def habilitarCajas(self, estado): # Método que habilita / desabilita el uso de las cajas
        self.txtAlbum.configure(state = estado)
        self.txtArtista.configure(state = estado)
        self.txtAnio.configure(state = estado)
        self.txtGenero.configure(state = estado)
        self.txtValoracion.configure(state = estado)
        self.txtComentario.configure(state = estado)

    def limpiarCajas(self): # Método que vacía / limpia las cajas de lo que esté escrito
        self.txtAlbum.delete(0,END)
        self.txtArtista.delete(0,END)
        self.txtAnio.delete(0,END)
        self.txtGenero.delete(0,END)
        self.txtValoracion.delete(0,END)
        self.txtComentario.delete(0,END)

    def habilitarBtnOper(self, estado): # Método que habilita / desabilita el uso de los botones azules (de operaciones)
        self.btnNuevo.configure(state = estado)
        self.btnModificar.configure(state = estado)
        self.btnEliminar.configure(state = estado)

    def habilitarBtnGuardarCancelar(self, estado): # Método que habilita / desabilita el uso de los botones Guardar y Cancelar
        self.btnGuardar.configure(state = estado)
        self.btnCancelar.configure(state = estado)

    def llenarTabla(self):
        datos = self.albumes.consulta_albumes() # Es necesario el self ya que paises es una variable de la clase
        for row in datos:
            print(row)
            self.grid.insert("", END, text = row[0], values = (row[1], row[2], row[3], row[4], row[5], row[6]))

    def limpiarTabla(self): # Método que se encarga que por cada iteración, cada elemento de la tabla se elimina
        for item in self.grid.get_children():
            self.grid.delete(item)

    def controlCamposVacios(self): #Mejorar
        listaCampos = [self.txtAlbum.get(), self.txtArtista.get(), self.txtGenero.get(), self.txtAnio.get(), self.txtValoracion.get()] 

        for campo in listaCampos:
            if campo == "":
                return True
            return False

    def controlCampoNumero(self, numero):
        return numero.isdecimal()


    def fNuevo(self):

        selected = self.grid.focus() # Al tocar el botón "Modificar", se guarda el registro seleccionado (como diccionario) en una variable

        clave = self.grid.item(selected, "text") # del diccionario, me trae el #0 

        if clave != "": # Si se seleccionó  algo (traerá la clave del seleccionado)
            messagebox.showwarning("Nuevo", "Hay un proceso que debes terminar.")
        else:
            self.habilitarCajas("normal") #Al tocar el botón "Nuevo", se habilitan las cajas para que podamos ingresar datos
            self.habilitarBtnOper("disabled") #Se desabilitan los botones azules, para que el proceso de ingreso de datos solo termine con Guardar/Cancelar
            self.habilitarBtnGuardarCancelar("normal") #Se habilitan estos botones para finalizar el ingreso de los datos
            self.limpiarCajas() # Se limpian los registros de las cajas
            self.txtAlbum.focus() # Coloca el cursor en la primera caja

    def fGuardar(self):
        if self.id == -1: # Si es -1, es porque se inserta un nuevo registro

            if self.controlCamposVacios():
                messagebox.showwarning("Guardar", "Hay datos vacios.")

            else:
                r = messagebox.askquestion("Guardar", "¿Deseas guardar el registro en la base?\n")
                if r == messagebox.YES:
                    self.albumes.inserta_album(self.txtAlbum.get(), self.txtArtista.get(), self.txtAnio.get(), self.txtGenero.get(), self.txtValoracion.get(), self.txtComentario.get()) 
                    #Al tocar el botón "Guardar", se cargan en la query que carga el método inserta_album, los datos que están en las 4 cajas
                    messagebox.showinfo("Guardar", "Elemento guardado correctamente")
                else:
                    pass

        else: # Es porque se está modificando un registro

            if self.controlCamposVacios():
                messagebox.showwarning("Guardar", "Hay datos vacios.")

            else:
                r = messagebox.askquestion("Guardar", "¿Deseas guardar la modificación del registro?\n")
                if r == messagebox.YES:
                    self.albumes.modifica_album(self.id, self.txtAlbum.get(), self.txtArtista.get(), int(self.txtAnio.get()), self.txtGenero.get(), int(self.txtValoracion.get()), self.txtComentario.get()) #Se guarda la modificación. el parámeto es el id del registro seleccionado luego de tocar el botón "Modificar"
                    messagebox.showinfo("Guardar", "Elemento modificado correctamente")
                    self.id = -1 #Luego de guardar una modificación, la variable id vuelve a su estado original
                else:
                    pass

        self.limpiarTabla() #Se busca borrar la tabla desactualizada para cargarla nuevamente
        self.llenarTabla() #Se busca actualizar la tabla, una vez cargado el nuevo registro

        self.limpiarCajas()

        self.habilitarBtnGuardarCancelar("disabled") #Una vez cargado el registro, se desabilitan los botones Guardar y Cancelar. El proceso de ingreso de datos termina
        self.habilitarBtnOper("normal") #Se vuelven a habilitar los botones azules, para que pueda comenzar un nuevo proceso a partir del botón "Nuevo"

        self.habilitarCajas("disabled") #Se deshabilitan las cajas, obligando al usuario a comenzar una nueva operación, preferentemente con el botón "Nuevo"
    
    def fModificar(self):
        selected = self.grid.focus() # Al tocar el botón "Modificar", se guarda el registro seleccionado (como diccionario) en una variable

        clave = self.grid.item(selected, "text") # del diccionario, me trae el #0 

        if clave == "": # Si no se seleccionó nada (por eso no trae clave)
            messagebox.showwarning("Modificar", "Debes seleccionar un elemento.")
        
        else:
            self.id = clave # la variable de la Clase toma el valor de la clave del registro seleccionado
            self.habilitarCajas("normal")
            self.limpiarCajas() # Prepara las cajas

            valores = self.grid.item(selected, "values")

            # Se cargan las cajas con los valores del registro seleeccionado
            self.txtAlbum.insert(0, valores[0])
            self.txtArtista.insert(0, valores[1])
            self.txtAnio.insert(0, valores[2])
            self.txtGenero.insert(0, valores[3])
            self.txtValoracion.insert(0, valores[4])
            self.txtComentario.insert(0, valores[5])

            # Deshabilita los botones de operaciones. Habilita sólo para Guardar cambios
            self.habilitarBtnOper("disabled")
            self.habilitarBtnGuardarCancelar("normal")
            self.txtAlbum.focus()

    def fEliminar(self):
        selected = self.grid.focus() # Al tocar el botón "Eliminar", se guarda el registro seleccionado (como diccionario) en una variable
        #row = self.grid.item(selected)
        #print(row) #me trae un diccionario

        clave = self.grid.item(selected, "text") # del diccionario, me trae el #0 

        if clave == "": # Si no se seleccionó nada (por eso no trae clave)
            messagebox.showwarning("Eliminar", "Debes seleccionar un elemento.")
        else:
            valores = self.grid.item(selected, "values") # del dicionario, me trae una tupla con los valores de las columnas restantes
            data = str(clave) + ", " + valores[0] + ", " + valores[1] # Guardamos una cadena "ID, Album, Artista"
            r = messagebox.askquestion("Eliminar", "¿Deseas eliminar el registro seleccionado?\n" + data)

            if r == messagebox.YES:
                n = self.albumes.elimina_album(clave) # El valor es 1 (si se eliminó) o 0 (si no). Se detalla en el método elimina_pais
                if n == 1: 
                    messagebox.showinfo("Eliminar", "El registro se eliminó satisfactoriamente.")
                    self.limpiarTabla()
                    self.llenarTabla()
                else:
                    messagebox.showwarning("Eliminar", "No fue posible elimiar el registro.")
            else:
                pass

    def fCancelar(self):
        r = messagebox.askquestion("Cancelar", "¿Deseas cancelar la operación actual?")
        if r == messagebox.YES:

            #Se vuelve al estado genérico y a la espera de una operación
            self.limpiarCajas()
            self.habilitarBtnGuardarCancelar("disabled")
            self.habilitarBtnOper("normal")
            self.habilitarCajas("disabled")

            self.on_treeview_click()
            self.id = -1

    def on_treeview_click(self, event = None):
        item = self.grid.selection()

        if item:  # Si se ha seleccionado un elemento
            # Desseleccionar el elemento haciendo clic en un área vacía
            self.grid.selection_remove(item)
            self.grid.focus('')
    #------------------------------------------------------------

    def create_widgets(self):

        frame1 = Frame(self, bg = "#303030") #NO es miembro de la clase. 1° Frame hijo de Ventana
        frame1.place(x = 3, y = 3, width = 92, height = 350) # Uso de place para ubicar este frame

        self.btnNuevo = Button(frame1, text = "Nuevo", command = self.fNuevo, bg = "#1DB954", fg = "white") #Variable miembro, tiene self porque lo necesitamos llamar por fuera de este método. Otras funciones necesitan alcanzar este boton
        self.btnNuevo.place(x = 6, y = 100, width = 80, height = 30) # ubicamos el boton en el frame 1

        self.btnModificar = Button(frame1, text = "Modificar", command = self.fModificar, bg = "#1DB954", fg = "white")
        self.btnModificar.place(x = 6, y = 160, width = 80, height = 30)

        self.btnEliminar = Button(frame1, text = "Eliminar", command = self.fEliminar, bg = "#1DB954", fg = "white")
        self.btnEliminar.place(x = 6, y = 220, width = 80, height = 30)

        #--------------------------------------------------------------

        frame2 = Frame(self, bg = "#303030") #NO es miembro de la clase. 2° Frame hijo de Ventana
        frame2.place(x = 98, y = 3, width = 150, height = 350)

        #Par Etiqueta - Caja Album
        lbl1 = Label(frame2, text = "Album: ", bg = "#303030", fg = "white") #No es miembro de la clase, no es necesario
        lbl1.place(x = 10, y = 5)
        self.txtAlbum = Entry(frame2) #Es miembro de la clase, para luego utilizar los valores ingresados
        self.txtAlbum.place(x = 10, y = 25, width = 100, height = 20)

        #Par Etiqueta - Caja Artista
        lbl2 = Label(frame2, text = "Artista: ",  bg = "#303030", fg = "white")
        lbl2.place(x = 10, y = 55)
        self.txtArtista = Entry(frame2)
        self.txtArtista.place(x = 10, y = 75, width = 100, height = 20)

        #Par Etiqueta - Caja Año
        lbl3 = Label(frame2, text = "Año: ",  bg = "#303030", fg = "white")
        lbl3.place(x = 10, y = 105)
        self.txtAnio = Entry(frame2, validate="key", validatecommand=(self.register(self.controlCampoNumero), "%S"))
        self.txtAnio.place(x = 10, y = 125, width = 50, height = 20)

        #Par Etiqueta - Caja Genero
        lbl4 = Label(frame2, text = "Género: ",  bg = "#303030", fg = "white")
        lbl4.place(x = 10, y = 155)
        self.txtGenero = Entry(frame2)
        self.txtGenero.place(x = 10, y = 175, width = 100, height = 20)

        #Par Etiqueta - Caja Valoración
        lbl4 = Label(frame2, text = "Valoración: ",  bg = "#303030", fg = "white")
        lbl4.place(x = 10, y = 205)
        self.txtValoracion = Entry(frame2, validate="key", validatecommand=(self.register(self.controlCampoNumero), "%S"))
        self.txtValoracion.place(x = 10, y = 225, width = 50, height = 20)

        #Par Etiqueta - Caja Comentario
        lbl4 = Label(frame2, text = "Comentario: ",  bg = "#303030", fg = "white")
        lbl4.place(x = 10, y = 255)
        self.txtComentario = Entry(frame2)
        self.txtComentario.place(x = 10, y = 275, width = 100, height = 20)

        
        #Botones
        self.btnGuardar = Button(frame2, text = "Guardar", command = self.fGuardar, bg = "#1DB954", fg = "#ffffff")
        self.btnGuardar.place(x = 10, y = 310, width = 60, height = 30)

        self.btnCancelar = Button(frame2, text = "Cancelar", command = self.fCancelar, bg = "red", fg = "#ffffff")
        self.btnCancelar.place(x = 80, y = 310, width = 60, height = 30)

        #--------------------------------------------------------------

        frame3 = Frame(self, bg = "#303030") #NO es miembro de la clase. 3° Frame hijo de Ventana. Contendrá al Grid
        frame3.place(x = 251, y = 3, width = 599, height = 350)

        #Agregar estilo y configurar el tema
        style = ttk.Style()
        style.theme_use("clam")

        #Configurar los colores del Treeview
        style.configure("Treeview",
            background = "#303030",
            foreground = "#ffffff",
            rowheight = 25,
            fieldbackground = "#303030")
        
        #Cambiar el color de la selección
        style.map("Treeview",
            background = [("selected", "#1DB954")])

        self.grid = ttk.Treeview(frame3, columns = ("col1", "col2", "col3", "col4", "col5", "col6")) # Objeto bautizado como "grid", un Treeview. Es miembro de la clase. Es hijo de Ventana. Contiene 7 columnas (#0 como ID)

        #Creación de las columnas
        self.grid.column("#0", width = 60) # total anchura de la suma de columnas (407px, 13px menos para arreglar discrepancia con el margen y con el scrollbar)
        self.grid.column("col1", width = 70, anchor = CENTER)
        self.grid.column("col2", width = 90, anchor = CENTER)
        self.grid.column("col3", width = 90, anchor = CENTER)
        self.grid.column("col4", width = 90, anchor = CENTER)
        self.grid.column("col5", width = 90, anchor = CENTER)
        self.grid.column("col6", width = 90, anchor = CENTER)

        #Creación de los encabezados
        self.grid.heading("#0", text = "ID", anchor = CENTER)
        self.grid.heading("col1", text = "Album", anchor = CENTER)
        self.grid.heading("col2", text = "Artista", anchor = CENTER)
        self.grid.heading("col3", text = "Año", anchor = CENTER)
        self.grid.heading("col4", text = "Género", anchor = CENTER)
        self.grid.heading("col5", text = "Valoración", anchor = CENTER)
        self.grid.heading("col6", text = "Comentario", anchor = CENTER)

        #Ubicación del Treeview en la Ventana y modo de selección de registros
        self.grid.pack(side = LEFT, fill = Y)
        self.grid["selectmode"] = "browse"
        
        #Scrollbar del Grid
        sb = Scrollbar(frame3, orient = VERTICAL)
        sb.pack(side = RIGHT, fill = Y)
        self.grid.config(yscrollcommand = sb.set)
        sb.config(command = self.grid.yview)

        #Ejemplos de registros
        """self.grid.insert("", END, text = 1, values = ("ARG", "Argentina", "Buenos Aires", "ARS"))
        self.grid.insert("", END, text = 2, values = ("USA", "United States", "Washington", "USD"))"""

        #--------------------------------------------------------------
        frame4 = Frame(self, bg = "#303030") #NO es miembro de la clase. 4° Frame hijo de Ventana. Contendrá al Grid
        frame4.place(x = 853, y = 3, width = 100, height = 350)

        imagen = Image.open("clef.png")

        self.imagen_tk = ImageTk.PhotoImage(imagen)
        self.propaganda = Label(frame4, image=self.imagen_tk)
        self.propaganda.pack()