'''ESTE CRUD ESTÁ INTEGRADO TODO EN ESTE ARCHIVO, FUNCIONA CON TK INTER Y MY SQL
SOLAMENTE TIENE UNA TABLA, CON ID, NOMBRE, CARGO Y SALARIO'''
#IMPORTAR LIBRERÍAS

import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#DESARROLLO DE LA INTERFAZ GRÁFICA (VENTANA)

root = Tk()
root.title("APLICACIÓN CRUD CON BASE DE DATOS.")
root.geometry("780x460")
root.config(bg = '#555555')

miId = StringVar()
miNombre = StringVar()
miCargo = StringVar()
miSalario = StringVar()

def conexionBBDD():
    miConexion = mysql.connector.connect(user='root',
                                         password='153125D.SSSm',
                                         host='localhost',
                                         database='',
                                         port='3306')
    miCursor = miConexion.cursor()
    print(miConexion)
    try:
        miCursor.execute('''CREATE DATABASE crud;
        USE crud;
        CREATE TABLE empleado(
        ID BIGINT PRIMARY KEY AUTO_INCREMENT, 
        NOMBRE VARCHAR(50) NOT NULL,
        CARGO VARCHAR(50) NOT NULL,
        SALARIO INT NOT NULL); 
        ''')
        messagebox.showinfo("CONEXION", "Tabla creada exitosamente.")
    except:
        messagebox.showinfo("CONEXION", "Conexion exitosa con la base de datos")

def eliminarBBDD():
    miConexion = mysql.connector.connect(user='root',
                                         password='153125D.SSSm',
                                         host='localhost',
                                         database='crud',
                                         port='3306')
    miCursor = miConexion.cursor()
    if messagebox.askyesno(message = "¿Los datos se perderán definitivamente, Desea continuar?", tittle = 'ADVERTENCIA!'): #VENTANA QUE PREGUNTA SI QUEREMOS TOMAR UNA DESICIÓN
        miCursor.execute("DROP TABLE empleado")
    else:
        pass

    limpiarCampos()
    mostrar()

def salirAplicacion():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la aplicación?")
    if valor == "yes":
        root.destroy()

def limpiarCampos():
    miId.set("")
    miNombre.set("")
    miCargo.set("")
    miSalario.set("")

def mensaje():
    acerca = '''
    Aplicacion CRUD
    Version 1.0
    Tecnologia Python Tkinter
    DANIEL BUSTAMANTE ORTEGA.
    '''
    messagebox.showinfo(title = "INFORMACIÓN", message = acerca)

#METODOS PARA REALIZAR EL CRUD.

def crear():
    miConexion = mysql.connector.connect(user='root',
                                    password='153125D.SSSm',
                                    host='localhost',
                                    database='crud',
                                    port='3306')
    miCursor = miConexion.cursor()
    try:
        datos = miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("INSERT INTO empleado VALUES(NULL,%s,%s,%s)", (datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al crear el registro, verifique conexión con base de datos")
        pass
    limpiarCampos()
    mostrar()
        
def mostrar():
    miConexion = mysql.connector.connect(user='root',
                                    password='153125D.SSSm',
                                    host='localhost',
                                    database='crud',
                                    port='3306')
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)

    try:
        miCursor.execute("SELECT * FROM empleado")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3]))

    except:
        pass

#TABLA
tree = ttk.Treeview(height=10, columns=('#0','#1','#2'))          #ESTA FUNCIÓN ES COMO UN ÁRBOL DE VISTAS QUE FUNCIONA COMO TABLA
tree.place(x=2,y=130)                                             #TAMAÑO DE LAS COLUMNAS
tree.column('#0',width=80)                                        #CABEZERAS
tree.heading('#0', text="ID", anchor = CENTER)                    #ENCABEZADO DE ID
tree.heading('#1', text="NOMBRE DEL EMPLEADO", anchor = CENTER)
tree.column('#1',width=318) 
tree.heading('#2', text="CARGO", anchor = CENTER)
tree.column('#2',width=240) 
tree.column('#3', width = 136)                                    #SE MODIFICA TAMAÑO DE COLUMNA 3
tree.heading('#3', text="SALARIO",anchor = CENTER)                #ENCABEZADO DE ID


