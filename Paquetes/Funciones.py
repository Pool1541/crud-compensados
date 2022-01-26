


def agregar_comilla(x):
    dato = "'"+x.get()+"'"
    return dato


def validar_fecha(fecha_comp):
    valor = fecha_comp.get()
    
    if len(valor) == 10 :
        if int(valor[0:2]) <=31 and int(valor[3:5]) <= 12 and int(valor[6:10]) <= 2021:
            return True
        else:
            return False
    else:
        return False



def centrar(root):
    ancho = 330
    alto = 200

    x_ventana = root.winfo_screenwidth() // 2 - ancho // 2
    y_ventana = root.winfo_screenheight() // 2 - alto // 2

    posicion = str(ancho) + "x" + str(alto) + "+" + str(x_ventana) + "+" + str(y_ventana)
    return posicion


