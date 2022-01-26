import tkinter as tk
from tkinter import ttk
import sqlite3 as SQ3
from tkinter import messagebox
from Paquetes.Funciones import agregar_comilla, validar_fecha


root = tk.Tk()
root.eval('tk::PlaceWindow . center')           #Centrar en pantalla
root.title("Compensados")
root.iconbitmap("E:\Proyectos\Proyecto_Compensados\Calendario.ico")
root.resizable(0,0)


frame = tk.Frame(root)
frame.pack()

feriado = tk.StringVar()
fecha = tk.StringVar()
estado = tk.StringVar()

conexion = None
cursor = None
contador = 0

#------------------------------------------------------------------------------------------------

def cuandoEscriba(event):
    fechaa = entry_fecha
    if event.char.isdigit():
        texto = fechaa.get()
        letras = 0
        for i in texto:
            letras +=1

        if letras == 2:
            fechaa.insert(2,"/")
        elif letras == 5:
            fechaa.insert(5,"/")
        elif letras == 10:
            fechaa.delete(9,"end")
    else:
        return "break"

def cuandoEscriba2(event):
    fechaa = entry_feriado
    if event.char.isdigit():
        texto = fechaa.get()
        letras = 0
        for i in texto:
            letras +=1

        if letras == 2:
            fechaa.insert(2,"/")
        elif letras == 5:
            fechaa.insert(5,"/")
        elif letras == 10:
            fechaa.delete(9,"end")
    else:
        return "break"


#-------------------------------------- Funciones -----------------------------------------------




def conectar():
    global conexion, cursor, contador
    try:
        conexion = SQ3.connect("E:\Python\Scripts-Pool\zBases_Datos\Compensados.db")
        cursor = conexion.cursor()

        cursor.execute("""
            create table COMPENSADOS(
                Feriado_Asistido varchar(50) unique,
                Fecha_Compensado varchar(50),
                Estado varchar(50)
            )""")
        conexion.commit()
        messagebox.showinfo("Compensados","Se ha creado la base de datos")
    except:
        if contador == 0:
            messagebox.showinfo("Compensados","Se ha conectado a la base de datos")
            contador +=1
        else :
            messagebox.showwarning("Aviso","Ya estás conectado a la base de datos")    

def salir():
    global conexion, contador
    valor = messagebox.askyesno("Salir","¿Estás seguro de cerrar el programa?")
    if valor is True:
        root.destroy()
        contador=0
        if conexion != None:
            conexion.close()

def limpiar_campos():
    feriado.set("")
    fecha.set("")
    estado.set("")

def agregar():
    global conexion, cursor, fecha
    valor_feriado = validar_fecha(feriado)
    valor_fecha = validar_fecha(fecha)

    try:
        try:
            if feriado.get() != "" and fecha.get() != "" and estado.get() != "":
                if valor_fecha == True and valor_feriado == True:
                    lista_compensados = [feriado.get(),fecha.get(),estado.get()]
                    cursor.execute("insert into COMPENSADOS values(?,?,?)", lista_compensados)
                    messagebox.showinfo("Compensados","Registro agregado con éxito!")
                    conexion.commit()
                else :
                    messagebox.showerror("Error","Ingresa una fecha válida")
            else:
                messagebox.showerror("Error","Por favor llena todos los campos correctamente")
        except SQ3.IntegrityError:
                messagebox.showerror("Error","Ya se ha ingresado el feriado "+feriado.get())
    except:
        messagebox.showerror("Error","Necesitas conectar la base de datos primero")
        

def mostrar():
    global conexion, cursor

    try:
        #Es necesario agregar las comillas simples porque el select en sql lo solicita cuando hablamos de un varchar. Si fuera un integer no sería necesario.
        dato = agregar_comilla(feriado)
        cursor.execute("select * from COMPENSADOS where Feriado_Asistido =" + dato)
        lista = cursor.fetchall()
        for datos in lista:
            fecha.set(datos[1])
            estado.set(datos[2])
        conexion.commit()
    except:
        messagebox.showerror("Error","Necesitas conectar la base de datos primero")

def cambiar():
    global conexion, cursor

    try:
        valor_feriado = validar_fecha(feriado)
        valor_fecha = validar_fecha(fecha)

        if feriado.get() != "" and fecha.get() != "" and estado != "":
            if valor_feriado is True and valor_fecha is True:
                lista = [fecha.get(),estado.get()]
                dato = agregar_comilla(feriado)
                cursor.execute("update COMPENSADOS set Fecha_Compensado =?, Estado =? where Feriado_Asistido ="+dato, lista)
                conexion.commit()
                messagebox.showinfo("Compensados","Registro modificado con éxito!")
            else :
                messagebox.showerror("Error","Ingresa una fecha válida con formato dd/mm/yyyy")
        else :
            messagebox.showerror("Error","Por favor llena todos los campos correctamente")
    except AttributeError:
        messagebox.showerror("Error","Necesitas conectar la base de datos primero")

