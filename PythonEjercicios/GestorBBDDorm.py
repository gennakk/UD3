import os.path
import csv
import sqlite3

import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

import Clases

class GestorBBDDorm:

    def __init__(self):
        self.ps = ""

    def listadoDeportistasDeporte(self):
        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            engine = create_engine("mysql://olimpiadas:olimpiadas@localhost/olimpiadas", echo=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        # evento = Clases.Evento
        #
        # e = evento.select()

        s = self.ps
        Sesion = sessionmaker(bind=engine)
        sesion = Sesion()

        temporada = ""

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

        result_set = sesion.query(Clases.Olimpiada).filter(Clases.Olimpiada.temporada == temporada).all()
        dict_olimpiada = {}
        for olimpiada in result_set:
            print(olimpiada.id_olimpiada, olimpiada.nombre)
            dict_olimpiada[str(olimpiada.id_olimpiada)] = olimpiada.nombre

        id_olimpiada = input("Selecciona id olimpiada")
# hola
        query = sesion.query(Clases.Evento).filter(Clases.Evento.id_olimpiada==id_olimpiada)
        dict_deporte = {}
        for deporte in query:
            print(deporte.nombre)
            # print(deporte.id_deporte, deporte.nombre)
            # dict_deporte[str(deporte.id_deporte)] = deporte.nombre

        id_deporte = input("Introduce id deporte")

        query = sesion.query(Clases.Evento).filter(Clases.Evento.id_deporte == id_deporte, Clases.Evento.id_olimpiada == id_olimpiada )
        dict_evento = {}
        for evento in query:
            print(evento.id_evento, evento.nombre)
            dict_evento[str(evento.id_evento)] = evento.nombre

        id_evento = input("Introduce id evento")

        print(temporada, dict_olimpiada[id_olimpiada], dict_deporte[id_deporte], dict_evento[id_evento])

        query = sesion.query(Clases.Participacion).filter( Clases.Participacion.id_evento == id_evento)
        for participacion in query:
            print(participacion.deportista.nombre, participacion.deportista.sexo, participacion.deportista.altura, participacion.deportista.peso, participacion.edad, participacion.evento.nombre, participacion.medalla)


        sesion.close()


    def modificarMedallaDeportista(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            engine = create_engine("mysql://olimpiadas:olimpiadas@localhost/olimpiadas", echo=True)

        elif opcion == 2:
            self.paramStyle(sqlite3)
            conexion = sqlite3.connect("olimpiadas.sqlite")

        else:
            print("Opción incorrecta")
            return

        s = self.ps
        Sesion = sessionmaker(bind=engine)
        sesion = Sesion()


        nom_dep = input("Introduce nombre de deportista")

        query = sesion.query(Clases.Deportista).filter(Clases.Deportista.nombre.match("%"+nom_dep+"%"))

        print("DEPORTISTAS")
        for deportista in query:
            print("Número: " + deportista.id_deportista + ", " + "Nombre: " +deportista.nombre + ".")
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
