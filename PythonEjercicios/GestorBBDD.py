import os.path
import csv
import sqlite3

import mysql.connector


class GestorBBDD:

    def __init__(self):
        self.ps = ""

    def listadoDeportistasDeporte(self):
        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                               passwd="olimpiadas", autocommit=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        s = self.ps
        cursor = conexion.cursor()

        queryID = """SELECT DISTINCT Participacion.id_deportista
FROM Participacion, Evento
WHERE Participacion.id_evento = Evento.id_evento
AND EXISTS
	(SELECT DISTINCT p.id_deportista, e.id_deporte
    FROM Participacion p, Evento e
    WHERE p.id_evento = e.id_evento
    AND Participacion.id_deportista = p.id_deportista
    AND Evento.id_deporte != e.id_deporte
    )"""
        cursor.execute(queryID)
        result_set = cursor.fetchall()
        for id in result_set:
            #Datos deportista
            queryDeportista = "SELECT id_deportista,nombre,sexo,altura,peso FROM Deportista WHERE id_deportista = " + s
            cursor.execute(queryDeportista,id)
            result_set = cursor.fetchall()
            for row in result_set:
                # print("Nombre: " + row["nombre"] + ", " + "Sexo: " + row["sexo"] + ", " + "Altura: " + row["altura"] + ", " + "Peso: " + row["peso"] + ".")
                print("Nombre: " + str(row[1]) + ", " + "Sexo: " + str(row[2]) + ", " + "Altura: " + str(row[3]) + ", " + "Peso: " + str(row[4]) + ".")

            #Resto de datos
            queryDatos = "SELECT p.edad ,p.medalla ,ev.nombre ,d.nombre ,o.nombre , eq.nombre  FROM Participacion p, Evento ev,Deporte d,Olimpiada o, Equipo eq WHERE p.id_deportista = " + s + " AND ev.id_evento=p.id_evento AND ev.id_deporte = d.id_deporte AND ev.id_olimpiada=o.id_olimpiada AND eq.id_equipo = p.id_equipo "
            cursor.execute(queryDatos,id)
            result_set = cursor.fetchall()
            for row in result_set:
                # print("Deporte: " + row["nombreD"]+", Edad: " + row["edad"]+", Evento: " + row["nombreEv"]+", Equipo: " + row["nombreEq"]+", Juegos : " + row["nombreO"]+", Medalla: " + row["medalla"]+".")
                print("Deporte: " + str(row[3])+", Edad: " + str(row[0])+", Evento: " + str(row[2])+", Equipo: " + str(row[5])+", Juegos : " + str(row[4])+", Medalla: " + str(row[1])+".")
            print("-----------------------------------------------------------------------------------")

        conexion.close()

    def listadoDeportistasParticipantes(self):
        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                               passwd="olimpiadas", autocommit=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        s = self.ps
        cursor = conexion.cursor()

        print("1. Temporada Winter")
        print("2. Temporada Summer")
        opcion = int(input("Introduce opcion"))
        if opcion == 1:
            temporada = "Winter"
        elif opcion == 2:
            temporada = "Summer"
        else:
            print("Opción incorrecta")
            return

        dict_edicion = {}
        queryEdicion = "SELECT id_olimpiada,nombre FROM Olimpiada WHERE temporada = " + s
        cursor.execute(queryEdicion, (temporada,))
        result_set = cursor.fetchall()
        print("EDICIONES")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
            dict_edicion[str(row[0])] = str(row[1])
        id_olimpiada = input("Introduce número: ")


        dict_deporte = {}
        queryDeportes = "SELECT DISTINCT d.id_deporte id_deporte,d.nombre nombre FROM Deporte d,Evento ev WHERE ev.id_olimpiada = "+s+" AND d.id_deporte = ev.id_deporte"
        cursor.execute(queryDeportes,(id_olimpiada,))
        result_set = cursor.fetchall()
        print("DEPORTES")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
            dict_deporte[str(row[0])] = str(row[1])
        id_deporte = input("Introduce número: ")

        dict_evento = {}
        queryEvento = "SELECT id_evento,nombre FROM Evento WHERE id_olimpiada = "+s+" AND id_deporte = "+s
        cursor.execute(queryEvento,(id_olimpiada, id_deporte))
        result_set = cursor.fetchall()
        print("EVENTOS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " +"Nombre: " + str(row[1]) + ".")
            dict_evento[str(row[0])] = str(row[1])
        id_evento = input("Introduce número: ")

        print("-----------------------------------------------------------------------------------")
        print("Temporada: "+ temporada)
        print("Edición: " + dict_edicion[id_olimpiada])
        print("Deporte: "+ dict_deporte[id_olimpiada])
        print("Evento: " + dict_evento[id_olimpiada])
        queryDeportista = "SELECT d.nombre,d.altura,d.peso,p.edad,e.nombre,p.medalla FROM Participacion p , Deportista d, Equipo e, Evento ev WHERE ev.id_olimpiada = " + s + " AND p.id_evento = " + s + " AND ev.id_evento = p.id_evento AND d.id_deportista = p.id_deportista AND p.id_equipo = e.id_equipo"
        cursor.execute(queryDeportista, (id_olimpiada, id_evento))
        result_set = cursor.fetchall()
        print("DEPORTISTAS")
        for row in result_set:
            print("Nombre: " + str(row[0]) + ", " + "Altura: " + str(row[1]) + ", ""Peso: " + str(row[2]) + ", ""Edad: " + str(row[3]) + ", ""Equipo: " + str(row[4]) + ", "+" Medalla: " + str(row[5]) + ".")
            dict_evento[str(row[0])] = str(row[1])
        print("-----------------------------------------------------------------------------------")

        conexion.close()

    def modificarMedallaDeportista(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                               passwd="olimpiadas", autocommit=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        s = self.ps

        cursor = conexion.cursor()
        nom_dep = input("Introduce nombre de deportista")

        queryDeportista = "SELECT id_deportista,nombre FROM Deportista WHERE nombre LIKE " + s
        cursor.execute(queryDeportista, ("%"+nom_dep+"%",))
        result_set = cursor.fetchall()
        print("DEPORTISTAS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
        id_deportista = input("Introduce número: ")

        queryParticipacion = "SELECT p.id_evento,e.nombre FROM Participacion p,Evento e WHERE p.id_deportista = " + s + " AND e.id_evento = p.id_evento"
        cursor.execute(queryParticipacion, (id_deportista,))
        result_set = cursor.fetchall()
        print("EVENTOS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
        id_evento = input("Introduce número: ")

        print("1. Oro")
        print("2. Plata")
        print("3. Bronce")
        print("4. Sin medalla")
        opcion = int(input("Introduce opcion"))
        if opcion == 1:
            medalla = "Gold"
        elif opcion == 2:
            medalla = "Silver"
        elif opcion == 3:
            medalla = "Bronze"
        elif opcion == 4:
            medalla = "NA"
        else:
            print("Opción incorrecta")
            return

        #UPDATE
        queryUpdate = "UPDATE Participacion SET medalla = " + s + " WHERE id_deportista = " + s +" AND id_evento = " + s
        cursor.execute(queryUpdate, (medalla, id_deportista, id_evento))

        print("Medalla modificada.")

        conexion.close()

    def aniadirParticipacion(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                               passwd="olimpiadas", autocommit=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        cursor = conexion.cursor()
        s = self.ps

        nom_dep = input("Introduce nombre de deportista")
        queryDeportista = "SELECT id_deportista,nombre FROM Deportista WHERE nombre LIKE " + s
        cursor.execute(queryDeportista, ("%" + nom_dep + "%",))
        result_set = cursor.fetchall()
        print("DEPORTISTAS")
        if(result_set.__len__()!=0):
            for row in result_set:
                print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
            id_deportista = input("Introduce número: ")
        else:
            print("CREAR DEPORTISTA")
            nombre = input("Introduce nombre")
            sexo = input("Introduce sexo")
            peso = input("Introduce peso")
            altura = input("Introduce altura")

            queryInsertDeportista = "INSERT INTO Deportista(nombre,sexo,peso,altura) VALUES  ("+s+", "+s+", "+s+", "+s+")"
            cursor.execute(queryInsertDeportista, ( nombre, sexo, peso, altura))

        print("1. Temporada Winter")
        print("2. Temporada Summer")
        opcion = int(input("Introduce opcion"))
        if opcion == 1:
            temporada = "Winter"
        elif opcion == 2:
            temporada = "Summer"
        else:
            print("Opción incorrecta")
            return


        queryEdicion = "SELECT id_olimpiada,nombre FROM Olimpiada WHERE temporada = " + s
        cursor.execute(queryEdicion, (temporada,))
        result_set = cursor.fetchall()
        print("EDICIONES")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")

        id_olimpiada = input("Introduce número: ")

        queryDeportes = "SELECT DISTINCT d.id_deporte id_deporte,d.nombre nombre FROM Deporte d,Evento ev WHERE ev.id_olimpiada = " + s + " AND d.id_deporte = ev.id_deporte"
        cursor.execute(queryDeportes, (id_olimpiada,))
        result_set = cursor.fetchall()
        print("DEPORTES")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
        id_deporte = input("Introduce número: ")

        queryEvento = "SELECT id_evento,nombre FROM Evento WHERE id_olimpiada = " + s + " AND id_deporte = " + s
        cursor.execute(queryEvento, (id_olimpiada, id_deporte))
        result_set = cursor.fetchall()
        print("EVENTOS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")

        id_evento = input("Introduce número: ")

        id_equipo = input("Introduce número de equipo")
        edad = input("Introduce edad")
        medalla = input("Introduce medalla")

        # INSERT
        queryInsert = "INSERT INTO Participacion (id_deportista,id_evento,id_equipo,edad,medalla) VALUES ("+s+", "+s+", "+s+", "+s+", "+s+")"
        cursor.execute(queryInsert, (id_deportista, id_evento, id_equipo, edad, medalla))

        print("Participación añadida.")

        conexion.close()

    def eliminarParticipacion(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                               passwd="olimpiadas", autocommit=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        s = self.ps

        cursor = conexion.cursor()

        nom_dep = input("Introduce nombre de deportista")
        queryDeportista = "SELECT id_deportista,nombre FROM Deportista WHERE nombre LIKE " + s
        cursor.execute(queryDeportista, ("%" + nom_dep + "%",))
        result_set = cursor.fetchall()
        print("DEPORTISTAS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
        id_deportista = input("Introduce número: ")

        queryParticipacion = "SELECT p.id_evento,e.nombre FROM Participacion p,Evento e WHERE p.id_deportista = " + s + " AND e.id_evento = p.id_evento"
        cursor.execute(queryParticipacion, (id_deportista,))
        result_set = cursor.fetchall()
        print("EVENTOS")
        for row in result_set:
            print("Número: " + str(row[0]) + ", " + "Nombre: " + str(row[1]) + ".")
        id_evento = input("Introduce número: ")
        queryDeleteParticipacion = "DELETE FROM Participacion WHERE id_deportista = " + s + " AND id_evento = " + s
        cursor.execute(queryDeleteParticipacion, (id_deportista, id_evento))
        print("Participacion borrada.")

        if result_set.__len__()==1:
            queryDeleteDeportista = "DELETE FROM Deportista WHERE id_deportista = " + s
            cursor.execute(queryDeleteDeportista, (id_deportista,))
            print("Deportista borrado.")

        conexion.close()

    def crearBBDDMySql(self):

        self.paramStyle(mysql.connector)

        conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                           passwd="olimpiadas", autocommit=True)

        cursor = conexion.cursor()

        file = open('olimpiadas.sql')
        sql = file.read()
        results = cursor.execute(sql, multi=True)

        for cur in results:
            if cur.with_rows:
                cur.fetchall()

        conexion.commit()

        cursor.close()

        conexion.close()

        conexion = mysql.connector.connect(host="localhost", database="olimpiadas", user="olimpiadas",
                                           passwd="olimpiadas", autocommit=True)

        self.crearBBDD(conexion)

    def crearBBDDSQLite(self):
        # ruta = input("Introduce la ruta del archivo SQLite")
        # ruta = "athlete_events_bueno.csv"

        self.paramStyle(sqlite3)

        conexion = sqlite3.connect("olimpiadas.sqlite")

        cursor = conexion.cursor()

        file = open('olimpiadas-backup.sql').encode('utf-8').strip()
        sql = file.read()
        results = cursor.execute(sql, multi=True)

        for cur in results:
            if cur.with_rows:
                cur.fetchall()

        conexion.commit()

        cursor.close()

        conexion.close()

        conexion = sqlite3.connect("olimpiadas.sqlite")

        self.crearBBDD(conexion)

    def crearBBDD(self, conexion):

        # ruta = input("Introduce la ruta del archivo csv")
        ruta = "athlete_events_bueno.csv"

        if not os.path.exists(ruta):
            print("El archivo csv no existe.")

        cursor = conexion.cursor()

        dict_olimpiadas = {}

        dict_deportes = {}

        lista_deportistas_id = set()

        dict_equipo = {}

        dict_evento = {}

        lista_query_olimpiada = set()

        lista_query_deportes = set()

        lista_query_deportistas = []

        lista_query_equipo = set()

        lista_query_evento = set()

        lista_query_participacion = []

        id_olimpiada = 1
        id_deporte = 1
        id_equipo = 1
        id_evento = 1

        with open(ruta) as file_olimpiadas:
            reader = csv.DictReader(file_olimpiadas)

            for linea in reader:

                # Tabla Olimpiada
                if not linea["Games"] in dict_olimpiadas:
                    lista_query_olimpiada.add(
                        (id_olimpiada, linea["Games"], linea["Year"], linea["Season"], linea["City"]))
                    dict_olimpiadas[linea["Games"]] = id_olimpiada
                    id_olimpiada += 1

                # Tabla Deporte
                if not linea["Sport"] in dict_deportes:
                    lista_query_deportes.add((id_deporte, linea["Sport"],))
                    dict_deportes[linea["Sport"]] = id_deporte
                    id_deporte += 1

                # Tabla Deportista
                if not lista_deportistas_id.__contains__(linea["ID"]):
                    lista_deportistas_id.add(linea["ID"])

                    lista_query_deportistas.append(
                        (linea["ID"], linea["Height"], linea["Name"], linea["Weight"], linea["Sex"]))

                # Tabla Equipo
                if not linea["NOC"] in dict_equipo:
                    lista_query_equipo.add((id_equipo, linea["Team"], linea["NOC"]))

                    dict_equipo[linea["NOC"]] = id_equipo
                    id_equipo += 1

                # Tabla Evento !!!!
                if not (linea["Sport"], linea["Games"], linea["Event"]) in dict_evento:
                    lista_query_evento.add(
                        (id_evento, linea["Event"], dict_olimpiadas[linea["Games"]], dict_deportes[linea["Sport"]]))
                    dict_evento[linea["Sport"], linea["Games"], linea["Event"]] = id_evento
                    id_evento += 1

                lista_query_participacion.append((linea["ID"],
                                                  dict_evento[linea["Sport"], linea["Games"], linea["Event"]],
                                                  linea["Age"], dict_equipo[linea["NOC"]], linea["Medal"]))

        try:
            s = self.ps

            queryOlimpiada = "INSERT INTO Olimpiada(id_olimpiada,nombre,anio,temporada,ciudad) VALUES (" + s + "," + s + "," + s + "," + s + "," + s + ")"
            cursor.executemany(queryOlimpiada, lista_query_olimpiada)

            queryDeporte = "INSERT INTO Deporte(id_deporte,nombre) VALUES (" + s + "," + s + ")"
            cursor.executemany(queryDeporte, lista_query_deportes)

            queryDeportistas = "INSERT INTO Deportista(id_deportista,altura,nombre,peso,sexo) VALUES (" + s + "," + s + "," + s + "," + s + "," + s + ")"
            # cursor.executemany(queryDeportistas, lista_query_deportistas)
            salto = 20000
            i = 0
            while i < len(lista_query_deportistas):
                cursor.executemany(queryDeportistas, lista_query_deportistas[i:salto + i])
                i += salto

            queryEquipo = "INSERT INTO Equipo(id_equipo,nombre,iniciales) VALUES (" + s + "," + s + "," + s + ")"
            cursor.executemany(queryEquipo, lista_query_equipo)
            conexion.commit()

            queryEvento = "INSERT INTO Evento(id_evento,nombre,id_olimpiada,id_deporte) VALUES (" + s + "," + s + "," + s + "," + s + ")"
            cursor.executemany(queryEvento, lista_query_evento)
            conexion.commit()

            queryParticipacion = "INSERT INTO Participacion(id_deportista,id_evento,edad,id_equipo,medalla) VALUES (" + s + "," + s + "," + s + "," + s + "," + s + ")"

            # cursor.executemany(queryParticipacion, lista_query_participacion)
            salto = 20000
            i = 0
            while i <= len(lista_query_participacion):
                cursor.executemany(queryParticipacion, lista_query_participacion[i:salto + i])
                conexion.commit()
                i += salto
        except Exception as e:
            print(e)
            print("Ha ocurrido algún error en la carga.")
        finally:
            conexion.close()

        print("La carga de la información se ha realizado correctamente.")
        return

    def paramStyle(self, bbdd):
        paramstyle = bbdd.paramstyle

        if paramstyle == 'qmark':
            self.ps = "?"
        elif paramstyle == 'pyformat':
            self.ps = "%s"
        else:
            raise Exception("Unexpected paramstyle: %s" % paramstyle)