def mostrar_libres():
    global conexion,cursor, Objetos_fechas

    try :
        cursor.execute("select * from COMPENSADOS where Estado = 'Libre'")
        lista = cursor.fetchall()
        row = 2

        root = tk.Tk()
        root.eval('tk::PlaceWindow . center')
        root.title("Días por compensar")
        root.iconbitmap("E:\Proyectos\Proyecto_Compensados\Calendario.ico")
        root.resizable(0,0)

        frame_libres = tk.Frame(root)
        frame_libres.pack()

        tk.Label(frame_libres,text ="Feriado Asistido", fg = "Black", font=("Arial",13)).grid(row=1,column=1, padx=15,pady=15)
        tk.Label(frame_libres,text ="Fecha Compensado", fg = "Black", font=("Arial",13)).grid(row=1,column=2, padx=15,pady=15)
        tk.Label(frame_libres,text ="Estado", fg = "Black", font=("Arial",13)).grid(row=1,column=3, padx=15,pady=15)

        for libres in lista:
            tk.Label(frame_libres,text =libres[0], fg = "#0D9E06", font=("Arial",10)).grid(row=row,column=1, padx=15,pady=15)
            tk.Label(frame_libres,text =libres[1], fg = "#0D9E06", font=("Arial",10)).grid(row=row,column=2, padx=15,pady=15)
            tk.Label(frame_libres,text =libres[2], fg = "#0D9E06", font=("Arial",10)).grid(row=row,column=3, padx=15,pady=15)
            row +=1
    except AttributeError:
        messagebox.showerror("Error","Necesitas conectar la base de datos primero")

def mostrar_todo():
    global conexion,cursor

    try :
        cursor.execute("select * from COMPENSADOS")
        lista = cursor.fetchall()
        row = 2

        root = tk.Tk()
        root.title("Días por compensar")
        root.iconbitmap("E:\Proyectos\Proyecto_Compensados\Calendario.ico")
        root.eval('tk::PlaceWindow . center')
        root.resizable(0,0)

        frame_libres = tk.Frame(root)
        frame_libres.pack()

        tk.Label(frame_libres,text ="Feriado Asistido", fg = "Black", font=("Arial",13)).grid(row=1,column=1, padx=15,pady=15)
        tk.Label(frame_libres,text ="Fecha Compensado", fg = "Black", font=("Arial",13)).grid(row=1,column=2, padx=15,pady=15)
        tk.Label(frame_libres,text ="Estado", fg = "Black", font=("Arial",13)).grid(row=1,column=3, padx=15,pady=15)
        for libres in lista:
            if libres[2] == "Libre" : 
                color = "#0D9E06"
            elif libres[2] == "En espera":
                color = "#89343f"
            else :
                color = "#05093D"
            tk.Label(frame_libres,text =libres[0], fg = color, font=("Arial",10)).grid(row=row,column=1, padx=15,pady=15)
            tk.Label(frame_libres,text =libres[1], fg = color, font=("Arial",10)).grid(row=row,column=2, padx=15,pady=15)
            tk.Label(frame_libres,text =libres[2], fg = color, font=("Arial",10)).grid(row=row,column=3, padx=15,pady=15)
            row +=1
    except AttributeError:
        messagebox.showerror("Error","Necesitas conectar la base de datos primero")

def mostrar_ayuda():
    root_ayuda = tk.Tk()
    root_ayuda.eval('tk::PlaceWindow . center')
    root_ayuda.title("Ayuda")
    root_ayuda.iconbitmap("E:\Proyectos\Proyecto_Compensados\Calendario.ico")
    root_ayuda.resizable(0,0)

    frame_ayuda = tk.Frame(root_ayuda)
    frame_ayuda.pack()

    #tk.Label(frame_ayuda, text="Estados válidos", font=("Arial",10)).grid(row=1,column=1, pady=10,padx=10)
    tk.Label(frame_ayuda,text="Formato válido para fecha", font=("Arial",10)).grid(row=1, column=1, pady=20,padx=30, columnspan=2)
    #tk.Label(frame_ayuda, text="Compensado",fg="Green", font=("Arial",10)).grid(row=2,column=1, pady=10,padx=10, sticky="w")
    #tk.Label(frame_ayuda, text="Libre",fg="Green", font=("Arial",10)).grid(row=3,column=1, pady=10,padx=10, sticky="w")
    #tk.Label(frame_ayuda, text="En espera",fg="Green", font=("Arial",10)).grid(row=4,column=1, pady=10,padx=10, sticky="w")
    #tk.Label(frame_ayuda, text="Aprobado",fg="Green", font=("Arial",10)).grid(row=5,column=1, pady=10,padx=10, sticky="w")

    tk.Label(frame_ayuda,text="dd/mm/yyyy",fg="green", font=("Arial",10)).grid(row=2, column=1, pady=1,padx=30,columnspan=2)

    tk.Button(frame_ayuda, text="Cerrar", border=2,command=lambda:root_ayuda.destroy()).grid(row=3,column=2, pady=15,padx=10, ipadx=5,ipady=5)


