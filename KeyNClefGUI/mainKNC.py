from tkinter import *
from ventanaKNC import Ventana
from tkinter import messagebox

def menu(root, ventana):

    def salirAplicacion():
        valor = messagebox.askquestion("Salir", "Deseas salir de la aplicación?")

        if valor == "yes":
            root.destroy()

    barraMenu = Menu(root)
    root.config(menu = barraMenu)

    bbddMenu = Menu(barraMenu, tearoff=0)
    bbddMenu.add_command(label="Salir", command = salirAplicacion)

    borrarMenu = Menu(barraMenu, tearoff = 0)
    borrarMenu.add_command(label="Borrar campos", command = ventana.limpiarCajas)

    crudMenu = Menu(barraMenu, tearoff = 0)
    crudMenu.add_command(label="Nuevo", command = ventana.fNuevo)
    crudMenu.add_command(label="Modificar", command = ventana.fModificar)
    crudMenu.add_command(label="Eliminar", command = ventana.fEliminar)

    ayudaMenu = Menu(barraMenu, tearoff = 0)
    ayudaMenu.add_command(label = "Licencia")
    ayudaMenu.add_command(label = "Acerca de")

    barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
    barraMenu.add_cascade(label="Borrar", menu=borrarMenu)
    barraMenu.add_cascade(label="CRUD", menu=crudMenu)
    barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


def main():
    root = Tk()
    root.wm_title("Key and Clef")
    root.iconbitmap("favicon.ico")
    app = Ventana(root) #Instanciamos un objeto de la clase Ventana. Raíz del GUI como parámetro
    menu(root, app)
    app.mainloop()


if __name__ == "__main__": #Punto de inicio del programa
    main()