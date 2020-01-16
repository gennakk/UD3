
from PythonEjercicios.GestorBBDDorm import GestorBBDDorm

gestor = GestorBBDDorm()

opcion = 6

#Menú
while opcion != 0:
    print("1. Crear BBDD MySQL")
    print("2. Crear BBDD SQLite")
    print("3. Listado de deportistas en diferentes deportes")
    print("4. Listado de deportistas participantes")
    print("5. Modificar medalla deportista")
    print("6. Añadir deportista/participación")
    print("7. Eliminar participación")
    print("0. Salir")

    opcion = int(input("Introduce opcion"))

    if opcion == 1:
        gestor.crearBBDDMySql()
    elif opcion == 2:
        gestor.crearBBDDSQLite()
    elif opcion == 3:
        gestor.listadoDeportistasDeporte()
    elif opcion == 4:
        gestor.listadoDeportistasParticipantes()
    elif opcion == 5:
        gestor.modificarMedallaDeportista()
    elif opcion == 6:
        gestor.aniadirParticipacion()
    elif opcion == 7:
        gestor.eliminarParticipacion()
