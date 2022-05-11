import datetime
import pymongo
import tkinter as tk
from tkinter import *


def busquedas(tipo, datos=''):
    try:
        # Conexion a base de datos
        cliente = pymongo.MongoClient("mongodb://localhost:27017")
        db = cliente['BaseDatosPeliculas']
        cole = db['Peliculas']

        if tipo == 'todo':
            resultado = list(cole.find())
            return resultado
        if tipo == 'director':
            agregado = cole.aggregate(
                [{
                    "$group":
                    {"_id": "$Director",
                     "peliculas": {"$sum": 1}
                     },
                },
                    {
                    "$sort": {"peliculas": -1}
                }
                ])
            return agregado
        if tipo == 'estreno':
            agregado = cole.aggregate([
                {
                    "$group": {
                        "_id": {"$year": "$Estreno"},
                        "peliculas": {"$sum": 1},
                    }
                },
                {
                    "$sort": {"peliculas": -1}
                }
            ])
            return agregado

    except Exception:
        print("Se produjo un error en busqueda")
    finally:
        print("Uso correcto de busquedas")


def cambios(tipo, datos, valid=""):
    # Conexion a base de datos
    cliente = pymongo.MongoClient("mongodb://localhost:27017")
    db = cliente['BaseDatosPeliculas']
    cole = db['Peliculas']

    if (tipo == 'nuevo'):
        cole.insert_one(datos)
    if (tipo == 'eliminar'):
        cole.delete_many({'Id': valid})
    if(tipo == 'actu'):
        cole.update_many({'Id': valid}, {'$set': datos})

    print("Uso correcto de modificar")


def main():
    for elemento in root.winfo_children():
        elemento.destroy()

    titulo = tk.Label(text="Menu principal")
    titulo.grid(column=0, row=1)

    botoncrear = tk.Button(text="Crear", command=lambda: menucrear())
    botonleer = tk.Button(text="Leer", command=lambda: menuleer())
    botoncambiar = tk.Button(text="Cambiar", command=lambda: menueditar())
    botoneliminar = tk.Button(text="Eliminar", command=lambda: menuborrar())
    botoncrear.grid(column=0, row=2)
    botonleer.grid(column=0, row=3)
    botoncambiar.grid(column=0, row=4)
    botoneliminar.grid(column=0, row=5)


def menucrear():
    for elemento in root.winfo_children():
        elemento.destroy()

    botonatras = tk.Button(text="atras", command=lambda: main())
    botonatras.grid(column=0, row=0)
    titulo = tk.Label(text="Pelicula nueva ingresar datos")
    textoid = tk.Label(text="id")
    textotitulo = tk.Label(text="Titulo")
    textopersonaje = tk.Label(text="Personaje")
    textoestreno = tk.Label(text="Estreno")
    textodirector = tk.Label(text="Director")
    entradaid = tk.Entry()
    entradatitulo = tk.Entry()
    entradapersonaje = tk.Entry()
    entradaestreno = tk.Entry()
    titulo.grid(column=0, row=1)
    textotitulo.grid(column=0, row=4)
    textoid.grid(column=0, row=2)
    textopersonaje.grid(column=0, row=6)
    textoestreno.grid(column=0, row=8)
    textodirector.grid(column=0, row=10)
    entradaid.grid(column=0, row=3)
    entradatitulo.grid(column=0, row=5)
    entradapersonaje.grid(column=0, row=7)
    entradaestreno.grid(column=0, row=9)
    entradadirector = tk.Entry()
    entradadirector.grid(column=0, row=11)

    btn_crear = tk.Button(text="Create", command=lambda: nuevaPelicula())
    btn_crear.grid(column=0, row=12, columnspan=2)

    def nuevaPelicula():
        f = datetime.datetime.strptime(
            entradaestreno.get(), "%Y-%m-%d")
        newDocument = {"Id": int(entradaid.get()), "Titulo": entradatitulo.get(
        ), "Personaje": entradapersonaje.get(), "Estreno": f, "Director": entradadirector.get()}

        cambios("nuevo", newDocument)