def seleccionarUsandoClick(event):                                #SELECCIONAR COLUMNA AL PASAR O DAR CLICK.
    item = tree.identify('item', event.x,event.y)
    miId.set(tree.item(item,'text'))
    miNombre.set(tree.item(item, "values")[0])
    miCargo.set(tree.item(item, "values")[1])
    miSalario.set(tree.item(item, "values")[2])

tree.bind("<Double-1>", seleccionarUsandoClick)


def actualizar():
    miConexion = mysql.connector.connect(user='root',
                                    password='153125D.SSSm',
                                    host='localhost',
                                    database='crud',
                                    port='3306')
    miCursor = miConexion.cursor()
    try:
        datos = miNombre.get(),miCargo.get(),miSalario.get()
        miCursor.execute("UPDATE empleado SET NOMBRE = %s, CARGO = %s, SALARIO = %s WHERE ID =" +miId.get(), (datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al actualizar el registro.")
        pass
    limpiarCampos()
    mostrar()
        

def borrar():
    miConexion = mysql.connector.connect(user='root',
                                    password='153125D.SSSm',
                                    host='localhost',
                                    database='crud',
                                    port='3306')
    miCursor = miConexion.cursor()
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            miCursor.execute("DELETE FROM empleado WHERE ID =" +miId.get())
            miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro.")
        pass
    limpiarCampos()
    mostrar()
        

#COLOCAR WIDGETS EN LA VISTA

#CREAR LOS MENUS
menubar=Menu(root)                            #MENÚ BAR
menubasedat=Menu(menubar,tearoff=0)           #ESTRUCTURA DE LOS MENUS

menubasedat.add_command(label='Crear / Conectar base de datos', command=conexionBBDD)
menubasedat.add_command(label='Eliminar base de datos', command=eliminarBBDD)
menubasedat.add_command(label='Salir', command=salirAplicacion)
menubar.add_cascade(label='Inicio', menu=menubasedat)

ayudamenu=Menu(menubar, tearoff=0)
ayudamenu.add_command(label='Resetear Campos', command=limpiarCampos)
ayudamenu.add_command(label='Acerca', command=mensaje)
menubar.add_cascade(label='Ayuda',menu=ayudamenu)

#CREAR ETIQUETAS Y CAJAS DE TEXTO

e1 = Entry(root, textvariable = miId)

l2 = Label(root, bg = '#8CB8C6', text = "NOMBRE ")
l2.place(x = 77, y = 10)
e2 = Entry(root, bg = '#FFDAB9', textvariable = miNombre, width = 80)
e2.place(x = 137, y = 10)

l3 = Label(root, bg = '#8CB8C6', text = "  CARGO  ")
l3.place(x = 77, y = 40)
e3 = Entry(root, bg = '#FFDAB9', textvariable = miCargo, width = 38)
e3.place(x = 137, y = 40)

l4 = Label(root, bg = '#8CB8C6', text = "SALARIO")
l4.place(x = 387, y = 40)
e4 = Entry(root, bg = '#FFDAB9', textvariable = miSalario, width = 23)
e4.place(x = 442, y = 40)

l5 = Label(root, bg = '#90EE90', text = " USD ")
l5.place(x = 587, y = 40)

#CREAR BOTONES

b1 = Button(root, text = "Crear registro", bg = '#8CB8C6', command = crear)
b1.place(x = 63, y = 90)

b2 = Button(root, text = "Modificar registro", bg = '#8CB8C6', command = actualizar)
b2.place(x = 240, y = 90)

b3 = Button(root, text = "Mostrar lista", bg = '#8CB8C6', command = mostrar)
b3.place(x = 450, y = 90)

b4 = Button(root, text = "Eliminar registro", bg = "#FF69B4", command = borrar)
b4.place(x = 620, y = 90)



root.config(menu=menubar)

root.mainloop()
        


            


