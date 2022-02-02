from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion=baseDatos[MONGO_COLECCION]
ID_ESTUDIANTE=" "

def mostrarDatos():
    try:
        registros=tabla.get_children()
        for registro in registros:
            tabla.delete(registro)
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"],values=documento["nombre"])
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo excedido")
    except pymongo.errors.ConnectionFailure as errorConexion:
        print("Fallo la conexión con Mongodb")

def crearRegistro():
    if len(nombre.get())!=0  and len(calificacion.get())!=0 and len(genero.get())!=0:
        try:
            documento={"nombre":nombre.get(),"calificacion":calificacion.get(),"genero":genero.get()}
            coleccion.insert(documento)
            nombre.delete(0,END)
            calificacion.delete(0,END)
            genero.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()
def dobleClickTabla(event):
    global ID_ESTUDIANTE
    ID_ESTUDIANTE=str(tabla.item(tabla.selection())["text"])
    #print(ID_ESTUDIANTE)
    documento=coleccion.find({"_id":ObjectId(ID_ESTUDIANTE)})[0]
    #print(documento)
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    calificacion.delete(0,END)
    calificacion.insert(0,documento["calificacion"])
    genero.delete(0,END)
    genero.insert(0,documento["genero"])
    insertar["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"
def editarRegistro():
    global ID_ESTUDIANTE
    if len(nombre.get())!=0 and len(calificacion.get())!=0 and len(genero.get())!=0 :
        try:
            idBuscar={"_id":ObjectId(ID_ESTUDIANTE)}
            nuevosValores={"nombre":nombre.get(),"calificacion":calificacion.get(),"genero":genero.get()}
            coleccion.update(idBuscar,nuevosValores)
            nombre.delete(0,END)
            calificacion.delete(0,END)
            genero.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    insertar["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
def borrarRegistro():
    global ID_ESTUDIANTE 
    try:
        idBuscar={"_id":ObjectId(ID_ESTUDIANTE)}
        coleccion.delete_one(idBuscar)
        nombre.delete(0,END)
        calificacion.delete(0,END)
        genero.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
        print(error)
    insertar["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
    mostrarDatos()
ventana=Tk()
tabla=ttk.Treeview(ventana,columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="NOMBRE")
tabla.bind("<Double-Button-1>",dobleClickTabla)
#Nombre
Label(ventana,text="Nombre").grid(row=2,column=0)
nombre=Entry(ventana)
nombre.grid(row=2,column=1)
#Calificación
Label(ventana,text="Calificación").grid(row=4,column=0)
calificacion=Entry(ventana)
calificacion.grid(row=4,column=1)
#Genero
Label(ventana,text="Genero").grid(row=3,column=0)
genero=Entry(ventana)
genero.grid(row=3,column=1)
#Botón insertar
insertar=Button(ventana,text="Insertar estudiante", command=crearRegistro,bg="CadetBlue",fg="white")
insertar.grid(row=5,columnspan=2)
#Botón Editar
editar=Button(ventana,text="Editar estudiante",command=editarRegistro,bg="magenta4")
editar.grid(row=6,columnspan=2)
editar["state"]="disabled"
#Botón Borrar
borrar=Button(ventana,text="Borrar estudiante",command=borrarRegistro,bg="OrangeRed3")
borrar.grid(row=7,columnspan=2)
borrar["state"]="disabled"

mostrarDatos()
ventana.mainloop()