def menuleer():
    for elemento in root.winfo_children():
        elemento.destroy()

    botonatras = tk.Button(text="atras", command=lambda: main())
    botonatras.grid(column=0, row=0)
    titulo = tk.Label(text="Modos de lectura")
    titulo.grid(column=1, row=1)
    botoncompleto = tk.Button(text="Vista completa",
                              command=lambda: vistacompleta())
    botonanual = tk.Button(text="Peliculas por año", command=lambda: anual())
    botondirector = tk.Button(
        text="Peliculas por director", command=lambda: pordirector())
    botoncompleto.grid(column=0, row=2)
    botondirector.grid(column=1, row=2)
    botonanual.grid(column=2, row=2)

    def vistacompleta():
        root = Tk()
        listbox = Listbox(root, width=70, height=50)

        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        respuesta = busquedas("todo")
        for values in respuesta:
            listbox.insert(END, values)

        scrollbar.config(command=listbox.yview)
        root.mainloop()

    def pordirector():
        root = Tk()
        listbox = Listbox(root, width=25, height=20)

        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        respuesta = busquedas("director")
        for values in respuesta:
            listbox.insert(END, values)

        scrollbar.config(command=listbox.yview)
        root.mainloop()

    def anual():
        root = Tk()
        listbox = Listbox(root, width=15, height=20)

        listbox.pack(side=LEFT, fill=BOTH)
        scrollbar = Scrollbar(root)
        scrollbar.pack(side=RIGHT, fill=BOTH)
        respuesta = busquedas("estreno")
        for values in respuesta:
            listbox.insert(END, values)

        scrollbar.config(command=listbox.yview)
        root.mainloop()


def menueditar():
    for elemento in root.winfo_children():
        elemento.destroy()

    botonatras = tk.Button(text="atras",
                           command=lambda: main())
    botonatras.grid(column=0, row=0)
    titulo = tk.Label(text="Cambiar datos de una pelicula")
    titulo.grid(column=0, row=1)
    textoid = tk.Label(text="Id")
    textoid.grid(column=0, row=2)
    entradaid = tk.Entry()
    entradaid.grid(column=1, row=2)
    titulo = tk.Label(text="Titulo")
    titulo.grid(column=0, row=3)
    entradatitulo = tk.Entry()
    entradatitulo.grid(column=1, row=3)
    textopersonaje = tk.Label(text="Personaje")
    textopersonaje.grid(column=0, row=4)
    entradapersonaje = tk.Entry()
    entradapersonaje.grid(column=1, row=4)
    textoestreno = tk.Label(text="Estreno")
    textoestreno.grid(column=0, row=5)
    entradaestreno = tk.Entry()
    entradaestreno.grid(column=1, row=5)
    textodirector = tk.Label(text="Director")
    textodirector.grid(column=0, row=6)
    entradadirector = tk.Entry()
    entradadirector.grid(column=1, row=6)

    botoncambiar = tk.Button(
        text="Cambiar", command=lambda: ejecutarActu())
    botoncambiar.grid(column=0, row=7)

    def ejecutarActu():
        id = int(entradaid.get())
        fecha = datetime.datetime.strptime(entradaestreno.get(), "%Y-%m-%d")
        data = {'Id': id, 'Titulo': entradatitulo.get(), 'Personaje': entradapersonaje.get(),
                'Estreno': fecha, 'Director': entradadirector.get()}
        cambios("actu", data, id)


def menuborrar():
    for elemento in root.winfo_children():
        elemento.destroy()

    botonatras = tk.Button(text="atras", command=lambda: main())
    botonatras.grid(column=0, row=0)
    titulo = tk.Label(text="Delete Movie")
    titulo.grid(column=0, row=1)

    textoid = tk.Label(text="Id")
    textoid.grid(column=0, row=2)
    entradaid = tk.Entry()
    entradaid.grid(column=0, row=3)

    botonborrar = tk.Button(text="Borrar", command=lambda: cambios(
        "eliminar", "", int(entradaid.get())))
    botonborrar.grid(column=0, row=4)


if __name__ == '__main__':
    root = tk.Tk(className='Programa')
    main()
    root.mainloop()
