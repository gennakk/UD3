while True:
    o = input(
        """¿Qué desea hacer? Introduzca un número:
    1. Listado de deportistas participantes
    2. Modificar medalla deportista
    3. Añadir deportista/participación
    4. Eliminar participación

    0. Salir

      > """)

    if o == "1":
        from ejer4_1 import participantes
        participantes()
    elif o == "2":
        from ejer4_2 import medalla
        medalla()
    elif o == "3":
        from ejer4_3 import add
        add()
    elif o == "4":
        from ejer4_4 import delete
        delete()
    elif o == "0":
        break
    else:
        print("No has introducido uno de los números pedidos")