#---------------------------------------------------------------------------------------------------

barra_menu = tk.Menu(root)
root.config(menu=barra_menu)

archivo = tk.Menu(barra_menu, tearoff=0)
archivo.add_command(label="Conectar", command=conectar)
archivo.add_command(label="Salir", command=salir)

limpiar = tk.Menu(barra_menu, tearoff=0)
limpiar.add_command(label="Limpiar Campos", command=limpiar_campos)

modificar = tk.Menu(barra_menu, tearoff=0)
modificar.add_command(label="Añadir registro", command=agregar)

ver = tk.Menu(barra_menu,tearoff=0)
ver.add_command(label="Mostrar todo", command=mostrar_todo)
ver.add_command(label="Mostrar Libres", command=mostrar_libres)

ayuda = tk.Menu(barra_menu, tearoff=0)
ayuda.add_command(label="Mostrar Ayuda", command=mostrar_ayuda)

barra_menu.add_cascade(label="Archivo", menu =archivo)
barra_menu.add_cascade(label="Limpiar", menu=limpiar)
barra_menu.add_cascade(label="Modificar", menu=modificar)
barra_menu.add_cascade(label="Ver", menu=ver)
barra_menu.add_cascade(label="Ayuda",menu=ayuda)


tk.Label(frame, text="Feriado Asistido\t\t:").grid(row=1, column=1, padx= 10, pady= 10, sticky="w")
tk.Label(frame, text="Fecha Compensado\t:").grid(row=2, column=1, padx= 10, pady= 10, sticky="w")
tk.Label(frame, text="Estado Compensado\t:").grid(row=3, column=1, padx= 10, pady= 10, sticky="w")



entry_feriado = tk.Entry(frame, border = 2, textvariable=feriado)
entry_feriado.grid(row=1,column=2, padx= 10, pady= 10)
entry_feriado.bind("<Key>", cuandoEscriba2)
entry_feriado.bind("<BackSpace>", lambda _:entry_feriado.delete(tk.END))

entry_fecha = tk.Entry(frame, border = 2, textvariable=fecha)
entry_fecha.grid(row=2,column=2, padx= 10, pady= 10)
entry_fecha.bind("<Key>", cuandoEscriba)
entry_fecha.bind("<BackSpace>", lambda _:entry_fecha.delete(tk.END))

"""entry_estado = tk.Entry(frame, border = 2, textvariable=estado)
entry_estado.grid(row=3,column=2, padx= 10, pady= 10)"""

#Debemos importar ttk desde tkinter para usar el combobox.
#Para que el usuario no pueda agregar ningun valor al combobox debemos indicar que el estado es solo lectura(readonly)
#Le asignamos una variable al combobox para trabajar con ella y obtener con .get() o setear con .set()
#Para agregar valores al combobox se indica la variable seguido de ["values"] sin ningún punto antes y en una lista se agrega cada uno de los valores del combobox
combo_estado = ttk.Combobox(frame, state="readonly", width=17,textvariable=estado)
combo_estado["values"] = ["Compensado","Libre","En espera","Aprobado"]
combo_estado.grid(row=3,column=2, padx= 10, pady= 10)

frame2 = tk.Frame(root)
frame2.pack()

boton_agregar = tk.Button(frame2, text="Agregar", border=2, command=agregar)
boton_agregar.grid(row=1, column=1, padx=20,pady=10)

boton_mostrar = tk.Button(frame2, text="Mostrar", border=2, command=mostrar)
boton_mostrar.grid(row=1, column=2, padx=20,pady=10)

boton_modificar = tk.Button(frame2, text="Modificar", border=2, command=cambiar)
boton_modificar.grid(row=1, column=3, padx=20,pady=10)

root.mainloop()

