import os.path
import csv
import sqlite3
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

from PythonEjercicios import Clases


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
            engine = create_engine('sqlite:///database.db')

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

        query = sesion.query(Clases.Evento).filter(Clases.Evento.id_olimpiada==id_olimpiada,Clases.Evento.id_deporte == id_deporte)
        for participacion in query:
            print(participacion.deportista.nombre, participacion.deportista.sexo, participacion.deportista.altura, participacion.deportista.peso, participacion.edad, participacion.evento.nombre, participacion.medalla)


        sesion.close()
        engine.close()


    def modificarMedallaDeportista(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            engine = create_engine("mysql://olimpiadas:olimpiadas@localhost/olimpiadas", echo=True)

        elif opcion == 2:
            self.paramStyle(sqlite3)
            engine = create_engine('sqlite:///database.db')

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

        query = sesion.query(Clases.Participacion,Clases.Evento,Clases.Olimpiada).filter(
            Clases.Evento.id_evento==Clases.Participacion.id_evento,
            Clases.Olimpiada.id_olimpiada==Clases.Evento.id_olimpiada,
            Clases.Participacion.id_deportista==id_deportista
        )
        print("EVENTOS")
        for participacion,evento,olimpiada in query:
            print("Número: " + str(evento.id_evento) + ", " + "Nombre: " + str(evento.nombre) + ".")
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

        sesion.query(Clases.Participacion).filter(Clases.Participacion.id_deportista==id_deportista,Clases.Participacion.id_evento==id_evento).update({Clases.Participacion.medalla:medalla}, synchronize_session = False)
        sesion.commit()
        print("Medalla modificada.")

        sesion.close()
        engine.close()

    def aniadirParticipacion(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            engine = create_engine("mysql://olimpiadas:olimpiadas@localhost/olimpiadas", echo=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            engine = create_engine('sqlite:///database.db')
        else:
            print("Opción incorrecta")
            return

        s = self.ps
        Sesion = sessionmaker(bind=engine)
        sesion = Sesion()

        nom_dep = input("Introduce nombre de deportista")
        query = sesion.query(Clases.Deportista).filter(Clases.Deportista.nombre.match("%"+nom_dep+"%"))
        print("DEPORTISTAS")
        if(query.__len__()!=0):
            for deportista in query:
                print("Número: " + str(deportista.id_deportista) + ", " + "Nombre: " + str(deportista.nombre) + ".")
            id_deportista = input("Introduce número: ")
        else:
            print("CREAR DEPORTISTA")
            nombre = input("Introduce nombre")
            sexo = input("Introduce sexo")
            peso = input("Introduce peso")
            altura = input("Introduce altura")

            deportista = Clases.Deportista(nombre=nombre, sexo=sexo, peso=peso, altura=altura)
            id_deportista = sesion.add(deportista)
            sesion.commit()

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


        queryEdicion = sesion.query(Clases.Olimpiada).filter(Clases.Olimpiada.temporada.match("%"+temporada+"%"))
        print("EDICIONES")
        for olimpiada in queryEdicion:
            print("Número: " + str(olimpiada.id_olimpiada) + ", " + "Nombre: " + str(olimpiada.nombre) + ".")

        id_olimpiada = input("Introduce número: ")

        queryDeportes = sesion.query(Clases.Deporte).filter(Clases.Evento.id_deporte==Clases.Deporte.id_deporte,Clases.Evento.id_olimpiada==id_olimpiada)
        print("DEPORTES")
        for deporte in queryDeportes:
            print("Número: " + str(deporte.id_deporte) + ", " + "Nombre: " + str(deporte.nombre) + ".")
        id_deporte = input("Introduce número: ")

        queryEvento = sesion.query(Clases.Evento).filter(Clases.Evento.id_deporte==id_deporte,Clases.Evento.id_olimpiada==id_olimpiada)
        print("EVENTOS")
        for evento in queryEvento:
            print("Número: " + str(evento.id_evento) + ", " + "Nombre: " + str(evento.nombre) + ".")

        id_evento = input("Introduce número: ")

        id_equipo = input("Introduce número de equipo")
        edad = input("Introduce edad")
        medalla = input("Introduce medalla")

        # INSERT
        participacion = Clases.Participacion(
            id_deportista=id_deportista,
            id_evento=id_evento,
            id_equipo=id_equipo,
            edad=edad,
            medalla=medalla
        )
        sesion.add(participacion)
        sesion.commit()

        print("Participación añadida.")

        sesion.close()
        engine.close()

    def eliminarParticipacion(self):

        print("1. Consulta MySQL")
        print("2. Consulta SQLite")
        opcion = int(input("Introduce opcion"))

        if opcion == 1:
            self.paramStyle(mysql.connector)
            engine = create_engine("mysql://olimpiadas:olimpiadas@localhost/olimpiadas", echo=True)
        elif opcion == 2:
            self.paramStyle(sqlite3)
            engine = create_engine('sqlite:///database.db')
        else:
            print("Opción incorrecta")
            return

        s = self.ps
        Sesion = sessionmaker(bind=engine)
        sesion = Sesion()

        nom_dep = input("Introduce nombre de deportista")
        queryDeportista = sesion.query(Clases.Deportista).filter(Clases.Deportista.nombre.match("%"+nom_dep+"%"))
        print("DEPORTISTAS")
        for deportista in queryDeportista:
            print("Número: " + str(deportista.id_deportista) + ", " + "Nombre: " + str(deportista.nombre) + ".")
        id_deportista = input("Introduce número: ")

        queryParticipacion = sesion.query(Clases.Participacion,Clases.Evento,Clases.Olimpiada,Clases.Deportista).filter(
            Clases.Evento.id_evento==Clases.Participacion.id_evento,
            Clases.Olimpiada.id_olimpiada==Clases.Evento.id_olimpiada,
            Clases.Deportista.id_deportista==Clases.Participacion.id_deportista,
            Clases.Participacion.id_deportista==id_deportista
        )
        print("EVENTOS")
        for participacion,evento,olimpiada,deportista in queryParticipacion:
            print("Número: " + str(evento.id_eventon) + ", " + "Nombre: " + str(evento.nombre) + ".")
        id_evento = input("Introduce número: ")

        participacion = sesion.query(Clases.Participacion).filter(
            Clases.Participacion.id_evento == id_evento,
        )
        sesion.delete(participacion)
        sesion.commit()
        print("Participacion borrada.")

        if queryParticipacion.__len__()==1:
            deportista = sesion.query(Clases.Deportista).filter(
                Clases.Deportista.id_evento == id_deportista,
            )
            sesion.delete(deportista)
            sesion.commit()
            print("Deportista borrado.")

        sesion.close()
        engine.close()

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
