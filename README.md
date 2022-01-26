# crud-compensados
Proyecto en Python para almacenar, mostrar, editar y eliminar fechas.
El presente es un proyecto que realice con el fin de poner en práctica mis conocimientos adquiridos en el lenguaje de programación Python además de la librería tkinter y sqlite.
El proyecto consta de una interfaz gráfica simple realizada con tkinter con la cual podemos crear y/o conectar una base de datos donde almacenamos fechas.
Estas fechas pueden tener diferentes estados:
Compensado : Quiere decir que la fecha ya ha sido pagada por el empleador/jefe, el trabajador ya tomó el día que estaba pendiente.
Libre : Es un dia pendiente a compensar.
En espera : Se envió la solicitud al jefe indicando el día que se trabajó y el día en el que se tomará a espera de una respuesta positiva o negativa.
Aprobado : El jefe ya dió una respuesta sobre la solicitud del día a compensar pero el día todavía no se ha tomado.

El proyecto tiene un campo donde se indica el día asistido y otro campo para indicar el día en el que se solicita la compensación de este.

Además cuenta con diferentes opciones para mostrar las fechas ingresadas con el estado actual de estas. Podemos añadir, modificar, leer y borrar los datos ingresados
a la base de datos a través de la interfaz gráfica.

El proyecto es muy simple y está desarrollada con Python Tkinter y sqlite.
